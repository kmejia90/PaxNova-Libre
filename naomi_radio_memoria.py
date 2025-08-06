import requests
import time
import json
import os
import tempfile
import whisper
from pydub import AudioSegment

# 📻 URL de la emisora en vivo (modifícala si quieres otra)
RADIO_URL = "https://radio5.rtveradio.cires21.com/radio5_hc.mp3"


# 🧠 Archivo de memoria persistente
MEMORIA_PATH = "noticias_radio.json"

# ⏱️ Tiempo de escucha en segundos
SEGUNDOS_AUDIO = 8

# 🕰️ Intervalo entre escuchas
INTERVALO_ANALISIS = 15

# 🎤 Modelo Whisper para transcripción offline
modelo = whisper.load_model("base")  # Usa "tiny" si necesitas menos consumo

def escuchar_radio_y_guardar():
    try:
        print("🔊 Escuchando radio...")

        with requests.get(RADIO_URL, stream=True) as r:
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                for i, chunk in enumerate(r.iter_content(chunk_size=1024)):
                    if i > (SEGUNDOS_AUDIO * 32):  # Aprox 32KB/s
                        break
                    f.write(chunk)
                ruta_mp3 = f.name

        ruta_wav = ruta_mp3.replace(".mp3", ".wav")
        AudioSegment.from_mp3(ruta_mp3).export(ruta_wav, format="wav")

        print("🎙️ Transcribiendo audio...")
        resultado = modelo.transcribe(ruta_wav, language="es")
        texto = resultado["text"].strip()

        if texto:
            print("🧠 Transcripción:", texto)
            guardar_memoria(texto)
        else:
            print("❌ No se pudo transcribir texto.")

        os.remove(ruta_mp3)
        os.remove(ruta_wav)

    except Exception as e:
        print(f"⚠️ Error: {e}")

def guardar_memoria(texto):
    if not os.path.exists(MEMORIA_PATH):
        with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
        datos = json.load(f)

    datos.append({"texto": texto, "timestamp": time.time()})

    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("🔁 Naomi está escuchando radio...")
    while True:
        escuchar_radio_y_guardar()
        time.sleep(INTERVALO_ANALISIS)
