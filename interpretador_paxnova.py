import os
import subprocess

def leer_binario_como_hex(ruta):
    with open(ruta, "rb") as f:
        contenido = f.read()
        return contenido.hex()

def interpretar_con_ollama(prompt, modelo="mistral", timeout=300):
    try:
        resultado = subprocess.run(
            ["ollama", "run", modelo],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=timeout
        )
        salida = resultado.stdout.decode("utf-8", errors="ignore")
        error = resultado.stderr.decode("utf-8", errors="ignore")
        return salida.strip(), error.strip()
    except subprocess.TimeoutExpired:
        return "", "Error: tiempo de espera agotado (timeout)"
    except Exception as e:
        return "", f"Error: {str(e)}"

def procesar_archivo(nombre_archivo):
    print(f"\nAnalizando archivo: {nombre_archivo}\n")
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    if not os.path.isfile(ruta):
        print("Archivo no encontrado.")
        return

    hex_data = leer_binario_como_hex(ruta)
    salida, error = interpretar_con_ollama(f"Analiza este bloque: {hex_data}")

    print("\n--- RESULTADO ---")
    print("Interpretación del archivo:\n")
    print("Análisis del contenido:")
    print(salida if salida else "No se pudo generar una salida.")
    print("\nErrores (si los hubo):")
    print(error if error else "Ninguno.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        procesar_archivo(sys.argv[1])
    else:
        print("Uso: python interpretador_paxnova.py archivo.bin")

