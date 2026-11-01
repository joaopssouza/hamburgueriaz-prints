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


def nos():
    adb("shell", "uiautomator", "dump", "/sdcard/ui.xml")
    adb("pull", "/sdcard/ui.xml", "ui.xml")
    return list(ET.parse("ui.xml").iter("node"))


def centro_no(n):
    x1, y1, x2, y2 = [int(v) for v in n.get("bounds").replace("][", ",").strip("[]").split(",")]
    return (x1 + x2) // 2, (y1 + y2) // 2


def achar(rid=None, texto=None):
    for n in nos():
        if rid and n.get("resource-id") == "%s:id/%s" % (PKG, rid):
            return n
        if texto and n.get("text") == texto:
            return n
    return None


def rolar():
    w, h = [int(v) for v in adb("shell", "wm", "size").stdout.split()[-1].split("x")]
    adb("shell", "input", "swipe", str(w // 2), str(int(h * 0.75)), str(w // 2), str(int(h * 0.25)), "400")
    time.sleep(1)


def toque(rid=None, texto=None):
    n = achar(rid, texto)
    if n is None:
        rolar()
        n = achar(rid, texto)
    if n is None:
        shot("erro-" + (rid or "texto"))
        raise SystemExit("elemento nao encontrado: %s %s" % (rid, texto))
    x, y = centro_no(n)
    adb("shell", "input", "tap", str(x), str(y))
    time.sleep(0.8)


def fechar_teclado():
    for _ in range(3):
        if "mInputShown=true" not in adb("shell", "dumpsys", "input_method").stdout:
            return
        adb("shell", "input", "keyevent", "4")
        time.sleep(1)


def esperar_foco(trecho, segundos=30):
    for _ in range(segundos):
        if trecho in adb("shell", "dumpsys", "window").stdout.split("mCurrentFocus")[-1].split("\n")[0]:
            return True
        time.sleep(1)
    return False


# sem teclado virtual: evita sugestões/autocorreção no campo do nome
for ime in adb("shell", "ime", "list", "-s").stdout.split():
    adb("shell", "ime", "disable", ime)

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
time.sleep(0.8)
# fecha o teclado (se estiver aberto) para nao cobrir os botoes
fechar_teclado()
toque("checkBacon")
toque("checkQueijo")
toque("btnMais")
toque("btnMais")
shot("3-1")

# envia o pedido: o Intent abre o seletor e depois o app de e-mail
toque("btnEnviar")
time.sleep(2)
shot("dbg-seletor")
toque(texto="E-mail (simulado)")
if achar(texto="Just once"):
    toque(texto="Just once")
print("e-mail em foco:", esperar_foco("mailstub"))
time.sleep(2)
shot("3-3")

# volta ao app e mostra o resumo do pedido
adb("shell", "input", "keyevent", "4")
time.sleep(2)
esperar_foco("hamburgueriaz")
fechar_teclado()
resumo = achar("txtResumo")
print("resumo na tela:", None if resumo is None else resumo.get("text"))
rolar()
shot("3-2")
