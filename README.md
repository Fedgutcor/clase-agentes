# Construye tu primer agente IA

![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

> **En esta clase construyes un bot de Telegram con memoria, herramientas propias, y dos modelos de IA que se respaldan entre sí.**

---

## Antes de empezar — tu primer repositorio en GitHub

Si llegaste aquí desde GitHub por primera vez: estás mirando el **código fuente** del proyecto.  
GitHub es como Google Drive, pero para código. Cada archivo que ves arriba es parte del bot que vas a construir.

Para descargar el proyecto a tu computadora:

```bash
git clone https://github.com/Fedgutcor/clase-agentes
cd clase-agentes
```

`git clone` descarga una copia completa. `cd clase-agentes` entra a la carpeta descargada.  
**Haz esto una sola vez.** Después de clonarlo, trabajas desde tu computadora.

---

## Qué vas a construir

Un bot de Telegram que:

- Habla con dos modelos de IA (Gemini y Groq) y elige cuál usar según el mensaje
- Recuerda información sobre cada usuario entre conversaciones
- Tiene herramientas propias: calculadora, notas, y 10 extras que puedes conectar

No es un chatbot de juguete — tiene la misma arquitectura base de los agentes de producción.

---

## Cómo está organizado el proyecto

```
clase-agentes/
│
├── app.py              ← el cerebro del bot — aquí empieza todo
├── memory.py           ← cómo el bot guarda y recuerda datos de cada usuario
├── setup.py            ← instalación guiada (corre esto primero)
├── verify_setup.py     ← verifica que el setup esté completo
│
├── prompts/
│   ├── system.txt      ← la personalidad del agente (qué le dijiste que ES)
│   └── personality.txt ← instrucciones adicionales de comportamiento
│
├── tools/
│   ├── calculator.py   ← herramienta: hace cuentas sin pedírselas a la IA
│   ├── notes.py        ← herramienta: guarda y lista notas por usuario
│   └── extras/         ← 10 herramientas opcionales listas para conectar
│
├── memory/
│   └── users/          ← un archivo .json por usuario (se crea solo al correr)
│
├── requirements.txt    ← lista de librerías que necesita el proyecto
├── .env.example        ← plantilla para tus API keys (sin datos reales)
└── .env                ← tus keys reales (nunca se sube a GitHub)
```

**Tres conceptos clave que vas a ver en el código:**

| Concepto | Qué es en este proyecto |
|----------|------------------------|
| **Tool** | Una función Python que el agente puede ejecutar (calculadora, notas) |
| **Memoria** | Archivo JSON por usuario — el bot lo lee antes de responder |
| **Router** | Lógica que decide qué modelo de IA usar según el mensaje |

---

## Cómo funciona por dentro

```
┌──────────────────────────────────────────────────────┐
│  TELEGRAM  — canal de comunicación con el usuario    │
└───────────────────────┬──────────────────────────────┘
                        │ mensaje del usuario
                        ▼
┌──────────────────────────────────────────────────────┐
│  handle_message()  en app.py                         │
│  Lee el mensaje y decide qué hacer con él            │
└──────┬───────────────────────────┬───────────────────┘
       │                           │
       ▼                           ▼
┌──────────────┐          ┌────────────────────┐
│  TOOLS       │          │  ROUTER            │
│  (primero)   │          │  choose_model()    │
│              │          └────────┬───────────┘
│ "calcula…"  ─┼─▶ calculator.py  │
│ "guarda…"   ─┼─▶ notes.py       ├── "rápido/corto" ─▶ GROQ (Llama 3.1)
│ "recuerda…" ─┼─▶ memory.py      └── (por defecto) ──▶ GEMINI (Flash 2.0)
└──────────────┘                                            │
                                                            │ si falla
                                                            ▼
                                                     GROQ como fallback
                                                     + prefijo [fallback]
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

**Flujo en palabras**: el bot recibe un mensaje → revisa si es una tool (calculadora, notas) → si no, consulta la memoria del usuario → elige el modelo de IA → envía respuesta.

---

## Setup

### Paso 1 — Clona el repo

```bash
git clone https://github.com/Fedgutcor/clase-agentes
cd clase-agentes
```

### Paso 2 — Corre el setup guiado

```bash
python setup.py
```

El script hace todo por ti: crea el entorno virtual, instala librerías, te explica cada API key y dónde conseguirla, y las guarda en `.env`.

**Las tres API keys que necesitas:**

| Key | Dónde obtenerla | Es gratis? |
|-----|-----------------|-----------|
| `TELEGRAM_TOKEN` | Habla con [@BotFather](https://t.me/BotFather) en Telegram | Sí |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/app/apikey) | Sí |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com/keys) | Sí |

### Paso 3 — Arranca el bot

```bash
# Mac / Linux
source venv/bin/activate
python app.py

# Windows
venv\Scripts\activate
python app.py
```

Cuando veas el banner con "AGENTE IA — ONLINE", el bot está corriendo.  
Abre Telegram, busca tu bot, y empieza a chatear.

---

## Comandos del bot

| Mensaje | Qué hace | Qué parte del código lo maneja |
|---------|----------|-------------------------------|
| Cualquier texto | Responde con Gemini (o Groq si falla) | `ask_ai()` en app.py |
| `rápido qué es un agente` | Fuerza Groq — más veloz para respuestas cortas | `choose_model()` en app.py |
| `calcula 45 * 12` | Calculadora integrada | `tools/calculator.py` |
| `guarda nota comprar leche` | Guarda una nota tuya | `tools/notes.py` |
| `mis notas` | Lista todas tus notas | `tools/notes.py` |
| `recuerda que estudio diseño` | Guarda un hecho en tu perfil | `memory.py` |

---

## Tools extra (`tools/extras/`)

10 herramientas listas para conectar. Ninguna requiere API key adicional salvo las que ya tienes.

| Archivo | Qué hace | Comando de ejemplo |
|---------|----------|--------------------|
| `weather.py` | Clima en tiempo real | `clima en Bogotá` |
| `translator.py` | Traduce texto (usa Groq) | `traduce al inglés: hola mundo` |
| `summarizer.py` | Resume en 3 puntos (usa Groq) | `resume: [texto largo]` |
| `reminder.py` | Recordatorio con temporizador | `recuérdame en 10 minutos: llamar al médico` |
| `web_search.py` | Búsqueda en DuckDuckGo | `busca: noticias de IA hoy` |
| `qr_generator.py` | Genera QR como imagen PNG | `genera qr: https://google.com` |
| `currency.py` | Convierte monedas | `convierte 100 USD a EUR` |
| `joke.py` | Chiste aleatorio | `cuéntame un chiste` |
| `pomodoro.py` | Temporizador Pomodoro | `pomodoro 25` |
| `text_stats.py` | Estadísticas de un texto | `analiza texto: [tu texto]` |

### Cómo conectar una tool extra

Son tres líneas de código en `app.py`. Por ejemplo, para activar el clima:

**1. Importa la función** (arriba del todo en app.py, junto a los otros imports):

```python
from tools.extras.weather import get_weather
```

**2. Agrega un bloque `if`** dentro de `handle_message`, antes de la parte de IA:

```python
if message.lower().startswith("clima en "):
    city = message[9:]                               # extrae la ciudad del mensaje
    await update.message.reply_text(get_weather(city))
    return                                           # sale sin llamar a la IA
```

**3. Reinicia el bot.** Listo.

> `reminder.py` y `pomodoro.py` requieren pasar `update` como callback — hay un ejemplo comentado dentro de cada archivo.

---

## Resiliencia por fallback

El bot intenta Gemini primero. Si Gemini falla (cuota agotada, red), cae a Groq sin interrumpir la conversación.

```
Usuario → Gemini ✓ → respuesta normal
               ✗ → Groq → respuesta con prefijo [fallback groq]
```

El prefijo `[fallback groq]` es intencional: te avisa cuándo se usó el backup.  
Para quitarlo cuando ya no lo necesites, edita esta línea en `app.py`:

```python
# antes
return f"[fallback groq] {response.choices[0].message.content}"
# después
return response.choices[0].message.content
```

---

## Troubleshooting

**El bot no responde y veo `quota` en el error**  
Gemini tiene límite de tokens por minuto en el tier gratuito. Espera 30 segundos e intenta de nuevo.

**El bot responde con `[fallback groq]`**  
Gemini alcanzó su cuota. El bot sigue funcionando — espera 1 minuto.

**`Conflict: terminated by other getUpdates request`**  
Hay dos instancias corriendo. Mátalas y reinicia:

```bash
# Mac / Linux
pkill -9 -f python
cd ~/Downloads/clase-agentes && source venv/bin/activate && python app.py

# Windows
taskkill /F /IM python.exe
cd %USERPROFILE%\Downloads\clase-agentes && venv\Scripts\activate && python app.py
```

**`AttributeError` en `_Updater` o `TypeError: proxies`**  
Versión de librería incompatible. Reinstala:

```bash
pip install "python-telegram-bot==21.9" "groq>=1.2.0"
```

**`404 models/gemini-1.5-flash is not found`**  
Modelo deprecado. Asegúrate de tener la versión actualizada de `app.py`.

**No veo el archivo `.env`**  
Los archivos que empiezan con `.` están ocultos por defecto:
```bash
open -e .env      # Mac
notepad .env      # Windows
```

---

> Versión en inglés: [README.en.md](README.en.md)

---

MIT License · Federico Gutiérrez
