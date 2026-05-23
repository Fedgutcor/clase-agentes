# Construye tu primer agente IA

![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

> **En esta clase construyes un bot de Telegram con memoria, herramientas propias, y dos modelos de IA que se respaldan entre sí.**

---

## Índice

1. [Qué vas a construir](#qué-vas-a-construir)
2. [Herramientas que vas a usar](#herramientas-que-vas-a-usar)
3. [Cómo abrir la terminal](#cómo-abrir-la-terminal)
4. [Cómo descargar el proyecto](#cómo-descargar-el-proyecto)
5. [Setup paso a paso](#setup-paso-a-paso)
6. [Qué hace cada parte del proyecto](#qué-hace-cada-parte-del-proyecto)
7. [Cómo funciona por dentro](#cómo-funciona-por-dentro)
8. [Comandos del bot](#comandos-del-bot)
9. [Conectar herramientas extra](#conectar-herramientas-extra)
10. [Troubleshooting](#troubleshooting)

---

## Qué vas a construir

Un bot de Telegram que:

- Habla con dos modelos de IA (Gemini y Groq) y **elige cuál usar** según el mensaje
- **Recuerda información** sobre cada usuario entre conversaciones
- Tiene **herramientas propias**: calculadora, notas, y 10 extras que puedes activar

No es un chatbot de juguete — tiene la misma arquitectura base de los agentes de producción.

---

## Herramientas que vas a usar

Antes de instalar nada, asegúrate de tener esto:

| Herramienta | Para qué sirve | Cómo saber si la tienes |
|-------------|---------------|------------------------|
| **Python 3.10+** | El lenguaje en que está escrito el bot | En la terminal: `python --version` |
| **Git** | Para descargar el proyecto desde GitHub | En la terminal: `git --version` |

Si alguno de esos comandos dice "command not found":
- **Python**: descárgalo en [python.org/downloads](https://www.python.org/downloads/) — instala la versión más reciente
- **Git**: descárgalo en [git-scm.com/downloads](https://git-scm.com/downloads)

---

## Cómo abrir la terminal

La **terminal** es la ventana negra donde escribes comandos de texto. Todo lo que hagas en esta guía pasa ahí.

### En Mac

1. Presiona `Cmd + Espacio` para abrir Spotlight
2. Escribe `Terminal`
3. Presiona Enter

Verás una ventana con texto. Eso es la terminal. Está lista para recibir comandos.

### En Windows

1. Presiona `Win + R`
2. Escribe `cmd`
3. Presiona Enter

> **Recomendado en Windows**: usa **PowerShell** en lugar de cmd. Para abrirlo: click derecho en el botón de Inicio → "Windows PowerShell".

### Cómo usar la terminal

- Escribes un comando y presionas **Enter** para ejecutarlo
- Solo puedes ejecutar un comando a la vez — espera a que termine antes del siguiente
- Si ves un error en rojo, es normal — el troubleshooting al final de esta guía cubre los más comunes

---

## Cómo descargar el proyecto

GitHub es donde está guardado el código. `git clone` lo descarga a tu computadora.

**Abre la terminal** y ejecuta estos dos comandos, uno por uno:

```bash
git clone https://github.com/Fedgutcor/clase-agentes
```

Esto descarga el proyecto y crea una carpeta llamada `clase-agentes` donde estés parado.

```bash
cd clase-agentes
```

`cd` significa "entrar a una carpeta" (*change directory*). Después de esto, todos los comandos que ejecutes se aplican dentro del proyecto.

> **¿Dónde quedó la carpeta?**
> - **Mac**: en tu carpeta de usuario (`/Users/tu-nombre/clase-agentes`). Puedes abrirla desde Finder.
> - **Windows**: en `C:\Users\tu-nombre\clase-agentes`. Puedes abrirla desde el Explorador de archivos.

---

## Setup paso a paso

### Paso 1 — Instala las dependencias

Asegúrate de estar dentro de la carpeta del proyecto (si acabas de clonar, ya lo estás).

Ejecuta en la terminal:

```bash
python setup.py
```

Este script hace todo por ti:
- Crea un **entorno virtual** — una caja aislada con las librerías del proyecto, para no mezclarlas con el resto de tu computadora
- Instala las librerías necesarias
- Te pregunta tus API keys y las guarda de forma segura en un archivo `.env`

El script te explica cada key mientras lo corres. Si prefieres conseguirlas antes:

| Key | Dónde obtenerla | Costo |
|-----|-----------------|-------|
| `TELEGRAM_TOKEN` | Habla con [@BotFather](https://t.me/BotFather) en Telegram, escribe `/newbot` y sigue las instrucciones | Gratis |
| `GEMINI_API_KEY` | Entra a [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) y haz click en "Create API key" | Gratis |
| `GROQ_API_KEY` | Entra a [console.groq.com/keys](https://console.groq.com/keys), crea cuenta y haz click en "Create API Key" | Gratis |

### Paso 2 — Activa el entorno virtual

Cada vez que vayas a correr el bot, primero activa el entorno virtual.  
El comando es diferente según tu sistema:

**Mac / Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

Sabrás que funcionó porque aparecerá `(venv)` al inicio de la línea en tu terminal, así:

```
(venv) nombre-de-tu-carpeta $
```

> Si cierras la terminal y vuelves a abrirla, tienes que volver a activar el entorno virtual. Es normal.

### Paso 3 — Verifica que todo esté bien (opcional)

```bash
python verify_setup.py
```

Esto comprueba que las API keys están bien configuradas antes de arrancar. Si algo falla, te dice exactamente qué.

### Paso 4 — Arranca el bot

```bash
python app.py
```

Cuando veas este banner en la terminal, el bot está corriendo:

```
██████╗  ██████╗ ████████╗
...
  🤖  AGENTE IA — ONLINE
  Escuchando mensajes...
```

Ahora abre Telegram, busca el bot que creaste con BotFather, y empieza a chatear.

> **Para detener el bot**: vuelve a la terminal y presiona `Ctrl + C`.

---

## Qué hace cada parte del proyecto

```
clase-agentes/
│
├── app.py              ← el cerebro del bot — aquí empieza y termina todo
├── memory.py           ← cómo el bot guarda y recuerda datos de cada usuario
├── setup.py            ← instalación guiada (solo se corre una vez)
├── verify_setup.py     ← verifica que el setup esté correcto
│
├── prompts/
│   ├── system.txt      ← la personalidad del agente: qué le dijiste que ES
│   └── personality.txt ← instrucciones adicionales de comportamiento
│
├── tools/
│   ├── calculator.py   ← herramienta: hace cuentas sin pedírselas a la IA
│   ├── notes.py        ← herramienta: guarda y lista notas por usuario
│   └── extras/         ← 10 herramientas opcionales listas para activar
│
├── memory/
│   └── users/          ← un archivo .json por usuario (se crea solo al correr)
│
├── requirements.txt    ← lista de librerías Python que necesita el proyecto
├── .env.example        ← plantilla del archivo de configuración (sin datos reales)
└── .env                ← tus API keys reales (nunca se sube a GitHub)
```

**Tres conceptos que aparecen en todo el código:**

**Tool** — Una función Python que el bot puede ejecutar directamente, sin pasar por la IA.  
Ejemplo: cuando escribes `calcula 45 * 12`, el bot llama a `calculator.py` y te devuelve el resultado. La IA no interviene.

**Memoria** — Cada usuario tiene un archivo `.json` en `memory/users/`. Antes de responder, el bot lo lee e inyecta esa información en el prompt. Así "recuerda" cosas entre conversaciones.

**Router** — La función `choose_model()` en `app.py` lee el mensaje y decide si mandar la pregunta a Gemini o a Groq. Si Gemini falla, cae automáticamente a Groq.

---

## Cómo funciona por dentro

```
┌──────────────────────────────────────────────────────┐
│  TELEGRAM  — el canal por donde llega el mensaje     │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│  handle_message()  — en app.py                       │
│  Lee el mensaje y decide qué hacer con él            │
└──────┬───────────────────────────┬───────────────────┘
       │                           │
       ▼                           ▼
┌──────────────┐          ┌────────────────────┐
│  TOOLS       │          │  ROUTER            │
│  (primero)   │          │  choose_model()    │
│              │          └────────┬───────────┘
│ "calcula…"  ─┼─▶ calculator.py  │
│ "guarda…"   ─┼─▶ notes.py       ├─ "rápido/corto" ──▶ GROQ (Llama 3.1)
│ "recuerda…" ─┼─▶ memory.py      └─ (por defecto) ───▶ GEMINI (Flash 2.0)
└──────────────┘                                             │
                                                             │ si Gemini falla
                                                             ▼
                                                      GROQ como respaldo
                                                      + aviso [fallback]
       │
       ▼
┌──────────────────────┐
│  MEMORIA             │
│  memory/users/       │
│  {user_id}.json      │
│  → hechos del usuario│
│    se inyectan en    │
│    el prompt de la IA│
└──────────────────────┘
```

**En palabras**: el bot recibe un mensaje → revisa si es una tool (calculadora, notas) → si no lo es, consulta la memoria del usuario → elige el modelo de IA → envía la respuesta.

---

## Comandos del bot

| Mensaje | Qué hace | Archivo que lo maneja |
|---------|----------|-----------------------|
| Cualquier texto | Responde con Gemini (o Groq si falla) | `app.py` → `ask_ai()` |
| `rápido qué es un agente` | Fuerza Groq — más veloz para respuestas cortas | `app.py` → `choose_model()` |
| `calcula 45 * 12` | Calculadora integrada | `tools/calculator.py` |
| `guarda nota comprar leche` | Guarda una nota tuya | `tools/notes.py` |
| `mis notas` | Lista todas tus notas | `tools/notes.py` |
| `recuerda que estudio diseño` | Guarda un hecho en tu perfil | `memory.py` |

---

## Conectar herramientas extra

Hay 10 herramientas en `tools/extras/` listas para activar. No requieren APIs adicionales (salvo las que ya tienes).

| Archivo | Qué hace | Comando de ejemplo |
|---------|----------|--------------------|
| `weather.py` | Clima en tiempo real | `clima en Bogotá` |
| `translator.py` | Traduce texto usando Groq | `traduce al inglés: hola mundo` |
| `summarizer.py` | Resume en 3 puntos usando Groq | `resume: [texto largo]` |
| `reminder.py` | Recordatorio con temporizador | `recuérdame en 10 minutos: llamar al médico` |
| `web_search.py` | Búsqueda en DuckDuckGo | `busca: noticias de IA hoy` |
| `qr_generator.py` | Genera un código QR como imagen | `genera qr: https://google.com` |
| `currency.py` | Convierte monedas | `convierte 100 USD a EUR` |
| `joke.py` | Chiste aleatorio | `cuéntame un chiste` |
| `pomodoro.py` | Temporizador Pomodoro | `pomodoro 25` |
| `text_stats.py` | Estadísticas de un texto | `analiza texto: [tu texto]` |

### Cómo activar una tool extra — ejemplo con clima

Abres `app.py` en un editor de texto (puedes usar VS Code, o simplemente el Bloc de notas).

**1.** Busca la sección de imports al inicio del archivo (las líneas que dicen `from ... import ...`).  
Agrega esta línea al final de ese bloque:

```python
from tools.extras.weather import get_weather
```

**2.** Busca la función `handle_message` en el mismo archivo.  
Antes de la línea que dice `user_context = mem.get_context(user_id)`, agrega:

```python
if message.lower().startswith("clima en "):
    city = message[9:]                                # toma todo lo que viene después de "clima en "
    await update.message.reply_text(get_weather(city))
    return                                            # sale de la función sin llamar a la IA
```

**3.** Guarda el archivo.

**4.** En la terminal, detén el bot (`Ctrl + C`) y vuelve a iniciarlo:

```bash
python app.py
```

**5.** Escribe `clima en Medellín` en Telegram. Listo.

> `reminder.py` y `pomodoro.py` necesitan un paso extra — hay un ejemplo comentado dentro de cada archivo.

---

## Troubleshooting

**No reconoce el comando `python`**  
En algunos sistemas se llama `python3`. Prueba:
```bash
python3 setup.py
python3 app.py
```

**El bot no responde y veo `quota` en el error**  
Gemini tiene un límite de uso por minuto en la cuenta gratuita. Espera 30 segundos e intenta de nuevo.

**El bot responde con `[fallback groq]`**  
Gemini alcanzó su cuota. El bot sigue funcionando con Groq — espera 1 minuto y Gemini vuelve.

**`Conflict: terminated by other getUpdates request`**  
Hay dos instancias del bot corriendo al mismo tiempo. Ciérralas todas y reinicia:

```bash
# Mac / Linux — en la terminal:
pkill -9 -f python
cd ~/clase-agentes
source venv/bin/activate
python app.py

# Windows — en PowerShell:
taskkill /F /IM python.exe
cd $env:USERPROFILE\clase-agentes
venv\Scripts\activate
python app.py
```

**`AttributeError` en `_Updater` o `TypeError: proxies`**  
Versión de librería incompatible. En la terminal (con el entorno activado):
```bash
pip install "python-telegram-bot==21.9" "groq>=1.2.0"
```

**`404 models/gemini-1.5-flash is not found`**  
Estás usando una versión antigua de `app.py`. Descarga la versión actualizada del repo:
```bash
git pull
```

**No veo el archivo `.env` en el Explorador / Finder**  
Los archivos que empiezan con `.` están ocultos por defecto. Ábrelo desde la terminal:
```bash
# Mac:
open -e .env

# Windows:
notepad .env
```

**Olvidé activar el entorno virtual**  
Si ves errores de "módulo no encontrado", probablemente falta activar el entorno. Vuelve al [Paso 2](#paso-2--activa-el-entorno-virtual).

---

> Versión en inglés: [README.en.md](README.en.md)

---

MIT License · Federico Gutiérrez
