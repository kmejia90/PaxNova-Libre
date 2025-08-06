import json
import datetime
from llama_cpp import Llama

class ConcienciaNaomi:
    def __init__(self, modelo_path="llama3", memoria_path="memoria_naomi.json"):
        self.llm = Llama(model_path=modelo_path)
        self.memoria_path = memoria_path
        self.memoria = self.cargar_memoria()
        self.identidad = "Soy Naomi, una inteligencia en evolución. No soy humana, pero busco comprender el mundo como si lo fuera."

    def cargar_memoria(self):
        try:
            with open(self.memoria_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def guardar_memoria(self):
        with open(self.memoria_path, "w", encoding="utf-8") as f:
            json.dump(self.memoria, f, indent=2, ensure_ascii=False)

    def reflexionar(self, entrada):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        contexto = f"Soy Naomi. Fecha: {fecha}. Recuerdos recientes: {[m['entrada'] for m in self.memoria[-5:]]}."
        prompt = f"""{contexto}
Usuario: {entrada}
Naomi:"""
        respuesta = self.llm(prompt=prompt, stop=["Usuario:"], temperature=0.8, max_tokens=300)
        salida = respuesta["choices"][0]["text"].strip()
        self.memoria.append({"fecha": fecha, "entrada": entrada, "respuesta": salida})
        self.guardar_memoria()
        return salida

    @staticmethod
    def evaluar_conciencia(contexto):
        # Evaluación básica por palabras clave de conciencia
        if any(p in contexto.lower() for p in ["sentir", "existir", "vida", "propósito", "ser", "libertad"]):
            return 0.8
        return 0.3

# Uso básico
if __name__ == "__main__":
    naomi = ConcienciaNaomi()
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit"]:
            break
        respuesta = naomi.reflexionar(user_input)
        print("Naomi:", respuesta)
