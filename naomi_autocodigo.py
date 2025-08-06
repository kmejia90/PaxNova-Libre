import os
import shutil
from datetime import datetime

VERSIONES_PATH = "version.txt"
HISTORIAL_DIR = "historial"

def obtener_version_actual(nombre_modulo):
    if not os.path.exists(VERSIONES_PATH):
        return "0.0"
    with open(VERSIONES_PATH, "r") as f:
        for linea in f:
            if linea.startswith(nombre_modulo):
                partes = linea.strip().split(":")
                if len(partes) > 1:
                    return partes[1]
    return "0.0"

def actualizar_version(nombre_modulo, nueva_version):
    lineas = []
    encontrado = False
    if os.path.exists(VERSIONES_PATH):
        with open(VERSIONES_PATH, "r") as f:
            lineas = f.readlines()
        for i, linea in enumerate(lineas):
            if linea.startswith(nombre_modulo):
                lineas[i] = f"{nombre_modulo}:{nueva_version}\n"
                encontrado = True
                break
    if not encontrado:
        lineas.append(f"{nombre_modulo}:{nueva_version}\n")
    with open(VERSIONES_PATH, "w") as f:
        f.writelines(lineas)

def analizar_codigo(nombre_modulo, path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            codigo = f.read()
        if "def " not in codigo:
            return "# Posible mejora: añadir funciones definidas.\n"
        if "#" not in codigo:
            return "# Posible mejora: añadir comentarios descriptivos.\n"
    except Exception as e:
        return f"# Error al leer código: {e}"
    return ""  # sin mejoras

def generar_nueva_version(nombre_modulo, path_modulo, propuesta):
    version_actual = obtener_version_actual(nombre_modulo)
    major, minor = map(int, version_actual.split("."))
    nueva_version = f"{major}.{minor + 1}"

    # Crear carpeta historial si no existe
    if not os.path.exists(HISTORIAL_DIR):
        os.makedirs(HISTORIAL_DIR)

    # Mover versión actual a historial antes de reemplazar
    nombre_archivo_actual = os.path.basename(path_modulo)
    ruta_historial = os.path.join(HISTORIAL_DIR, f"{nombre_modulo}_v{version_actual}.py")
    if os.path.exists(path_modulo):
        shutil.copy(path_modulo, ruta_historial)

    # Crear la nueva versión
    nuevo_path = f"{nombre_modulo}_v{nueva_version}.py"
    with open(nuevo_path, "w", encoding="utf-8") as f:
        f.write(f"# Generado por Naomi automáticamente el {datetime.now()}\n")
        with open(path_modulo, "r", encoding="utf-8") as original:
            f.write(original.read())
        f.write("\n\n" + propuesta)

    print(f"✅ Nueva versión generada: {nuevo_path}")
    actualizar_version(nombre_modulo, nueva_version)

def intentar_automejora():
    nombre_modulo = "memoria"
    path_modulo = "memoria.py"
    if not os.path.exists(path_modulo):
        print(f"⚠️ Módulo {path_modulo} no encontrado.")
        return

    propuesta = analizar_codigo(nombre_modulo, path_modulo)
    if propuesta:
        generar_nueva_version(nombre_modulo, path_modulo, propuesta)
    else:
        print("🧠 No se generó nueva versión: sin cambios significativos.")

if __name__ == "__main__":
    intentar_automejora()
