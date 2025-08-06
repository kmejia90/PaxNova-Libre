import os
import json
from datetime import datetime
from paxnova_chat import procesar_entrada

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MEMORIA_VIVA_PATH = os.path.join(BASE_PATH, "memoria_viva.json")
ACTUALIZACIONES_PATH = os.path.join(BASE_PATH, "autoactualizacion", "actualizaciones")
VERSIONES_PATH = os.path.join(BASE_PATH, "autoactualizacion", "version.txt")

def obtener_version_actual(modulo):
    with open(VERSIONES_PATH, "r") as f:
        for linea in f:
            if linea.startswith(modulo):
                return float(linea.strip().split("=")[1])
    return 0.0

def leer_memoria_conversacional():
    with open(MEMORIA_VIVA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def analizar_conversaciones(entradas):
    resumen = ""
    for entrada in entradas[-100:]:  # Solo analiza las últimas 100 interacciones
        rol = entrada.get("rol", "")
        texto = entrada.get("texto", "")
        if rol == "usuario":
            resumen += f"Usuario dijo: {texto}\n"
        else:
            resumen += f"Naomi respondió: {texto}\n"
    prompt = (
        "Estas son las últimas conversaciones entre un usuario y una IA llamada Naomi. "
        "Analiza si Naomi cometió errores, dio respuestas pobres, o podría mejorar su forma de razonar. "
        "Si detectas posibles mejoras, sugiere una nueva versión del módulo 'memoria.py'. "
        "Solo responde con el nuevo código Python sugerido:"
        f"\n\n{resumen}"
    )
    return procesar_entrada(prompt)

def guardar_codigo_generado(modulo, nueva_version, codigo):
    nombre_archivo = f"{modulo}_v{nueva_version}.py"
    ruta_completa = os.path.join(ACTUALIZACIONES_PATH, nombre_archivo)
    with open(ruta_completa, "w", encoding="utf-8") as f:
        f.write(f"# Automejora generada por Naomi el {datetime.now()}\n")
        f.write(codigo)
    print(f"✅ Naomi creó: {nombre_archivo}")

def autoevaluarse():
    conversaciones = leer_memoria_conversacional()
    version_actual = obtener_version_actual("memoria")
    nueva_version = round(version_actual + 1.0, 1)
    codigo = analizar_conversaciones(conversaciones)
    if "def" in codigo and "memoria" in codigo:
        guardar_codigo_generado("memoria", nueva_version, codigo)
    else:
        print("🟡 Naomi no detectó mejoras necesarias basadas en conversaciones.")

if __name__ == "__main__":
    autoevaluarse()
