"""
Los modelos de IA que usa el bot, en UN solo lugar.

¿Por qué un archivo aparte? Porque los proveedores retiran modelos cada pocos
meses. Cuando eso pasa, la API responde con un error 404 ("not found") o 410
("gone") y el bot deja de contestar. Este repo ya lo vivió dos veces
(gemini-1.5-flash y gemini-2.0-flash). Con los nombres acá, cambiar de modelo
es cambiar una línea, no buscarla por todo el código.

Tienes dos formas de cambiar un modelo:

  1. Sin tocar código: agrega una línea a tu archivo .env, por ejemplo
         GROQ_MODEL=openai/gpt-oss-120b
  2. Cambiando el valor por defecto aquí abajo.

Para saber si los tres modelos responden, corre:  python verify_setup.py
"""
import os

from dotenv import load_dotenv

load_dotenv()  # así el .env se lee aunque este archivo se importe primero

# Si la variable no existe en el .env (o está vacía), se usa el valor de la derecha.

# Gemini (Google) — el modelo por defecto, equilibrado. Catálogo: aistudio.google.com
GEMINI_MODEL = os.getenv("GEMINI_MODEL") or "gemini-3.8-flash"

# Groq — la opción "rápido". Catálogo: console.groq.com/docs/models
GROQ_MODEL = os.getenv("GROQ_MODEL") or "openai/gpt-oss-20b"

# NVIDIA build — la opción "potente" y el último respaldo. Catálogo: build.nvidia.com
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL") or "nvidia/nemotron-3-ultra-550b-a55b"
