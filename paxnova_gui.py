import tkinter as tk
from tkinter import scrolledtext
import threading
import os
import subprocess
from datetime import datetime
from paxnova_chat import procesar_entrada, respuesta_inicial, monitor_alertas_gui

# ───────── Config visual estilo Win XP ─────────
COLOR_BG        = "#dcdcdc"      # gris claro
COLOR_HEADER    = "#316AC5"      # azul XP
COLOR_USER      = "#0052cc"      # texto usuario
COLOR_NAOMI     = "#000000"
FONT_MAIN       = ("Tahoma", 11)

# Ruta base del proyecto
ruta_base = os.path.dirname(os.path.abspath(__file__))

# Lanzar actualizador y automejora (igual que antes)
for script in ("gestor_actualizaciones.py", "naomi_autocodigo.py"):
    try:
        subprocess.run(["python", os.path.join(ruta_base, script)], check=True)
    except Exception as e:
        print(f"⚠️ Error ejecutando {script}: {e}")

def enviar_mensaje():
    texto = entrada_usuario.get().strip()
    if not texto:
        return
    entrada_usuario.delete(0, tk.END)
    mostrar_mensaje("Tú", texto)
    estado.set("🧠 Pensando…")
    threading.Thread(target=procesar_respuesta, args=(texto,), daemon=True).start()

def procesar_respuesta(msg):
    try:
        respuesta = procesar_entrada(msg)
        mostrar_mensaje("Naomi", respuesta.strip())
        estado.set("✅ Respuesta generada")
    except Exception as e:
        mostrar_mensaje("Naomi", f"⚠️ Error: {e}")
        estado.set("⚠️ Error al generar respuesta")

def mostrar_mensaje(remitente, mensaje):
    area_texto.config(state=tk.NORMAL)
    tag = "usuario" if remitente == "Tú" else "naomi"
    alineacion = "e" if remitente == "Tú" else "w"   # derecha / izquierda
    area_texto.insert(tk.END, f"{remitente}: {mensaje}\n", (tag, alineacion))
    area_texto.config(state=tk.DISABLED)
    area_texto.yview(tk.END)

def actualizar_reloj():
    ahora = datetime.now().strftime("%H:%M:%S")
    barra_estado_clock.config(text=f"⏰ {ahora}")
    ventana.after(1000, actualizar_reloj)

def iniciar_gui():
    global ventana, entrada_usuario, area_texto, estado, barra_estado_clock

    ventana = tk.Tk()
    ventana.title("PaxNova – Naomi")
    ventana.geometry("820x560")
    ventana.configure(bg=COLOR_BG)

    # Header azul
    header = tk.Frame(ventana, bg=COLOR_HEADER, height=36)
    header.pack(fill=tk.X, side=tk.TOP)
    tk.Label(header, text="PaxNova – Naomi", bg=COLOR_HEADER,
             fg="white", font=("Tahoma", 12, "bold")).pack(pady=6)

    # Área de conversación
    area_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD,
                                           bg=COLOR_BG, fg=COLOR_NAOMI,
                                           font=FONT_MAIN, bd=0,
                                           state=tk.DISABLED)
    area_texto.tag_config("usuario", foreground=COLOR_USER)
    area_texto.tag_config("naomi", foreground=COLOR_NAOMI)
    area_texto.tag_config("e", justify="right")  # right align
    area_texto.tag_config("w", justify="left")   # left align
    area_texto.pack(padx=8, pady=6, fill=tk.BOTH, expand=True)

    # Entrada + botón
    frame_inferior = tk.Frame(ventana, bg=COLOR_BG)
    frame_inferior.pack(padx=8, pady=6, fill=tk.X)
    entrada_usuario = tk.Entry(frame_inferior, font=FONT_MAIN)
    entrada_usuario.pack(side=tk.LEFT, fill=tk.X, expand=True)
    entrada_usuario.bind("<Return>", lambda e: enviar_mensaje())
    tk.Button(frame_inferior, text="Enviar", width=10,
              command=enviar_mensaje).pack(side=tk.RIGHT, padx=6)

    # Barra de estado estilo XP
    barra_estado = tk.Frame(ventana, bg="#b0b0b0", height=22, relief="sunken", bd=1)
    barra_estado.pack(fill=tk.X, side=tk.BOTTOM)

    estado = tk.StringVar(value="Naomi lista ✅")
    tk.Label(barra_estado, textvariable=estado, bg="#b0b0b0",
             anchor="w", font=("Tahoma", 9)).pack(side=tk.LEFT, padx=6)

    barra_estado_clock = tk.Label(barra_estado, bg="#b0b0b0",
                                  anchor="e", font=("Tahoma", 9))
    barra_estado_clock.pack(side=tk.RIGHT, padx=6)

    actualizar_reloj()

    # 🔔 Hilo de alertas
    threading.Thread(target=monitor_alertas_gui,
                     args=(lambda m: mostrar_mensaje("Naomi", m),),
                     daemon=True).start()

    mostrar_mensaje("Naomi", respuesta_inicial())
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_gui()
