<p align="center">
  <img src="assets/avatar.png" alt="Project mascot: a smiling robot" width="180">
</p>

# Build Your First AI Agent

![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

> **In this class you build a Telegram bot with memory, custom tools, and three AI models that back each other up.**

---

## Architecture

```
Telegram
   │
   ▼
 Router
 ├── "rápido/corto"  → Groq (fastest)
 ├── "potente/exp."  → NVIDIA (largest, reasons before answering)
 └── default         → Gemini (balanced)
        └── automatic fallback chain → Gemini → Groq → NVIDIA

   + Manual tools
   ├── calculate ...      → calculator.py
   ├── save note ...      → notes.py
   └── my notes

   + Per-user memory
   └── remember that ...  → memory/users/{id}.json
```

---

## Setup

> **No-install option (recommended if you're new):** open the repo on GitHub → green **`< > Code`** button → **Codespaces** tab → **Create codespace on main**. You get a ready-to-use terminal in your browser (Python + Git preinstalled). Skip step 1 below and jump straight to `python setup.py`.

### 1. Clone the repo and enter the folder

```bash
git clone https://github.com/Fedgutcor/clase-agentes
cd clase-agentes
```

### 2. Run the guided setup

```bash
python setup.py
```

That's it. The script:
- Creates the virtual environment
- Installs all dependencies
- Explains each API key and where to get it (Telegram, Gemini, Groq, **and NVIDIA** — get the latter at [build.nvidia.com](https://build.nvidia.com), the key starts with `nvapi-`)
- Saves them securely to `.env`
- Verifies everything works

### 3. Start the bot

```bash
source venv/bin/activate   # Mac / Linux
venv\Scripts\activate      # Windows

python app.py
```

---

## Bot commands

| Message | What it does |
|---------|--------------|
| Any text | Responds with Gemini (or a backup if it fails) |
| `fast what is an agent` | Forces Groq — faster for short answers |
| `potente explain relativity` | Forces NVIDIA — larger model for hard questions |
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

The bot tries Gemini first. If Gemini fails (quota, network, unavailable model), it walks down the fallback chain — Gemini → Groq → NVIDIA — without interrupting the conversation.

```
User → Gemini ✓ → normal response
            ✗ → Groq ✓ → response prefixed with [fallback groq]
                    ✗ → NVIDIA → response prefixed with [fallback nvidia]
```

The prefix is intentional — it tells you which backup was used. To remove it once you no longer need it, edit the matching `return` in `app.py`:

```python
# before
return f"[fallback groq] {_ask_groq(prompt)}"
# after
return _ask_groq(prompt)
```

---

## Project structure

```
clase-agentes/
├── app.py              ← entry point, main logic
├── memory.py           ← per-user memory (JSON)
├── models.py           ← which AI model each provider uses (change it here or in .env)
├── verify_setup.py     ← checks the setup and pings each model with a real question
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

**Bot responds with `[fallback groq]` or `[fallback nvidia]`**
The primary model failed, so the bot walked down the fallback chain (Gemini → Groq → NVIDIA). It means resilience is working — wait 1 minute.

**`401`/`Unauthorized` when asking for something `potente`**
The `NVIDIA_API_KEY` is empty or wrong. Make sure it starts with `nvapi-` in your `.env`. Regenerate it at [build.nvidia.com](https://build.nvidia.com) and re-run `python setup.py` if needed.

**`ModuleNotFoundError: No module named 'openai'`**
The NVIDIA client (OpenAI-compatible) is missing. With the venv active: `pip install openai`.

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

**The bot stops answering and you see `404`, `410`, `not found`, `no longer available` or `model_not_found`**
The provider retired the model — it happens every few months. Either run `git pull` to get the latest models, or run `python verify_setup.py` to see which model failed, pick a current one from that provider's catalog, and add it to your `.env` (e.g. `GROQ_MODEL=model-name`). The defaults live in `models.py`.

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
