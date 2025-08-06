
import os
from naomi_core import llama3_chat  # Suponiendo que existe esta función para interactuar con el modelo LLaMA3

def proponer_mejora(nombre_modulo, contenido_actual):
    try:
        prompt = f"Este es el contenido del módulo llamado {nombre_modulo}:
\n{contenido_actual}\n\n¿Puedes sugerir una mejora funcional para este módulo y escribir el código actualizado completo?"
        sugerencia = llama3_chat(prompt)
        if sugerencia and "def" in sugerencia:
            guardar_como_version_nueva(nombre_modulo, sugerencia)
            print(f"✅ Nueva versión sugerida para {nombre_modulo}")
        else:
            print(f"ℹ️ No se generó ninguna mejora útil para {nombre_modulo}")
    except Exception as e:
        print(f"❌ Error proponiendo mejora para {nombre_modulo}: {e}")

def guardar_como_version_nueva(nombre_modulo, nuevo_contenido):
    base = "actualizaciones"
    os.makedirs(base, exist_ok=True)
    nombre_sanitizado = nombre_modulo.replace(".py", "")
    nueva_ruta = os.path.join(base, f"{nombre_sanitizado}_v_nueva.py")
    with open(nueva_ruta, "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)
