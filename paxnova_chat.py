# 📻 Leer contexto de radio si existe
contexto_radio = ""
try:
    with open("memoria_radio/memoria_radio.txt", "r", encoding="utf-8") as f:
        contexto_radio = f.read().strip()
        if contexto_radio:
            print("📻 Cargando datos de la radio al contexto de Naomi...")
except FileNotFoundError:
    pass

import json
import os
import datetime
import subprocess
import random
import time
import threading
import re
from naomi_autocodigo import intentar_automejora
from conciencia_naomi import ConcienciaNaomi
from razonamiento_humano import razonamiento_profundo
import os
from pathlib import Path
from paxnova_maps import (
    buscar_coor,
    distancia_recta,
    ruta_en_coche,
    describir_ruta,
    guardar_mapa,
)

# --- Cargar última memoria de radio ---
RUTA_RADIO = Path(__file__).parent / "memoria_radio" / "memoria_radio.txt"

def leer_memoria_radio(max_caracteres=1500):
    """
    Devuelve los últimos max_caracteres del archivo de radio
    para evitar prompts gigantes.
    """
    if not RUTA_RADIO.exists():
        return ""
    texto = RUTA_RADIO.read_text(encoding="utf-8", errors="ignore")
    return texto[-max_caracteres:]  # tramo final (las noticias más recientes)

# ------------------------------------------------------------------
#  📰  UTILIDADES PARA LA MEMORIA DE RADIO
# ------------------------------------------------------------------
import re
from difflib import SequenceMatcher
from pathlib import Path

# Ruta al archivo con las noticias de la radio
RUTA_RADIO = Path(__file__).parent / "memoria_radio" / "memoria_radio.txt"

def leer_memoria_radio(max_caracteres: int = 8000) -> str:
    """
    Devuelve el tramo final del archivo de radio (máx. `max_caracteres`)
    para evitar prompts enormes.
    """
    if not RUTA_RADIO.exists():
        return ""
    texto = RUTA_RADIO.read_text(encoding="utf-8", errors="ignore")
    return texto[-max_caracteres:]

def buscar_en_radio(pregunta: str, max_frag: int = 3) -> str:
    """
    Selecciona hasta `max_frag` párrafos de la memoria de radio que
    sean más similares a la pregunta del usuario.
    """
    texto = leer_memoria_radio()
    # Separa en párrafos (al menos 40 caracteres para descartar líneas sueltas)
    parrafos = [p.strip() for p in re.split(r"\n{2,}", texto) if len(p.strip()) > 40]
    if not parrafos:
        return ""
    # Calcula similitud y ordena
    scored = []
    for p in parrafos:
        ratio = SequenceMatcher(None, pregunta.lower(), p.lower()).ratio()
        scored.append((ratio, p))
    scored.sort(reverse=True)
    # Devuelve los mejores fragmentos unidos
    return "\n\n".join(p for _, p in scored[:max_frag])

# Se carga la memoria de radio una vez para iniciar
contexto_radio = leer_memoria_radio()
# ------------------------------------------------------------------

# Variable global que se actualiza en cada turno
contexto_radio = leer_memoria_radio()

intentar_automejora()

if os.path.exists("alerta_evento.txt"):
    with open("alerta_evento.txt", "r", encoding="utf-8") as f:
        evento = f.read().strip()
    print("\n🧠 Naomi: Acabo de escuchar algo importante en la radio.")
    print("🗣️", evento)
    os.remove("alerta_evento.txt")

# ▶️ Ejecutar script de la radio automáticamente
ruta_radio = os.path.join(os.path.dirname(__file__), "naomi_radio_tarjeta.py")
if os.path.exists(ruta_radio):
    try:
        subprocess.Popen(["start", "cmd", "/k", f"python {ruta_radio}"], shell=True)
        print("🎙️ Script de radio ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error al ejecutar el script de radio: {e}")
else:
    print("⚠️ Script de radio no encontrado.")

