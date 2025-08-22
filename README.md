# NoBroker — Full‑Stack Rental Platform

A full‑stack application for broker‑free property rentals. Owners list properties; tenants search, shortlist, and apply.

- Backend: FastAPI + SQLAlchemy
- DB: PostgreSQL (Docker) or SQLite (fallback for local)
- Frontend: React (Vite)
- Containerization: Docker + docker‑compose

---

## Repository Structure

```
.
├─ client/
│  └─ web/                 # React (Vite) frontend
├─ server/                 # FastAPI backend
│  ├─ api/                 # Routers (auth, properties, etc.)
│  ├─ core/                # Config, settings
│  ├─ db/                  # DB session & init
│  ├─ models/              # SQLAlchemy models
│  ├─ schemas/             # Pydantic schemas
│  ├─ services/            # Business logic
│  ├─ tests/               # Backend tests
│  ├─ main.py              # FastAPI app entrypoint
│  ├─ pyproject.toml       # Python deps (managed with uv)
│  ├─ uv.lock              # Locked dependency graph
│  └─ .env.example         # Sample backend env
├─ product/                # Product docs (specs, APIs, architecture)
├─ Dockerfile              # Multi‑stage build (frontend + server)
├─ docker-compose.yml      # Services: db, api, web (dev)
└─ README.md               # This file
```

---

## Services & Ports

From `docker-compose.yml`:

- db (PostgreSQL): host `localhost:5433` → container `5432`
- api (FastAPI/Uvicorn): `http://localhost:8000`
- web (Vite dev server): `http://localhost:5174` (proxied from container 5173)

Notes:
- CORS is configured in `server/main.py` to allow `http://localhost:5173` and `http://localhost:5174`.
- The Dockerfile also builds the frontend and copies artifacts to `/app/server/static`. For development we use the `web` service; serving built assets from FastAPI can be enabled later if desired.

---

## Quick Start (Docker)

Requirements: Docker + Docker Compose

1) Copy backend env file and edit values as needed.
```bash
cp server/.env.example server/.env
```

2) Start everything (builds images on first run):
```bash
sudo docker compose up -d --build
```

3) Verify containers:
```bash
sudo docker compose ps
```

4) Open the apps:
- Frontend (dev): http://localhost:5174
- API root: http://localhost:8000/
- API docs (Swagger): http://localhost:8000/docs
- API docs (ReDoc): http://localhost:8000/redoc

5) View logs (follow mode):
```bash
sudo docker compose logs -f web
sudo docker compose logs -f api
sudo docker compose logs -f db
```

6) Stop services:
```bash
sudo docker compose down
```

---

## Environment Configuration (Backend)

Backend settings live in `server/core/config.py` using Pydantic Settings (v2). Default `.env` path is `server/.env`.

Key variables:
- SECRET_KEY: JWT secret (required)
- DATABASE_URL: e.g. `postgresql+psycopg2://nb:nb@db:5432/nb`
- or DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD (compose alternative)
- ENVIRONMENT, DEBUG, APP_NAME, APP_VERSION, APP_DESCRIPTION

Behavior:
- If `DATABASE_URL` is missing and DB_* parts are incomplete, the app falls back to SQLite: `sqlite:///./app.db` (dev convenience).

Compose injects:
- PYTHONPATH=/app
- STATIC_FILES_DIR=/app/server/static

See `server/.env.example` for a full template.

---

## Development Workflow

### Frontend (Vite)
- Live dev server is provided by the `web` service at http://localhost:5174
- Source path: `client/web/`
- Typical local run (without Docker):
  ```bash
  cd client/web
  pnpm install
  pnpm dev --host
  ```

### Backend (FastAPI)
- Source path: `server/`
- With Docker: handled by `api` service on port 8000
- Typical local run (without Docker, if you prefer):
  ```bash
  cd server
  # Install uv (https://github.com/astral-sh/uv) or use pip
  uv sync
  uv run uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
  ```

### Database
- Postgres runs in `db` container.
- Host connection string (from your machine):
  - Host: `localhost`
  - Port: `5433`
  - User: `nb`, Password: `nb`, DB: `nb`
- Inside compose network (containers):
  - Host: `db`
  - Port: `5432`

---

## Building the Production Image

The `Dockerfile` is a multi‑stage build:
1) client-builder: installs frontend deps and runs `pnpm build` (Vite → `/app/dist`).
2) server: installs Python deps with `uv` and copies built frontend to `/app/server/static`.

For a fresh build of the API image:
```bash
sudo docker compose build api
sudo docker compose up -d api
```

Note: `server/main.py` currently returns JSON on `/`. To serve the built frontend from FastAPI, you can mount `StaticFiles` and serve `index.html` (optional for production since the dev `web` service is used during development).

---

## Common Docker Commands

- Follow logs
  ```bash
  sudo docker compose logs -f api
  sudo docker compose logs -f web
  sudo docker compose logs -f db
  ```
- Show last N lines and follow
  ```bash
  sudo docker compose logs --tail=100 -f api
  ```
- Restart a service
  ```bash
  sudo docker compose restart api
  ```
- Rebuild a service
  ```bash
  sudo docker compose up -d --build api
  ```

If you want to avoid `sudo`, add your user to the `docker` group and re‑login:
```bash
sudo usermod -aG docker "$USER"
```

---

## API Overview

See product docs:
- `product/spec.md` — Product scope & user stories
- `product/architecture.md` — System & DB design
- `product/api_spec.md` — Endpoint details

FastAPI interactive docs:
- Swagger UI: `GET /docs`
- ReDoc: `GET /redoc`

Auth highlights:
- `POST /auth/register` — Register tenant/owner
- `POST /auth/login` — JWT login

Properties:
- `GET /properties` — Search/filter
- `POST /properties` — Create (owner)
- `GET /properties/{id}` — Detail

Shortlist:
- `POST /me/shortlist`, `GET /me/shortlist`, `DELETE /me/shortlist/{property_id}`

Applications:
- `POST /applications`, `GET /applications`, `PUT /applications/{id}`

---

## Testing

Backend tests live under `server/tests/`.
- With Docker (exec into API container and run):
  ```bash
  sudo docker compose exec api sh -lc "uv run pytest -q"
  ```
- Locally:
  ```bash
  cd server
  uv run pytest -q
  ```

---

## Troubleshooting

- Frontend CORS errors from dev server
  - Ensure `server/main.py` `allow_origins` includes `http://localhost:5174`.
  - Hard refresh the browser (Ctrl+Shift+R).

- API can’t reach Postgres
  - Check `server/.env` → `DATABASE_URL` or DB_* variables.
  - Confirm DB is healthy: `sudo docker compose ps` shows `db` healthy.

- Port conflicts
  - DB uses host 5433. Change in `docker-compose.yml` if needed.

- Logs show preflight (OPTIONS) 400
  - CORS `allow_methods=['*']` and `allow_headers=['*']` are set; confirm origins list and rebuild API service.

---

## Contributing

- Use feature branches and pull requests.
- Keep code formatted and linted (frontend via Vite/ESLint, backend via your editor/linters).
- Add or update tests under `server/tests/` for backend changes.

---

## License

Proprietary or TBD.
