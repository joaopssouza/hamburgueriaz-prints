"""Usa o app HamburgueriaZ no emulador (via adb) e captura as telas do relatório."""
import os
import subprocess
import time
import xml.etree.ElementTree as ET

from PIL import Image

PKG = "com.example.hamburgueriaz"
OUT = "prints"
os.makedirs(OUT, exist_ok=True)


def adb(*args):
    return subprocess.run(["adb", *args], capture_output=True, text=True, check=True)


def shot(nome):
    with open(os.path.join(OUT, nome + ".png"), "wb") as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f, check=True)
    print("capturado", nome)


def centro(rid):
    adb("shell", "uiautomator", "dump", "/sdcard/ui.xml")
    adb("pull", "/sdcard/ui.xml", "ui.xml")
    for n in ET.parse("ui.xml").iter("node"):
        if n.get("resource-id") == "%s:id/%s" % (PKG, rid):
            x1, y1, x2, y2 = [int(v) for v in n.get("bounds").replace("][", ",").strip("[]").split(",")]
            return (x1 + x2) // 2, (y1 + y2) // 2
    raise SystemExit("elemento nao encontrado: " + rid)


def rolar():
    w, h = [int(v) for v in adb("shell", "wm", "size").stdout.split()[-1].split("x")]
    adb("shell", "input", "swipe", str(w // 2), str(int(h * 0.75)), str(w // 2), str(int(h * 0.25)), "400")
    time.sleep(1)


def toque(rid):
    try:
        x, y = centro(rid)
    except SystemExit:
        rolar()
        x, y = centro(rid)
    adb("shell", "input", "tap", str(x), str(y))
    time.sleep(0.6)


# instala os dois apps (o segundo é o e-mail simulado)
adb("install", "-r", "app/build/outputs/apk/debug/app-debug.apk")
adb("install", "-r", "mailstub/build/outputs/apk/debug/mailstub-debug.apk")

adb("shell", "am", "start", "-n", PKG + "/.MainActivity")
time.sleep(5)

# 2-5: interface inicial; 2-6: topo da tela (banner)
shot("2-5")
img = Image.open(os.path.join(OUT, "2-5.png"))
img.crop((0, 0, img.width, int(img.height * 0.30))).save(os.path.join(OUT, "2-6.png"))

# preenche o pedido: Joao, Bacon + Queijo, quantidade 2
toque("editNome")
adb("shell", "input", "text", "Joao")
adb("shell", "input", "keyevent", "4")  # fecha o teclado
time.sleep(0.8)
toque("checkBacon")
toque("checkQueijo")
toque("btnMais")
toque("btnMais")
shot("3-1")

# envia o pedido: o Intent abre o app de e-mail
toque("btnEnviar")
time.sleep(3)
shot("3-3")

# volta e mostra o resumo do pedido
adb("shell", "input", "keyevent", "4")
time.sleep(2)
rolar()
shot("3-2")