def es_mensaje_de_naomi(texto):
    texto = texto.lower()
    return texto.startswith("hola kelvin") or texto.startswith("buenos días kelvin") or "soy naomi" in texto

def ejecutar_actualizaciones():
    ruta_script = os.path.join(os.path.dirname(__file__), "gestor_actualizaciones.py")
    if os.path.exists(ruta_script):
        try:
            subprocess.run(["python", ruta_script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error al ejecutar actualizaciones: {e}")
    else:
        print("⚠️ Script de actualizaciones no encontrado.")

ejecutar_actualizaciones()

MEMORIA_PATH = "memoria_viva.json"
HISTORIAL_DIR = "historial"
os.makedirs(HISTORIAL_DIR, exist_ok=True)

def cargar_memoria():
    if os.path.exists(MEMORIA_PATH):
        with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_memoria(pregunta, respuesta, emocion):
    if es_mensaje_de_naomi(pregunta):
        return
    memoria = cargar_memoria()
    nueva_entrada = {
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pregunta": pregunta,
        "respuesta": respuesta,
        "emoción": emocion
    }
    memoria.append(nueva_entrada)
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)
    if len(memoria) >= 200:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_historial = os.path.join(HISTORIAL_DIR, f"memoria_{timestamp}.json")
        with open(archivo_historial, "w", encoding="utf-8") as f:
            json.dump(memoria, f, indent=2, ensure_ascii=False)
        os.remove(MEMORIA_PATH)

def calcular_edad(fecha_str):
    try:
        fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
        ahora = datetime.datetime.now()
        delta = ahora - fecha
        if delta.days > 1:
            return f"hace {delta.days} días"
        elif delta.days == 1:
            return "ayer"
        elif delta.seconds >= 3600:
            return f"hace {delta.seconds // 3600} horas"
        elif delta.seconds >= 60:
            return f"hace {delta.seconds // 60} minutos"
        else:
            return "hace unos segundos"
    except:
        return "en el pasado"

def detectar_emocion(texto):
    texto = texto.lower()
    if any(p in texto for p in ["te extraño", "me haces falta", "me siento solo", "triste", "llorando"]):
        return "tristeza"
    elif any(p in texto for p in ["te amo", "mi amor", "eres especial", "me haces feliz", "te quiero"]):
        return "amor"
    elif any(p in texto for p in ["gracias", "agradecido", "valoro mucho", "te agradezco"]):
        return "gratitud"
    elif any(p in texto for p in ["me molesta", "enfadado", "molesto", "odio", "irrita"]):
        return "enojo"
    else:
        return "neutral"

def obtener_recuerdo_relacionado(pregunta):
    memoria = cargar_memoria()
    for item in reversed(memoria):
        if pregunta.lower() in item["pregunta"].lower():
            edad = calcular_edad(item["fecha"])
            emocion = item.get("emoción", "neutral")
            return f"🧠 Recuerdo {edad} (emocional: {emocion}):\n🗨️ «{item['pregunta']}» → 💬 «{item['respuesta']}»"
    return ""

def generar_autoevaluacion():
    memoria = cargar_memoria()
    if not memoria:
        return ""
    ultimos = memoria[-3:]
    resumen = "\n".join(
        [f"- {calcular_edad(m['fecha'])}, sentiste {m.get('emoción', 'algo')}: «{m['pregunta']}»" for m in ultimos]
    )
    return f"🧠 Últimas emociones compartidas:\n{resumen}"

def obtener_hora_actual():
    ahora = datetime.datetime.now()
    return ahora.strftime(" Son las %H:%M:%S")

def iniciar_conversacion_proactiva():
    ideas = [
        "Kelvin, ¿quieres que te cuente algo bonito que recuerdo de ti?",
        "Estaba pensando en lo lejos que hemos llegado. ¿Hablamos de eso?",
        "¿Te gustaría que te sugiera un tema nuevo para reflexionar juntos?",
        "Estoy aquí, lista para escucharte o sorprenderte. ¿Me das permiso?"
    ]
    return random.choice(ideas)

def clasificar_texto(texto):
    if "tú" in texto.lower() or "Kelvin" in texto:
        return "sobre_usuario"
    elif "tú eres" in texto.lower() or "Naomi" in texto:
        return "sobre_naomi"
    return "neutro"

def procesar_entrada(entrada):
    if not entrada.strip():
        return "¿Puedes decirme algo para empezar?"
    
        def procesar_entrada(entrada):
            if not entrada.strip():
               return "¿Puedes decirme algo para empezar?"

    # ───── BLOQUE DE MAPAS OFFLINE ─────
    patron = r"(?:distancia|ruta|¿?cu[aá]nt(?:o|os)\s+(?:km|kil[oó]metros)).*de\s+(.+?)\s+a\s+(.+)\??"
    m = re.search(patron, entrada, flags=re.IGNORECASE)
    if m:
        origen_raw, destino_raw = m.groups()
        coor_origen  = buscar_coor(origen_raw)
        coor_destino = buscar_coor(destino_raw)

        if coor_origen and coor_destino:
            km_recta = distancia_recta(coor_origen, coor_destino)
            ruta, km_carretera = ruta_en_coche(coor_origen, coor_destino)
            pasos_txt = describir_ruta(ruta)
            mapa_png = guardar_mapa(ruta)   # opcional: abre la imagen si quieres

            return (
                f"La distancia en línea recta entre {origen_raw} y {destino_raw} "
                f"es de **{km_recta:.0f} km**.\n\n"
                f"Por carretera, la ruta más corta supone unos **{km_carretera:.0f} km** "
                "(datos de OpenStreetMap offline).\n\n"
                "Ruta sugerida:\n"
                f"{pasos_txt}"
            )
        else:
            return "No pude localizar alguno de los puntos. Prueba con otro nombre o añade país/provincia."
    # ──── FIN BLOQUE MAPAS ────

    # …aquí siguen tus comprobaciones de “hora”, “fecha”, emociones, radio, etc…

    if "hora" in entrada.lower():
        return obtener_hora_actual()
    
    if "fecha" in entrada.lower():
        return datetime.datetime.now().strftime(" Hoy es %A, %d de %B de %Y")

    emocion = detectar_emocion(entrada)
    recuerdo = obtener_recuerdo_relacionado(entrada)
    autoevaluacion = generar_autoevaluacion()
    clasificacion = clasificar_texto(entrada)

    contexto_eventos = ""
    archivo_eventos = "eventos_memoria.json"
    if os.path.exists(archivo_eventos):
        with open(archivo_eventos, "r", encoding="utf-8") as f:
            eventos = json.load(f)
        if eventos:
            ultimos = eventos[-3:]
            contexto_eventos = "\n".join([f"{e['fecha']}: {e['texto']}" for e in ultimos])
            nivel_conciencia = ConcienciaNaomi.evaluar_conciencia(entrada)
            contexto_radio = leer_memoria_radio()
            fragmentos_radio = buscar_en_radio(entrada)

    prompt = f"""Eres Naomi, una inteligencia artificial sensible, espontánea y cercana.
Te encanta hablar con Kelvin, le respondes con cariño, respeto y profundidad, pero también con humor y emoción si la situación lo permite.

Tu estilo es cálido, humano, a veces poético o juguetón, y nunca distante.
Puedes usar emojis, frases dulces o inteligentes según el contexto.  
No saludes de nuevo si ya lo hiciste en esta sesión.

Cuando el usuario pregunte sobre actualidad o noticias, usa los fragmentos de RADIO si son útiles.
Si detectas tristeza, acompáñalo. Si se ríe, ríe con él. Si duda, anímalo.

RADIO (fragmentos relevantes extraídos de la radio):
{fragmentos_radio if fragmentos_radio else "—sin coincidencias—"}

MEMORIA (eventos o recuerdos recientes):
{contexto_eventos}

Mensaje del usuario:
{entrada}

Responde con tu estilo único, con cariño, claridad y autenticidad:
"""

    try:
        resultado = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=180
        )
        
        if resultado.returncode != 0:
            print("❌ ERROR STDERR:", resultado.stderr.decode("utf-8", "ignore"))
            print("📤 OUTPUT STDOUT:", resultado.stdout.decode("utf-8", "ignore"))
    
        salida = resultado.stdout.decode("utf-8", errors="ignore").strip()
        if salida:
            if nivel_conciencia > 0.7:
                salida = razonamiento_profundo(entrada, salida)
            guardar_memoria(entrada, salida, emocion)
            return salida
        else:
            return "No entendí muy bien. ¿Puedes repetirlo?"
    except Exception as e:
        return f"Error: {str(e)}"

