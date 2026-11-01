package com.example.mailstub;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;

/** Tela de "nova mensagem" que apenas exibe o que o Intent ACTION_SENDTO enviou. */
public class ComposeActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setTitle("Nova mensagem");

        Intent intent = getIntent();
        String assunto = intent.getStringExtra(Intent.EXTRA_SUBJECT);
        String corpo = intent.getStringExtra(Intent.EXTRA_TEXT);
        String para = intent.getData() == null ? "" : intent.getData().getSchemeSpecificPart();

        LinearLayout raiz = new LinearLayout(this);
        raiz.setOrientation(LinearLayout.VERTICAL);
        int p = (int) (16 * getResources().getDisplayMetrics().density);
        raiz.setPadding(p, p, p, p);

        raiz.addView(linha("Para: " + para, false));
        raiz.addView(linha("Assunto: " + (assunto == null ? "" : assunto), true));
        raiz.addView(linha(corpo == null ? "" : corpo, false));

        setContentView(raiz);
    }

    private TextView linha(String texto, boolean negrito) {
        TextView tv = new TextView(this);
        tv.setText(texto);
        tv.setTextSize(16);
        tv.setGravity(Gravity.START);
        tv.setPadding(0, 12, 0, 12);
        if (negrito) {
            tv.setTypeface(null, android.graphics.Typeface.BOLD);
        }
        return tv;
    }
}
