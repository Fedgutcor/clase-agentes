<p align="center">
  <img src="assets/avatar.png" alt="Mascota del proyecto: un robot sonriente" width="180">
</p>

# Construye tu primer agente IA

![Python](https://img.shields.io/badge/python-3.10+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

> **En esta clase construyes un bot de Telegram con memoria, herramientas propias, y tres modelos de IA que se respaldan entre sí.**
>
> *¿Nunca tocaste una terminal? Tranquilo. Esta guía asume cero experiencia: cada comando viene explicado, y al final hay un [glosario](#glosario--qué-significa-cada-palabra) con todas las palabras técnicas en lenguaje cotidiano.*

---

## Índice

1. [Qué vas a construir](#qué-vas-a-construir)
2. [Antes de empezar](#antes-de-empezar)
3. [La forma fácil — Codespaces (sin instalar nada)](#la-forma-fácil--codespaces-sin-instalar-nada)
4. [La forma local — en tu computadora](#la-forma-local--en-tu-computadora)
5. [Setup paso a paso](#setup-paso-a-paso)
6. [Qué hace cada parte del proyecto](#qué-hace-cada-parte-del-proyecto)
7. [Cómo funciona por dentro](#cómo-funciona-por-dentro)
8. [Comandos del bot](#comandos-del-bot)
9. [Conectar herramientas extra](#conectar-herramientas-extra)
10. [Hasta dónde puedes llevarlo](#hasta-dónde-puedes-llevarlo)
11. [Glosario — qué significa cada palabra](#glosario--qué-significa-cada-palabra)
12. [Troubleshooting](#troubleshooting)

---

## Qué vas a construir

Un bot de Telegram que:

- Habla con tres modelos de IA (Gemini, Groq y NVIDIA) y **elige cuál usar** según el mensaje
- **Recuerda información** sobre cada usuario entre conversaciones
- Tiene **herramientas propias**: calculadora, notas, y 10 extras que puedes activar

No es un chatbot de juguete — tiene la misma arquitectura base de los agentes de producción.

**Los tres modelos, en una frase:**

| Modelo | Cuándo lo usa el bot | Por qué |
|--------|----------------------|---------|
| **Gemini** (Google) | Por defecto, para casi todo | Equilibrado: rápido y capaz |
| **Groq** (un modelo abierto en chips especiales) | Cuando pides algo `rápido` | El más veloz para respuestas cortas |
| **NVIDIA** (Nemotron, un modelo grande que razona) | Cuando pides algo `potente` | El más grande, para preguntas difíciles. Tarda unos segundos más porque *piensa* antes de responder |

Y si uno falla, el bot pasa solo al siguiente. Nunca te quedas sin respuesta.

> **¿Cuál modelo exacto usa cada uno?** Está escrito en un solo archivo: `models.py`. Los proveedores retiran modelos cada pocos meses; cuando eso pase, `python verify_setup.py` te dirá cuál falló y cómo cambiarlo (ver [Troubleshooting](#troubleshooting)).

---

## Antes de empezar

Esto es lo único que necesitas tener listo. Son cuentas gratis, sin tarjeta de crédito.

- [ ] Una cuenta de **Telegram** (la app de mensajería) — [telegram.org](https://telegram.org)
- [ ] Una cuenta de **Google** (para la key de Gemini) — seguramente ya tienes una
- [ ] Una cuenta de **GitHub** — [github.com/signup](https://github.com/signup)

**Tiempo:** unos 20-30 minutos la primera vez. No tienes que terminar de una sentada.

**Ahora elige tu camino.** Hay dos formas de hacer la clase. Hacen exactamente lo mismo — cambia solo *dónde* corre el bot:

| | 🟢 La forma fácil (Codespaces) | 💻 La forma local |
|---|---|---|
| **Dónde corre** | En tu navegador, en la nube | En tu propia computadora |
| **¿Instalas algo?** | **Nada** | Python + Git |
| **Ideal para** | Empezar sin complicarte | Tener todo en tu máquina |

> **Si nunca programaste, usa Codespaces.** Te ahorra instalar Python y Git —que es donde más gente se traba— y te da una terminal lista con un par de clicks. Lee la sección de abajo y sáltate por completo "La forma local".

---

## La forma fácil — Codespaces (sin instalar nada)

GitHub Codespaces te presta una computadora en la nube con **todo preinstalado**, dentro de tu navegador. No instalas Python, ni Git, ni nada en tu máquina.

1. Entra al repositorio: **[github.com/Fedgutcor/clase-agentes](https://github.com/Fedgutcor/clase-agentes)**
2. Haz click en el botón verde **`< > Code`** (arriba a la derecha de la lista de archivos)
3. Elige la pestaña **"Codespaces"** y haz click en **"Create codespace on main"**
4. Espera 1-2 minutos. Se abre un editor (es VS Code) dentro del navegador, con Python y Git ya listos.
5. En la parte de abajo verás una **terminal**. Si no aparece, abre el menú **`☰`** (arriba a la izquierda) → **Terminal → New Terminal**. Ahí vas a escribir los comandos.

Eso es todo. **Salta directo a [Setup paso a paso](#setup-paso-a-paso)** y corre `python setup.py` en esa terminal. El resto de la guía funciona igual.

> Codespaces es gratis hasta 60 horas al mes — de sobra para esta clase. Cuando termines, ciérralo en **[github.com/codespaces](https://github.com/codespaces)** (botón `...` → *Stop*) para no gastar horas mientras no lo usas.

---

## La forma local — en tu computadora

> **¿Usaste Codespaces?** Entonces sáltate toda esta sección y ve directo a [Setup paso a paso](#setup-paso-a-paso). Esto es solo para quien quiere instalar el proyecto en su propia máquina.

### Herramientas que vas a usar

Antes de instalar nada, asegúrate de tener esto:

| Herramienta | Para qué sirve | Cómo saber si la tienes |
|-------------|---------------|------------------------|
| **Python 3.10+** | El lenguaje en que está escrito el bot | En la terminal: `python --version` |
| **Git** | Para descargar el proyecto desde GitHub | En la terminal: `git --version` |

Si alguno de esos comandos dice "command not found" (no lo reconoce), instálalo:
- **Python**: descárgalo en [python.org/downloads](https://www.python.org/downloads/) — instala la versión más reciente
- **Git**: descárgalo en [git-scm.com/downloads](https://git-scm.com/downloads)

> ⚠️ **Importante en Windows — el error #1 de toda la clase:** cuando instalas Python, la **primera** pantalla del instalador tiene, abajo, una casilla que dice **"Add Python to PATH"** (o "Add python.exe to PATH"). **MÁRCALA antes de continuar.** Si no lo haces, Windows no encontrará el comando `python` y nada funcionará — y el error no dice que la causa fue esa casilla. Si ya instalaste sin marcarla: desinstala Python desde "Agregar o quitar programas" y vuelve a instalarlo marcando la casilla.

Después de instalar, **cierra y vuelve a abrir la terminal**, y confirma que ambos responden:

```bash
python --version
git --version
```

Si los dos te muestran un número de versión (ej: `Python 3.12.1`), estás listo para seguir.

### Cómo abrir la terminal

La **terminal** es la ventana negra donde escribes comandos de texto. Todo lo que hagas en esta guía pasa ahí.

#### En Mac

1. Presiona `Cmd + Espacio` para abrir Spotlight
2. Escribe `Terminal`
3. Presiona Enter

Verás una ventana con texto. Eso es la terminal. Está lista para recibir comandos.

#### En Windows

1. Presiona `Win + R`
2. Escribe `cmd`
3. Presiona Enter

> **Recomendado en Windows**: usa **PowerShell** en lugar de cmd. Para abrirlo: click derecho en el botón de Inicio → "Windows PowerShell".

#### Cómo usar la terminal

- Escribes un comando y presionas **Enter** para ejecutarlo
- Solo puedes ejecutar un comando a la vez — espera a que termine antes del siguiente
- Si ves un error en rojo, es normal — el troubleshooting al final de esta guía cubre los más comunes

> **Truco para no escribir a mano**: puedes **copiar** un comando de esta guía y **pegarlo** en la terminal.
> - **Mac**: pegar es `Cmd + V`
> - **Windows**: pegar es `Ctrl + V` (o click derecho dentro de la terminal)
>
> **No te asustes si la terminal "no hace nada" mientras escribes tu contraseña o una key**: por seguridad, algunos campos no muestran lo que tecleas (ni puntitos). Está escribiendo igual — presiona Enter al terminar.

---

### Cómo descargar el proyecto

GitHub es donde está guardado el código (como una "nube" de proyectos). Hay dos maneras de bajarlo. Elige una:

**Opción A — sin Git (la más simple):**

1. Entra a [github.com/Fedgutcor/clase-agentes](https://github.com/Fedgutcor/clase-agentes)
2. Haz click en el botón verde **`< > Code`** → **"Download ZIP"**
3. Descomprime el archivo (doble click en Windows; en Mac se descomprime solo)
4. Mueve la carpeta `clase-agentes` a un lugar fácil de encontrar, por ejemplo tu Escritorio
5. Abre la terminal y entra a esa carpeta con `cd` (ver abajo qué significa)

Con esta opción no necesitas Git instalado. La desventaja: para traer cambios futuros tienes que volver a descargar el ZIP (con Git bastaría un `git pull`).

**Opción B — con Git (recomendada si lo tienes):**

**Git** es un programa que descarga y maneja código; el comando `git clone` hace la descarga. **Abre la terminal** y ejecuta estos dos comandos, **uno por uno** (escribe el primero, Enter, espera a que termine, y recién ahí el segundo):

```bash
git clone https://github.com/Fedgutcor/clase-agentes
```

Esto descarga el proyecto y crea una carpeta llamada `clase-agentes` donde estés parado. Mientras descarga vas a ver algo así — es normal:

```
Cloning into 'clase-agentes'...
remote: Enumerating objects: 100% (...), done.
Receiving objects: 100% (...), done.
```

Cuando vuelve a aparecer la línea para escribir, terminó. Ahora entra a la carpeta:

```bash
cd clase-agentes
```

`cd` significa "entrar a una carpeta" (*change directory*). Después de esto, todos los comandos que ejecutes se aplican dentro del proyecto.

> **¿Cómo sé que estoy dentro de la carpeta?** El nombre `clase-agentes` aparece ahora en la línea de la terminal, antes del cursor. Esa línea (con la ruta o el nombre de carpeta) se llama el *prompt* — es la terminal diciéndote dónde estás parado.

> **¿Dónde quedó la carpeta?**
> - **Mac**: en tu carpeta de usuario (`/Users/tu-nombre/clase-agentes`). Puedes abrirla desde Finder.
> - **Windows**: en `C:\Users\tu-nombre\clase-agentes`. Puedes abrirla desde el Explorador de archivos.

---

## Setup paso a paso

### Paso 1 — Instala las dependencias

Asegúrate de estar dentro de la carpeta del proyecto (si usaste Codespaces o acabas de clonar, ya lo estás).

Ejecuta en la terminal:

```bash
python setup.py
```

Este script hace todo por ti:
- Crea un **entorno virtual** — una caja aislada con las librerías del proyecto, para no mezclarlas con el resto de tu computadora
- Instala las librerías necesarias
- Te pregunta tus API keys y las guarda de forma segura en un archivo `.env`

El script te explica cada key mientras lo corres. Si prefieres conseguirlas antes, aquí está el paso a paso para cada una:

---

#### Token de Telegram — `TELEGRAM_TOKEN`

1. Abre Telegram y busca **@BotFather** (el oficial tiene una palomita azul)
2. Escribe `/newbot` y presiona Enter
3. Te va a pedir un **nombre** para el bot (el que verán los usuarios, ej: "Mi Agente IA")
4. Luego un **username** — debe terminar en `bot` (ej: `mi_agente_ia_bot`)
5. BotFather te responde con un mensaje que incluye el token. Se ve así:
   ```
   Use this token to access the HTTP API:
   7123456789:ABCdefGHIjklMNOpqrsTUVwxyz_EJEMPLO
   ```
   (token de ejemplo, no es válido — el tuyo lo genera BotFather en el paso anterior)
6. Copia ese token — es tu `TELEGRAM_TOKEN`

> El username del bot es cómo lo van a encontrar en Telegram. Una vez creado, puedes hablarle buscando `@mi_agente_ia_bot`.

---

#### API Key de Gemini — `GEMINI_API_KEY`

1. Entra a [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Si te pide iniciar sesión, usa tu cuenta de Google
3. Haz click en **"Create API key"**
4. Selecciona **"Create API key in new project"**
5. Se genera una clave. Se ve así: `AIzaSyD3k8...`
6. Haz click en el ícono de copiar al lado de la clave

> Guárdala en un lugar seguro — Google no te la vuelve a mostrar completa después de cerrar esa ventana. Si la pierdes, crea una nueva.

---

#### API Key de Groq — `GROQ_API_KEY`

1. Entra a [console.groq.com](https://console.groq.com) y crea una cuenta (puedes usar Google)
2. En el menú de la izquierda, haz click en **"API Keys"**
3. Haz click en **"Create API Key"**
4. Ponle un nombre (ej: "clase-agentes") — es solo para que tú la identifiques
5. Se genera la clave. Se ve así: `gsk_abc123...`
6. Cópiala en ese momento — Groq tampoco la vuelve a mostrar completa

---

#### API Key de NVIDIA — `NVIDIA_API_KEY`

NVIDIA tiene una plataforma gratuita, **NVIDIA build**, para probar sus modelos de IA más grandes. Esta key es la que usa el bot cuando le pides algo `potente`.

1. Entra a [build.nvidia.com](https://build.nvidia.com)
2. Haz click en **"Login"** (arriba a la derecha) y crea una cuenta — puedes usar tu correo o tu cuenta de Google
3. Una vez dentro, abre cualquier modelo del catálogo — por ejemplo, escribe **`nemotron`** en el buscador y abre el primero que aparezca. La key que vas a generar sirve para todos los modelos, no solo para ese
4. En la página del modelo, a la derecha verás un panel de código con un botón **"Get API Key"** (o "Generate Key"). Haz click ahí
5. Confirma y se genera la clave. Empieza con `nvapi-`, así: `nvapi-AbC123...`
6. Cópiala enseguida — guárdala en un lugar seguro

> **¿Por qué empieza con `nvapi-`?** Es solo el prefijo que NVIDIA le pone a todas sus keys, para reconocerlas de un vistazo. Igual que las de Groq empiezan con `gsk_`.
>
> La cuenta gratuita te da créditos de sobra para la clase. Si alguna vez se agotan, el bot sigue funcionando con Gemini y Groq.

---

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

Esto comprueba que las API keys están bien configuradas y le hace una pregunta corta a cada modelo para confirmar que responde. Si algo falla, te dice exactamente qué y cómo arreglarlo.

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
├── models.py           ← qué modelo de IA usa cada proveedor (se cambia aquí o en el .env)
├── setup.py            ← instalación guiada (solo se corre una vez)
├── verify_setup.py     ← verifica el setup y prueba que cada modelo responda
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
├── .devcontainer/      ← receta del entorno en la nube (lo usa Codespaces)
├── .env.example        ← plantilla del archivo de configuración (sin datos reales)
└── .env                ← tus API keys reales (nunca se sube a GitHub)
```

**Tres conceptos que aparecen en todo el código:**

**Tool** — Una función Python que el bot puede ejecutar directamente, sin pasar por la IA.  
Ejemplo: cuando escribes `calcula 45 * 12`, el bot llama a `calculator.py` y te devuelve el resultado. La IA no interviene.

**Memoria** — Cada usuario tiene un archivo `.json` en `memory/users/`. Antes de responder, el bot lo lee e inyecta esa información en el prompt. Así "recuerda" cosas entre conversaciones.

**Router** — La función `choose_model()` en `app.py` lee el mensaje y decide a cuál de los tres modelos mandarlo: Groq si pediste algo `rápido`, NVIDIA si pediste algo `potente`, y Gemini para todo lo demás. Si el modelo por defecto falla, el bot baja por una cadena de respaldo (Gemini → Groq → NVIDIA) para que siempre haya respuesta.

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
│ "guarda…"   ─┼─▶ notes.py       ├─ "rápido/corto" ───▶ GROQ (el más veloz)
│ "recuerda…" ─┼─▶ memory.py      ├─ "potente/exp."  ─▶ NVIDIA (el más grande)
└──────────────┘                  └─ (por defecto) ───▶ GEMINI (equilibrado)
                                                             │
                                                             │ si falla, baja por la
                                                             ▼ cadena de respaldo:
                                                   GEMINI → GROQ → NVIDIA
                                                   + aviso [fallback ...]
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

**En palabras**: el bot recibe un mensaje → revisa si es una tool (calculadora, notas) → si no lo es, consulta la memoria del usuario → elige el modelo de IA (Gemini, Groq o NVIDIA) → envía la respuesta.

---

## Comandos del bot

| Mensaje | Qué hace | Archivo que lo maneja |
|---------|----------|-----------------------|
| Cualquier texto | Responde con Gemini (o el respaldo si falla) | `app.py` → `ask_ai()` |
| `rápido qué es un agente` | Fuerza Groq — más veloz para respuestas cortas | `app.py` → `choose_model()` |
| `potente explícame la relatividad` | Fuerza NVIDIA — modelo más grande para preguntas difíciles | `app.py` → `choose_model()` |
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

## Hasta dónde puedes llevarlo

Terminaste la clase y tienes un agente funcionando. Esto no es el techo — es la base. Acá van ideas para seguir, ordenadas de más fácil a más ambiciosa. No necesitas hacerlas todas: elige la que te dé curiosidad.

**Cambiar el modelo de NVIDIA (5 minutos).**
En `build.nvidia.com` hay decenas de modelos. Abre `models.py` y cambia el valor de `NVIDIA_MODEL` por el nombre de otro modelo del catálogo (ej. uno especializado en código). Reinicia el bot y compara las respuestas. Así aprendes que *cambiar de cerebro es cambiar una línea*.

> Ojo: algunos modelos "razonan" y entregan su respuesta en un campo distinto. Si después del cambio el bot responde vacío o con un error, ese modelo no encaja con el código tal como está — prueba con otro y corre `python verify_setup.py` para confirmar.

**Inventar tu propio comando de router (10 minutos).**
Hoy `rápido` manda a Groq y `potente` a NVIDIA. Abre `choose_model()` y agrega tu propia palabra clave — por ejemplo, que `código` siempre vaya a un modelo bueno programando. Es el mismo patrón, copiado.

**Activar más herramientas (15 minutos).**
Ya tienes 10 tools listas en `tools/extras/`. Sigue la receta de [Conectar herramientas extra](#conectar-herramientas-extra) y enciende clima, traductor, búsqueda web... Cada una son ~4 líneas en `app.py`.

**Escribir tu primera herramienta propia.**
Una tool es solo una función de Python que devuelve texto. Copia `tools/calculator.py`, cámbiale la lógica por lo que quieras (un conversor, un generador de contraseñas, lo que sea) y conéctala como cualquier extra. El bot no sabe la diferencia.

**Darle más personalidad.**
Abre `prompts/system.txt` y `prompts/personality.txt` y reescríbelos. No tocas ni una línea de código: cambias *quién es* el agente. Pruébalo — la diferencia es inmediata.

**Conceptos para investigar cuando quieras crecer:**

| Concepto | Qué te abre |
|----------|-------------|
| **Function calling / tool use** | Que la IA decida *sola* qué herramienta usar, en vez de detectarlo con `startswith` |
| **RAG** (búsqueda + IA) | Que el bot responda usando *tus* documentos, no solo lo que el modelo ya sabe |
| **Bases de datos** (SQLite) | Reemplazar los archivos `.json` de memoria por algo que escale a miles de usuarios |
| **Despliegue** (deploy) | Sacar el bot de tu computadora y dejarlo corriendo 24/7 en un servidor |
| **Streaming** | Que las respuestas aparezcan palabra por palabra, como en ChatGPT |

> No corras a aprender todo de golpe. Elige UNA cosa, hazla funcionar, y disfruta el momento en que cae la ficha. Así se construye de verdad.

---

## Glosario — qué significa cada palabra

Si en algún punto una palabra te frenó, búscala acá. Todo en lenguaje cotidiano.

| Palabra | En cristiano |
|---------|-------------|
| **Terminal** | La ventana de texto donde escribes comandos. La "consola" de tu computadora. |
| **Comando** | Una orden que escribes en la terminal y ejecutas con Enter (ej: `python app.py`). |
| **Git** | Un programa para descargar y manejar código que vive en internet. |
| **GitHub** | El sitio web donde está guardado el código de este proyecto (y de millones más). |
| **Codespaces** | Una computadora en la nube, con todo preinstalado, que abres dentro del navegador. |
| **Clonar** (`git clone`) | Descargar una copia del proyecto a tu computadora. |
| **Repositorio** (repo) | La carpeta de un proyecto con todo su código e historial. Esto que clonaste es un repo. |
| **Directorio / carpeta** | Lo mismo que una carpeta en tu computadora. `cd` sirve para entrar a una. |
| **Python** | El lenguaje de programación en el que está escrito el bot. |
| **Librería** | Código que otros ya escribieron y tú reutilizas (ej: `rich`, `openai`). |
| **Dependencias** | Las librerías que el proyecto necesita para funcionar. Están en `requirements.txt`. |
| **Entorno virtual** (venv) | Una caja aislada con las librerías de *este* proyecto, para no mezclarlas con el resto. |
| **API** | La forma en que dos programas se hablan entre sí por internet. |
| **API key** | Una credencial secreta que te identifica ante un servicio (Gemini, Groq, NVIDIA). |
| **Token** (de Telegram) | La API key específica de tu bot de Telegram: su usuario y contraseña juntos. |
| **`.env`** | El archivo donde se guardan tus keys. Nunca se sube a GitHub. |
| **Variable de entorno** | Un dato de configuración que el código lee del sistema (tus keys llegan así). |
| **Modelo** (LLM) | El "cerebro" de IA que genera las respuestas. Acá hay tres: Gemini, Groq, NVIDIA. |
| **Prompt** | El texto que le mandas a la IA. También: la línea de la terminal lista para tu comando. |
| **Router** | La función que decide a cuál modelo mandar cada mensaje. |
| **Fallback** | El plan B: si un modelo falla, el bot usa otro automáticamente. |
| **Tool** (herramienta) | Una función que el bot ejecuta directo, sin pasar por la IA (ej: la calculadora). |

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

**El bot responde con `[fallback groq]` o `[fallback nvidia]`**  
El modelo principal (Gemini) alcanzó su cuota o falló, así que el bot bajó por la cadena de respaldo (Gemini → Groq → NVIDIA). Es señal de que el fallback funciona. Espera 1 minuto y Gemini vuelve.

**Al pedir algo `potente` veo un error `401` o `Unauthorized`**  
La `NVIDIA_API_KEY` está vacía o mal copiada. Confirma que en tu `.env` empiece con `nvapi-` y no tenga espacios. Si dudas, vuelve a generarla en [build.nvidia.com](https://build.nvidia.com) y corre `python setup.py` de nuevo para pegarla.

**`ModuleNotFoundError: No module named 'openai'`**  
Falta la librería de NVIDIA (usa el cliente de OpenAI). Con el entorno activado:
```bash
pip install openai
```

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

**El bot no responde y veo `404`, `410`, `not found`, `no longer available` o `model_not_found`**  
El proveedor retiró el modelo. Pasa cada pocos meses: a este repo ya le ocurrió con `gemini-1.5-flash`, `gemini-2.0-flash` y los modelos Llama de Groq y NVIDIA. Tienes dos salidas:

1. Descarga la versión más reciente del repo, que trae modelos vigentes:
   ```bash
   git pull
   ```
2. Si el repo todavía no se actualizó, corre `python verify_setup.py`: te dice qué modelo falló. Busca uno vigente en el catálogo de ese proveedor y agrégalo a tu `.env` (por ejemplo `GROQ_MODEL=nombre-del-modelo`). Reinicia el bot.

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
