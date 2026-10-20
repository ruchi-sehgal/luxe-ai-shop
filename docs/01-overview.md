# 1 · Overview

## What is LUXE?

LUXE is a clothing store built for a retail client who already has a MongoDB
product catalogue. The goal: a browsable storefront, plus an AI shopping
assistant that turns a plain-English request ("white shirt under 2000") into
a real database query, instead of making shoppers click through category and
price filters by hand.

Built in stages, each one working end to end before the next starts:

1. **The store** — real product data, a backend API, a browsable frontend. *(done)*
2. **The chatbot** — a standalone endpoint that turns a sentence into a MongoDB filter. *(not started)*
3. **Integration** — the chatbot becomes a chat widget on the storefront. *(not started)*
4. **Deployment** — the whole thing running on Google Cloud Run. *(not started)*

## Why no vector database / RAG?

The product catalogue is small and structured (name, category, price, sizes,
colours) — exactly the shape a database query already handles well. The AI's
job is narrow: read a sentence, write one MongoDB filter, done. That's a
**text-to-filter** problem, not a retrieval problem — no embeddings, no
chunking, no vector index. One LLM call, one tool call, real data back.

## Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | FastAPI (Python) | Turns Python functions into HTTP endpoints; automatic interactive docs at `/docs` |
| Database | MongoDB Atlas | Matches the client's existing database; free tier is enough for this build |
| Frontend | Plain HTML/CSS/JS, no build step | Loads instantly, nothing to compile — matches how a chat widget would later drop into a real client site as a single script tag |
| Config | `pydantic-settings` | Reads `.env` into one typed, validated object instead of scattered `os.environ` calls |
| AI agent *(Phase 2)* | Pydantic AI + Groq | Structured, typed tool calls; Groq's free tier avoids per-request cost while learning |
| Hosting *(Phase 4)* | Google Cloud Run | Scales to zero when idle; deployed via Cloud Build, no servers to manage |

## Data

Products live in MongoDB Atlas, database `luxe_shop`, collection `products`.
Each document looks like:

```json
{
  "name": "Classic Black Tee",
  "description": "Soft cotton crew-neck t-shirt for everyday wear.",
  "price": 499,
  "category": "men",
  "sizes": ["S", "M", "L", "XL"],
  "colours": ["Black"],
  "image_url": "/images/classic_black_tee.jpg"
}
```

Seeded from `seed_data/bulk_upload.xlsx` via `seed_data/seed.py`. Product
images live in `static/images/` and are served directly by the backend at
`/images/<filename>`.