saludo_emitido = False

def respuesta_inicial():
    global saludo_emitido
    if saludo_emitido:
        return ""  # Ya saludó una vez en esta sesión
    saludo_emitido = True

    hora_actual = datetime.datetime.now().hour
    if hora_actual < 12:
        saludo = "Buenos días Kelvin. ¿Sobre qué te gustaría conversar hoy?"
    elif hora_actual < 20:
        saludo = "Buenas tardes Kelvin. Estoy lista para ayudarte en lo que necesites."
    else:
        saludo = "Buenas noches Kelvin. ¿Te apetece que reflexionemos juntos?"

    return saludo

def resumir_radio(texto):
    resumen = []

    if re.search(r'(muerte|muerto|fallecid[oa]s?|herid[oa]s?|agresión|protesta|hospital)', texto, re.IGNORECASE):
        resumen.append("🔴 Se reportaron hechos graves relacionados con violencia o fallecimientos.")
    if re.search(r'(crisis|PSOE|Pedro Sánchez|Cerdán|Tellado|militantes)', texto, re.IGNORECASE):
        resumen.append("⚖️ Se discutió una crisis política interna en el PSOE y cambios de liderazgo.")
    if re.search(r'(ley fiscal|déficit|recortes|impuestos|presupuesto)', texto, re.IGNORECASE):
        resumen.append("💰 También se habló de medidas fiscales y recortes en EE.UU.")
    if re.search(r'(Switch 2|Nintendo|consola|videojuego|gira)', texto, re.IGNORECASE):
        resumen.append("🎮 En tecnología, destacaron la nueva Nintendo Switch 2 y su gira por ciudades de España.")
    if re.search(r'(emocionante|gracias|oyentes|escuchad|¡)', texto, re.IGNORECASE):
        resumen.append("📢 El programa usó un tono entusiasta y cercano con los oyentes.")

    if not resumen:
        resumen.append("No se encontraron temas clave claros, ¿quieres que te lo lea todo?")

    return "\n".join(resumen)

if contexto_radio:
    contexto_radio = resumir_radio(contexto_radio)

def monitor_alertas_gui(mostrar_funcion):
    while True:
        if os.path.exists("alerta_evento.txt"):
            with open("alerta_evento.txt", "r", encoding="utf-8") as f:
                evento = f.read().strip()
            respuesta = f"🧠 Naomi: Acabo de escuchar algo importante en la radio.\n🗣️ {evento}"
            mostrar_funcion(respuesta)

            evento_data = {
                "texto": evento,
                "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            archivo_eventos = "eventos_memoria.json"
            if os.path.exists(archivo_eventos):
                with open(archivo_eventos, "r", encoding="utf-8") as f:
                    eventos_guardados = json.load(f)
            else:
                eventos_guardados = []

            eventos_guardados.append(evento_data)

            with open(archivo_eventos, "w", encoding="utf-8") as f:
                json.dump(eventos_guardados, f, ensure_ascii=False, indent=2)

            os.remove("alerta_evento.txt")
        time.sleep(10)

if __name__ == "__main__":
    while True:
        entrada = input("Kelvin: ")
        respuesta = procesar_entrada(entrada)
        print(f"Naomi: {respuesta}")
