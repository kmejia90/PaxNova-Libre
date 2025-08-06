import sounddevice as sd
import numpy as np
import whisper
import time
import os
import json
from datetime import datetime

# ─────────── Inicializa Whisper ───────────
modelo = whisper.load_model("base")

# Carpeta y archivo de memoria
if not os.path.exists("memoria_radio"):
    os.makedirs("memoria_radio")
archivo_memoria = os.path.join("memoria_radio", "memoria_radio.txt")

# Palabras clave de alerta
PALABRAS_CLAVE = [
    "muerto", "fallecido", "explosión", "violencia", "accidente",
    "protesta", "ataque", "guerra", "bombardeo"
]

def escuchar_y_procesar():
    print("🔊 Naomi está escuchando la tarjeta de sonido…")

    while True:
        try:
            # 15 s de audio (16 kHz mono)
            duracion = 15
            fs = 16000
            audio = sd.rec(int(duracion * fs), samplerate=fs,
                           channels=1, dtype='float32')
            sd.wait()
            audio_np = np.squeeze(audio)

            # ─── Transcripción ───
            resultado = modelo.transcribe(audio_np, language="es")
            texto = resultado["text"].strip()

            # ─── Filtrar ruido / frases muy cortas ───
            if len(texto) < 15:
                time.sleep(1)
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entrada = f"[{timestamp}] {texto}"

            print(f"🧠 Naomi escuchó: {entrada}")

            # ─── Alerta de evento ───
            if any(p in texto.lower() for p in PALABRAS_CLAVE):
                with open("alerta_evento.txt", "w", encoding="utf-8") as f:
                    f.write(entrada)

                datos_evento = {
                    "texto": texto,
                    "datetime": timestamp,
                    "origen": "radio",
                    "emocion": "alerta"
                }
                with open("evento_historico.json", "a", encoding="utf-8") as fjson:
                    fjson.write(json.dumps(datos_evento, ensure_ascii=False) + "\n")

            # ─── Guardar en memoria general ───
            with open(archivo_memoria, "a", encoding="utf-8") as f:
                f.write(entrada + "\n\n")          # salto doble para separar párrafos

        except Exception as e:
            print(f"⚠️ Error: {e}")

        time.sleep(2)  # pausa entre escuchas

# Inicia la escucha
if __name__ == "__main__":
    escuchar_y_procesar()
