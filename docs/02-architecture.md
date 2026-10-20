# 2 · Architecture

## How a request flows right now

```mermaid
flowchart LR
    B["Browser"] -->|GET /| M["main.py (FastAPI)"]
    M -->|static files| F["frontend/ (HTML/CSS/JS)"]
    B -->|GET /products| M
    M --> R["backend/routes/products.py"]
    R --> DB[("MongoDB Atlas\nluxe_shop.products")]
    B -->|GET /images/...| M
    M -->|static files| I["static/images/"]
```

- `main.py` is the single entry point. It registers routes in a deliberate order:
  1. `app.include_router(products.router)` — `/products`, handled by Python code
  2. `app.mount("/images", ...)` — anything under `/images/` is served straight from disk
  3. `app.mount("/", ...)` — everything else falls through to the `frontend/` folder (registered **last**, so it never shadows the two routes above it)
- `backend/config.py` reads `.env` once into a typed `Settings` object at startup.
- `backend/database.py` opens one MongoDB connection (`db`), imported by every route that needs it.
- `frontend/src/main.js` fetches `/products` once, stores the full list in memory, and re-filters it client-side as category/price buttons are clicked — no repeated network calls per click.

## Where Phase 2 (the chatbot) plugs in

```mermaid
flowchart LR
    B["Browser"] -->|POST /chat, a sentence| M["main.py"]
    M --> C["backend/chatbot/agent.py"]
    C -->|writes a MongoDB filter| DB[("MongoDB Atlas")]
    DB -->|matching products| C
    C --> M
    M -->|products, JSON| B
```

One new endpoint, one new file. Nothing about the store (routes, database
connection, frontend) changes — the chatbot is additive.

## Identity note

There are currently no user accounts, carts, or orders — this build is
scoped to what the proposal actually needs: a browsable catalogue and a
chatbot that queries it. Accounts/cart/checkout are not part of this build
unless asked for separately.
