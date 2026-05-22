# Build Your First AI Agent

![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

> **In this class you build a Telegram bot with memory, custom tools, and two AI models that back each other up.**

---

## Architecture

```
Telegram
   │
   ▼
 Router
 ├── "fast/quick" → Groq (Llama 3.1)
 └── default      → Gemini 2.0 Flash
                       └── automatic fallback → Groq

   + Manual tools
   ├── calculate ...      → calculator.py
   ├── save note ...      → notes.py
   └── my notes

   + Per-user memory
   └── remember that ...  → memory/users/{id}.json
```

---

## Setup

### 1. Clone the repo and enter the folder

```bash
git clone https://github.com/ultragresion/clase-agentes
cd clase-agentes
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If you already have `google-generativeai` installed, uninstall it first — this project uses the new SDK (`google-genai`):
> ```bash
> pip uninstall google-generativeai -y
> pip install -r requirements.txt
> ```

### 4. Configure your API keys

```bash
cp .env.example .env
```

Open `.env` and fill in the three values:

```bash
open -e .env      # Mac
notepad .env      # Windows
```

| Variable | Where to get it |
|----------|-----------------|
| `TELEGRAM_TOKEN` | Telegram → @BotFather → `/newbot` |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) → Get API key |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys → Create |

> `.env` is a hidden file. If you don't see it in your file explorer, open it directly from the terminal using the commands above.

### 5. Verify everything works

```bash
python verify_setup.py
```

If you see three green checkmarks, you're ready. Run the bot:

```bash
python app.py
```

---

## Bot commands

| Message | What it does |
|---------|--------------|
| Any text | Responds with Gemini (or Groq if it fails) |
| `fast what is an agent` | Forces Groq — faster for short answers |
| `calculate 45 * 12` | Built-in calculator |
| `save note buy milk` | Saves a note |
| `my notes` | Lists all your notes |
| `remember that I study design` | Saves a fact to your profile |

---

## Extra tools (`tools/extras/`)

10 tools ready to plug into the agent. None require additional API keys beyond what you already have.

| File | What it does | Example command |
|------|--------------|-----------------|
| `weather.py` | Real-time weather | `weather in London` |
| `translator.py` | Translates text (uses Groq) | `translate to Spanish: hello world` |
| `summarizer.py` | Summarizes in 3 points (uses Groq) | `summarize: [long text]` |
| `reminder.py` | Timer-based reminder | `remind me in 10 minutes: call the doctor` |
| `web_search.py` | DuckDuckGo search | `search: AI news today` |
| `qr_generator.py` | Generates QR as PNG image | `generate qr: https://google.com` |
| `currency.py` | Currency conversion | `convert 100 USD to EUR` |
| `joke.py` | Random joke | `tell me a joke` |
| `pomodoro.py` | Pomodoro timer | `pomodoro 25` |
| `text_stats.py` | Text statistics | `analyze text: [your text]` |

### How to connect a tool

**1.** Import the function in `app.py`:

```python
from tools.extras.weather import get_weather
```

**2.** Add an `if` block in `handle_message`:

```python
if message.lower().startswith("weather in "):
    city = message[11:]
    await update.message.reply_text(get_weather(city))
    return
```

**3.** Restart the bot. Done.

> `reminder.py` and `pomodoro.py` require passing `update` as a callback — there's a commented example inside each file.

---

## Fallback resilience

The bot tries Gemini first. If Gemini fails (quota, network, unavailable model), it automatically falls back to Groq without interrupting the conversation.

```
User → Gemini ✓ → normal response
            ✗ → Groq → response prefixed with [fallback groq]
```

The prefix is intentional — it tells you when the backup was used. To remove it once you no longer need it, edit `app.py`:

```python
# before
return f"[fallback groq] {response.choices[0].message.content}"
# after
return response.choices[0].message.content
```

---

## Project structure

```
clase-agentes/
├── app.py              ← entry point, main logic
├── memory.py           ← per-user memory (JSON)
├── verify_setup.py     ← checks that setup is complete
├── requirements.txt    ← dependencies
├── .env.example        ← config template (no real keys)
├── .env                ← your keys (never committed to GitHub)
├── prompts/
│   ├── system.txt      ← agent base personality
│   └── personality.txt
├── tools/
│   ├── calculator.py
│   ├── notes.py
│   └── extras/         ← 10 optional extra tools
├── memory/
│   └── users/          ← one .json per user (auto-generated)
└── logs/
```

---

## Troubleshooting

**Bot doesn't respond and I see `quota` in the error**
Gemini has a token-per-minute limit on the free tier. Wait 30 seconds and try again.

**Bot responds with `[fallback groq]`**
Gemini hit its quota. The bot keeps working — wait 1 minute.

**`Conflict: terminated by other getUpdates request`**
Two instances are running. Kill them and restart:

```bash
# Mac / Linux
pkill -9 -f python
cd ~/Downloads/clase-agentes && source venv/bin/activate && python app.py

# Windows
taskkill /F /IM python.exe
cd %USERPROFILE%\Downloads\clase-agentes && venv\Scripts\activate && python app.py
```

**`AttributeError` in `_Updater` or `TypeError: proxies`**
Incompatible library version. Reinstall:

```bash
pip install "python-telegram-bot==21.9" "groq>=1.2.0"
```

**`404 models/gemini-1.5-flash is not found`**
Deprecated model. Make sure you have the latest version of `app.py`.

**I can't see the `.env` file**
Files starting with `.` are hidden by default. Open it directly from the terminal:
```bash
open -e .env      # Mac
notepad .env      # Windows
```

---

> Versión en español: [README.md](README.md)

---

MIT License · Federico Gutiérrez
