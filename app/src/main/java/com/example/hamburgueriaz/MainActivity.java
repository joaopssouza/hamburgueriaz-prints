package com.example.hamburgueriaz;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    private static final double PRECO_BASE = 20.0;
    private static final double PRECO_BACON = 2.0;
    private static final double PRECO_QUEIJO = 2.0;
    private static final double PRECO_ONION_RINGS = 3.0;

    private int quantidade = 0;

    private EditText editNome;
    private CheckBox checkBacon;
    private CheckBox checkQueijo;
    private CheckBox checkOnion;
    private TextView txtQuantidade;
    private TextView txtResumo;
    private TextView txtTotal;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        editNome = findViewById(R.id.editNome);
        checkBacon = findViewById(R.id.checkBacon);
        checkQueijo = findViewById(R.id.checkQueijo);
        checkOnion = findViewById(R.id.checkOnion);
        txtQuantidade = findViewById(R.id.txtQuantidade);
        txtResumo = findViewById(R.id.txtResumo);
        txtTotal = findViewById(R.id.txtTotal);
    }

    public void somar(View view) {
        quantidade++;
        txtQuantidade.setText(String.valueOf(quantidade));
    }

    public void subtrair(View view) {
        if (quantidade > 0) {
            quantidade--;
        }
        txtQuantidade.setText(String.valueOf(quantidade));
    }

    private double calcularPreco() {
        double precoUnitario = PRECO_BASE;
        if (checkBacon.isChecked()) {
            precoUnitario += PRECO_BACON;
        }
        if (checkQueijo.isChecked()) {
            precoUnitario += PRECO_QUEIJO;
        }
        if (checkOnion.isChecked()) {
            precoUnitario += PRECO_ONION_RINGS;
        }
        return precoUnitario * quantidade;
    }

    private String simNao(boolean marcado) {
        return marcado ? "Sim" : "Não";
    }

    public void enviarPedido(View view) {
        String nome = editNome.getText().toString().trim();
        if (nome.isEmpty()) {
            Toast.makeText(this, "Informe o nome do cliente", Toast.LENGTH_SHORT).show();
            return;
        }
        if (quantidade == 0) {
            Toast.makeText(this, "Escolha ao menos 1 hambúrguer", Toast.LENGTH_SHORT).show();
            return;
        }

        double total = calcularPreco();
        String precoFormatado = String.format(Locale.forLanguageTag("pt-BR"), "%.2f", total);

        String resumo = nome + "\n"
                + "Tem Bacon? " + simNao(checkBacon.isChecked()) + "\n"
                + "Tem Queijo? " + simNao(checkQueijo.isChecked()) + "\n"
                + "Tem Onion Rings? " + simNao(checkOnion.isChecked()) + "\n"
                + "Quantidade: " + quantidade + "\n"
                + "Preço final: R$ " + precoFormatado;

        txtResumo.setText(resumo);
        txtTotal.setText("R$ " + precoFormatado);

        Intent intent = new Intent(Intent.ACTION_SENDTO);
        intent.setData(Uri.parse("mailto:"));
        intent.putExtra(Intent.EXTRA_SUBJECT, "Pedido de " + nome);
        intent.putExtra(Intent.EXTRA_TEXT, resumo);

        try {
            startActivity(intent);
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "Nenhum aplicativo de e-mail encontrado", Toast.LENGTH_LONG).show();
        }
    }
}
