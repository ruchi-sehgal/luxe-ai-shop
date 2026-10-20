# 4 · Status & Roadmap

## Done and verified

- [x] FastAPI backend, isolated Python environment
- [x] MongoDB Atlas connection (`/health` endpoint confirms it live)
- [x] `GET /products` reading real data from MongoDB
- [x] 100 products seeded from a spreadsheet, with real images
- [x] Images served at `/images/<filename>`
- [x] Storefront UI: category filter (Men/Women/Kids) + price-range filter
- [x] Git repo initialized, committed, pushed to GitHub

## Not started yet

- [ ] **Phase 2 — AI chatbot (standalone)**: `POST /chat`, Pydantic AI + Groq,
      natural language → MongoDB filter → real products back
- [ ] **Phase 3 — integration**: chat widget on the storefront itself
- [ ] **Phase 4 — GCP deployment**: Artifact Registry, Secret Manager, Cloud
      Build, Cloud Run

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
