import requests
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import os

# URL del streaming de la radio (puedes cambiarla)
RADIO_URL = "https://stream.live.vc.bbcmedia.co.uk/bbc_world_service"  # ejemplo: BBC

def descargar_fragmento(nombre="radio_chunk.mp3", segundos=10):
    response = requests.get(RADIO_URL, stream=True)
    with open(nombre, "wb") as f:
        for i, chunk in enumerate(response.iter_content(chunk_size=1024)):
            if i > (44100 * segundos / 1024):  # aproximadamente 10 segundos
                break
            f.write(chunk)
    return nombre

def transcribir_audio(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export("temp.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            texto = recognizer.recognize_google(audio_data, language="es-ES")
            print("🎙️ Transcripción:", texto)
        except sr.UnknownValueError:
            print("⚠️ No se entendió el audio.")
        except sr.RequestError as e:
            print(f"❌ Error de reconocimiento: {e}")

if __name__ == "__main__":
    nombre_archivo = descargar_fragmento()
    transcribir_audio(nombre_archivo)
    os.remove("temp.wav")
    os.remove(nombre_archivo)
