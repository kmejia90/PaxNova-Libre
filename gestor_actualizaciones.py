import os
import shutil

MODULO_DIR = "modulos"
ACTUAL_DIR = "."
VERSION_FILE = "version.txt"

def leer_versiones():
    path = os.path.join(ACTUAL_DIR, VERSION_FILE)
    versiones = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for linea in f:
                if "=" in linea:
                    nombre, version = linea.strip().split("=")
                    versiones[nombre] = float(version)
    return versiones

def actualizar_modulo(nombre):
    versiones = leer_versiones()
    version_actual = versiones.get(nombre, 0.0)
    max_version = version_actual
    archivo_nuevo = None

    for archivo in os.listdir(MODULO_DIR):
        if archivo.startswith(nombre) and "_v" in archivo and archivo.endswith(".py"):
            nueva_version = float(archivo.split("_v")[1].replace(".py", ""))
            print(f"Detectado archivo candidato: {archivo} -> versión {nueva_version}")
            if nueva_version > max_version:
                max_version = nueva_version
                archivo_nuevo = archivo

    if archivo_nuevo:
        print(f"📦 Actualizando {nombre} a la versión {max_version}")
        shutil.copy(os.path.join(MODULO_DIR, archivo_nuevo), os.path.join(ACTUAL_DIR, f"{nombre}.py"))

        # Actualizar version.txt
        versiones[nombre] = max_version
        with open(os.path.join(ACTUAL_DIR, VERSION_FILE), 'w') as f:
            for n, v in versiones.items():
                f.write(f"{n}={v}\n")
    else:
        print(f"✅ {nombre} ya está actualizado.")

if __name__ == "__main__":
    actualizar_modulo("memoria")
    actualizar_modulo("gui")
    actualizar_modulo("razonamiento")
