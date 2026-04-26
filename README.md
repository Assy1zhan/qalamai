# QalamAI — Multilingual AI Tutor Telegram Bot

An AI-powered Telegram chatbot that acts as a virtual tutor for students and a planning assistant for teachers, supporting **Russian, Kazakh, and English**.

## What it does

QalamAI behaves differently depending on who's using it:

- **For students** — instead of giving answers directly, the bot uses the **Socratic method**: it asks leading questions, gauges the student's existing knowledge, reinforces theory with practice problems for STEM topics, and helps with writing without writing *for* the student. It adapts to the student's grade level.
- **For teachers** — the bot helps draft lesson plans and answer pedagogical questions, asking clarifying questions about subject, grade level, and curriculum to produce relevant plans.

Both modes are available in three languages, selected at the start of each session.

## Tech stack

- **Python 3.11**
- **[aiogram 3.x](https://github.com/aiogram/aiogram)** — async Telegram bot framework
- **OpenAI API** (`gpt-4o-mini`) for response generation
- **python-dotenv** for environment-variable management
- **Heroku** (`Procfile`) as the original hosting target

## Architecture

- `run.py` — entry point; sets up the bot and dispatcher.
- `app/handlers.py` — message and callback handlers, including the system prompts that define the bot's pedagogical behavior.
- `app/keyboards.py` — inline keyboards for language and role selection.

The bot keeps a per-user conversation history (in-memory, keyed by Telegram user ID) and sends it to the OpenAI Chat Completions endpoint on every message. Conversation state resets on `/start`.

## How to run locally

### Prerequisites
- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- An OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)

### Setup

```bash
git clone https://github.com/Assy1zhan/qalamai.git
cd qalamai

python -m venv venv
source venv/bin/activate          # macOS / Linux
# .\venv\Scripts\activate         # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env and put your real TG_TOKEN and AI_TOKEN values

python run.py
```

The bot uses long polling, so no public URL or webhook is needed for local testing.

### Deploy

The included `Procfile` (`worker: python run.py`) is configured for Heroku worker dynos, but the same command works on any platform that supports Python workers (Railway, Render, Fly.io, a VPS with `systemd`, etc.).

## What I learned

- Building real async Python applications using `asyncio` and `aiogram`'s router/dispatcher pattern.
- Designing **system prompts** that shape an LLM's behavior over a multi-turn conversation, including role-conditioned and language-conditioned prompts.
- Per-user state management in a polling bot.
- Environment-variable hygiene — using `python-dotenv` and `.env.example`, never committing secrets.
- Deploying a long-running Python process via `Procfile` and `requirements.txt`.

## Possible extensions

- Persist conversation history to a database (SQLite or Postgres) so context survives restarts.
- Add per-user rate limiting to control OpenAI API costs.
- Structured logging and monitoring.
- Unit tests for handler logic with mocked OpenAI responses.
- Streamed responses (`stream=True`) so users see replies progressively.
