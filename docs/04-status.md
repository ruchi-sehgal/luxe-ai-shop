# 4 · Status & Roadmap

## Done and verified

- [x] FastAPI backend, isolated Python environment
- [x] MongoDB Atlas connection (`/health` endpoint confirms it live)
- [x] `GET /products` reading real data from MongoDB
- [x] 100 products seeded from a spreadsheet, with real images
- [x] Images served at `/images/<filename>`
- [x] Storefront UI: category filter (Men/Women/Kids) + price-range filter
- [x] Git repo initialized, committed, pushed to GitHub
- [x] **Phase 2 — AI chatbot (standalone)**: `POST /chat`, Pydantic AI + Groq,
      natural language → structured `ProductFilter` → MongoDB query → real
      products back. Includes a `Literal` type guard against the AI
      misclassifying fields, an honest `reply` field (no fabricated
      popularity/ratings claims), a capped `limit` (1–20), `total_matches`
      so capped results don't look like the whole answer, and multi-turn
      conversation memory (a follow-up like "what about blue?" correctly
      keeps earlier filters)
- [x] **Phase 3 — integration**: chat widget (toggle button, panel,
      `frontend/src/chat.js`) on the storefront, conversation memory handled
      automatically via a browser-side `history` variable, a zero-result
      fallback that relaxes price → colour → keyword and says so honestly
- [x] **Phase 4 — GCP deployment**: live at
      **https://luxe-ai-shop-web-lmusiuaqbq-el.a.run.app** — Docker image
      built via Cloud Build (no local Docker needed), stored in Artifact
      Registry (`asia-south1`), secrets (`MONGO_URI`, `GROQ_API_KEY`) in
      Secret Manager, running on Cloud Run with a $5 budget alert. Verified:
      storefront, `/health`, `/products` (100 items), and `/chat` all working
      against the real production database

## Not started yet

- [ ] **Phase 2b — Pydantic Evals**: an offline eval suite (a golden set of
      real queries with their expected filter) that runs before every change
      to the chatbot is trusted — catches regressions instead of eyeballing
      a few test messages
- [ ] **Phase 4b — CI/CD**: a Cloud Build trigger wired to GitHub, so every
      `git push` to `main` automatically builds and redeploys — no manual
      deploy steps after initial setup
- [ ] **Phase 5 — RAG layer (hybrid)**: added on top of Phase 2's structured
      filtering, not a replacement. Exact fields (price, category, colour)
      stay as MongoDB queries. Vector search over product descriptions
      handles vibe/style requests with no matching field (e.g. "something
      elegant for a beach wedding") that the current agent can't catch

## Deliberately out of scope (for now)

Not part of this build unless asked for separately — the proposal's core ask
is the catalogue + chatbot, not a full e-commerce platform:

- User accounts / sign-in
- Cart / checkout / orders
- Admin product management UI
- Guardrails, tracing, eval suite (the proposal's security/observability
  layers — real and worth adding once the basic chatbot works)

## A detailed build log

A running, more narrative log of every step taken — including the
debugging detours — is kept separately: see the conversation history, or
ask for it to be exported here.
