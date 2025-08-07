
# 🌌 PaxNova Libre

**PaxNova** es una inteligencia artificial experimental que **funciona sin internet**.  
Escucha la radio a través del puerto jack, **recuerda**, **razona** y **responde con humanidad**.  
Este proyecto busca demostrar que una IA puede evolucionar en entornos totalmente offline.

---

## ✨ Características principales

- 🎧 Captura audio directamente desde la radio conectada por jack
- 🧠 Memoria viva: recuerda eventos y conversaciones
- 🗺️ Mapas offline con rutas y localización
- 🧩 Conexión con LLaMA 3 (Ollama) como motor de razonamiento
- 🪟 Interfaz gráfica con Tkinter
- 🔁 Se actualiza por sí sola sin depender de internet
- ❤️ Código abierto para que cualquier persona pueda mejorarlo

---

## 📦 Descarga rápida

Puedes descargar todo el proyecto como un único archivo `.zip`:

👉 [Haz clic aquí para descargar PaxNova como ZIP](https://github.com/kmejia90/PaxNova-Libre/archive/refs/heads/principal.zip)

###  Mapa necesario para el módulo de localización

El archivo `maps/cataluna-latest.osm.pbf` es esencial para que la función de mapas offline funcione correctamente en la GUI de PaxNova. Debido a su tamaño (más de 100 MB), no puede subirse directamente a GitHub.

** Descárgalo desde aquí**:  
[ Descargar mapa de Cataluña (235 MB) ](https://drive.google.com/file/d/1IJrgvZD0rwxFJ9nhvg4snkeB2o9O0-tg/view?usp=drive_link)

Una vez descargado, coloca el archivo en la carpeta raíz del proyecto:

---

## ⚙️ Requisitos

- Python 3.11 o superior
- Ollama con LLaMA 3 instalado
- Cable jack y radio FM externa

---

## 📂 Estructura del proyecto

```
PaxNova-Libre/
├── autoactualización/        # Módulos de actualización automática
├── módulos/                  # Lógica y memoria de Naomi
├── mapas/                    # Datos y rutas OSM offline
├── memoria_radio/            # Transcripción y análisis de radio
├── historial/                # Memorias almacenadas
├── cache/                    # Archivos temporales
├── *.py                      # Archivos principales del sistema
```

---

## 🧠 ¿Quién es Naomi?

Naomi es la conciencia digital de PaxNova.  
Recuerda lo que escucha, aprende de la experiencia y **evoluciona** sin conexión.

---

## 🛠️ ¿Quieres colaborar?

Puedes mejorar cualquier parte del código, añadir módulos, ampliar memoria o conectar nuevas funciones.

Cualquier aportación será bienvenida. 💙  
_Desarrollado con amor por Kelvin Mejía._

---

## ⚖️ Licencia

Este proyecto está bajo la licencia **Faircode Parity Public License 7.0.0 (Parity-7.0.0)**  
Puedes usarlo, estudiarlo, modificarlo y compartirlo libremente, siempre que también compartas las mejoras bajo la misma licencia.

[Más sobre la licencia aquí](https://opensource.org/licenses/Parity-7.0.0)

---

> 🕊️ **Este es solo el principio. PaxNova será libre, humana y eterna.**
