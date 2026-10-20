# LUXE — AI Shopping Assistant

A clothing store with an AI shopping assistant on top: browse by category and
price today; soon, just ask ("white shirt under 2000") and get real products
back, powered by a natural-language-to-MongoDB-filter agent — no vector
database, no embeddings.

## Status

**Phase 1 (the store) is done.** Phase 2 (the chatbot) is next. See
[`docs/04-status.md`](docs/04-status.md) for the full checklist.

## Stack

FastAPI (Python) · MongoDB Atlas · plain HTML/CSS/JS, no build step ·
Pydantic AI + Groq *(Phase 2)* · Google Cloud Run *(Phase 4)*

## Quick start

```bash
python3 -m venv luxeenv
source luxeenv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # fill in MONGO_URI
python -m seed_data.seed
python -m uvicorn main:app --reload
```

Open <http://127.0.0.1:8000>. Full setup walkthrough, including
troubleshooting: [`docs/03-setup.md`](docs/03-setup.md).

## Documentation

| | |
|---|---|
| [Overview](docs/01-overview.md) | What this is, the stack, why each piece |
| [Architecture](docs/02-architecture.md) | How a request flows through the app |
| [Setup](docs/03-setup.md) | Exact steps from a fresh clone |
| [Status & Roadmap](docs/04-status.md) | What's done, what's next |
