# Construye tu primer agente IA

![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

> **En esta clase construyes un bot de Telegram con memoria, herramientas propias, y dos modelos de IA que se respaldan entre sí.**

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                     TELEGRAM                        │
│              (canal de comunicación)                │
└───────────────────────┬─────────────────────────────┘
                        │ mensaje del usuario
                        ▼
┌─────────────────────────────────────────────────────┐
│                  HANDLE MESSAGE                     │
│              (app.py · punto de entrada)            │
└──────┬──────────────────────────┬───────────────────┘
       │                          │
       ▼                          ▼
┌─────────────┐          ┌────────────────────┐
│  TOOLS      │          │  ROUTER DE MODELOS │
│  manuales   │          │  choose_model()    │
│             │          └────────┬───────────┘
│ calcula … ──┼──▶ calculator.py  │
│ guarda … ───┼──▶ notes.py       ├── "rápido/rapido" ──▶ GROQ
│ mis notas ──┼──▶ notes.py       │                      Llama 3.1
│ recuerda ───┼──▶ memory.py      └── (default) ─────▶ GEMINI
└─────────────┘                                        Flash 2.0
                                                          │
                                                          │ falla (quota/red)
                                                          ▼
                                                       GROQ (fallback)
                                                       + prefijo [fallback]
       │
       ▼
┌─────────────────────┐
│  MEMORIA            │
│  memory/users/      │
│  {user_id}.json     │
│  → hechos del user  │
│    se inyectan en   │
│    el prompt        │
└─────────────────────┘
```

---

## Setup

### 1. Clona el repo y entra a la carpeta

```bash
git clone https://github.com/ultragresion/clase-agentes
cd clase-agentes
```

### 2. Crea el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
```

### 3. Instala dependencias

```bash
pip install -r requirements.txt
```

> Si ya tenías `google-generativeai` instalado de antes, desinstálalo primero — este proyecto usa la SDK nueva (`google-genai`):
> ```bash
> pip uninstall google-generativeai -y
> pip install -r requirements.txt
> ```

### 4. Configura tus API keys

```bash
cp .env.example .env
```

Abre `.env` y llena los tres valores:

```bash
open -e .env      # Mac
notepad .env      # Windows
```

| Variable | Dónde obtenerla |
|----------|-----------------|
| `TELEGRAM_TOKEN` | Telegram → @BotFather → `/newbot` |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) → Get API key |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys → Create |

> Los archivos `.` están ocultos por defecto. Si no ves `.env` en tu explorador de archivos, ábrelo directo desde la terminal con los comandos de arriba.

### 5. Verifica que todo funciona

```bash
python verify_setup.py
```

Si ves tres checkmarks verdes, estás listo. Corre el bot:

```bash
python app.py
```

---

## Comandos del bot

| Mensaje | Qué hace |
|---------|----------|
| Cualquier texto | Responde con Gemini (o Groq si falla) |
| `rápido qué es un agente` | Fuerza Groq — más veloz para respuestas cortas |
| `calcula 45 * 12` | Calculadora integrada |
| `guarda nota comprar leche` | Guarda una nota tuya |
| `mis notas` | Lista todas tus notas |
| `recuerda que estudio diseño` | Guarda un hecho en tu perfil |

---

## Tools extra (`tools/extras/`)

10 herramientas listas para conectar al agente. Ninguna requiere API key adicional salvo las que ya tienes.

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

### Cómo conectar una tool

**1.** Importa la función en `app.py`:

```python
from tools.extras.weather import get_weather
```

**2.** Agrega un bloque `if` en `handle_message`:

```python
if message.lower().startswith("clima en "):
    city = message[9:]
    await update.message.reply_text(get_weather(city))
    return
```

**3.** Reinicia el bot. Listo.

> `reminder.py` y `pomodoro.py` requieren pasar `update` como callback — hay un ejemplo comentado dentro de cada archivo.

---

## Resiliencia por fallback

El bot intenta Gemini primero. Si Gemini falla (cuota, red, modelo no disponible), cae automáticamente a Groq sin interrumpir la conversación.

```
Usuario → Gemini ✓ → respuesta normal
               ✗ → Groq → respuesta con prefijo [fallback groq]
```

El prefijo es intencional: te avisa cuándo se usó el backup. Para quitarlo cuando ya no lo necesites, edita `app.py`:

```python
# antes
return f"[fallback groq] {response.choices[0].message.content}"
# después
return response.choices[0].message.content
```

---

## Estructura del proyecto

```
clase-agentes/
├── app.py              ← punto de entrada, lógica principal
├── memory.py           ← memoria por usuario (JSON)
├── verify_setup.py     ← verifica que el setup está completo
├── requirements.txt    ← dependencias
├── .env.example        ← template de configuración (sin keys reales)
├── .env                ← tus keys (no se sube a GitHub)
├── prompts/
│   ├── system.txt      ← personalidad base del agente
│   └── personality.txt
├── tools/
│   ├── calculator.py
│   ├── notes.py
│   └── extras/         ← 10 tools adicionales opcionales
├── memory/
│   └── users/          ← un .json por usuario (generado al correr)
└── logs/
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
Los archivos que empiezan con `.` están ocultos. Ábrelo desde la terminal:
```bash
open -e .env      # Mac
notepad .env      # Windows
```

---

> English version: [README.en.md](README.en.md)

---

MIT License · Federico Gutiérrez
