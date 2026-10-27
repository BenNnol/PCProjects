# AGENTS.md

## What this project is

PCProjects is a small FastAPI service: a status page at `/` plus the JSON
payload it renders at `/api/info` (also exposed as interactive docs at `/docs`).

## Running it (sandbox / preview)

```sh
docker compose -f docker-compose.base44.yml up -d --build
```

- One service, `web`, built on the plain `python:3.12-slim` image with the repo
  bind-mounted at `/app`. It runs the app via `uvicorn --reload` from the
  cloned source — never a prebuilt image — so code edits are picked up live.
- Host port 3000 maps to the container's 8000, which is what the preview shows.
- **Dependencies are installed at container start**, not baked into an image:
  the compose command runs `pip install -r requirements.txt` before `exec`-ing
  uvicorn. So after adding or changing a dependency, recreate the service
  (`docker compose -f docker-compose.base44.yml up -d --build`) — a plain file
  edit and live reload will not install it.
- `.env`-style secrets are not needed: the app talks to no external service.
  If that changes, wire `/run/base44/app.env` in as the **last** `env_file:`
  entry in compose rather than using `environment:` (which would outrank it).

## Verifying it works

```sh
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/          # 200, HTML
curl -s http://localhost:3000/api/info                                   # JSON status payload
docker compose -f docker-compose.base44.yml ps                           # web should be (healthy)
```

The compose healthcheck probes `/api/info` (a real app endpoint — no
health-only route was added to the app), so `(healthy)` means the app itself
answers, not just that the port is open.

## Tests

```sh
docker compose -f docker-compose.base44.yml exec -T web python -m pytest -q
```

Tests live in `tests/` and run inside the `web` container — the sandbox host has
no Python runtime of its own.

## Notes

- No sandbox-specific code or host/origin allowlist overrides are required:
  uvicorn and FastAPI accept any `Host`/`Origin` by default, and the page and
  its JSON API are same-origin. `BASE44_PREVIEW_MODE` is therefore unused here;
  if a future change needs host/origin gating, gate it on
  `os.getenv("BASE44_PREVIEW_MODE") == "1"` and keep the original behaviour when
  it is unset.
- `README.md` at the repo root is GitHub profile boilerplate, unrelated to this
  service; it was left untouched.
