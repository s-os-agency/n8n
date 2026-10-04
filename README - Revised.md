# n8n Operating Stack — plain-language README

## What this is
A ready-to-run setup for n8n, a visual tool for building automations ("when X happens, do Y"). It runs on your own computer or server using Docker. It comes with a database, a job queue and some starter automations.

## Who it's for
Seif, to run the automations behind his businesses. It works with the S-OS command hub and the AgentEmpire dashboard.

## What it does today
- Starts n8n together with PostgreSQL, a database that keeps your automations and their history, and Redis, a queue that lines up jobs.
- Includes a Telegram approval automation (`workflows/telegram-approval.json`). It sends a message with Approve / Reject buttons and acts on the answer.
- On GitHub, it automatically checks that the automation files and the Docker setup are valid (`.github/workflows/validate.yml`).
- Includes guides for putting it online, including on DigitalOcean (`DEPLOY_TO_DO.md`, `PRODUCTION.md`, `SCALING.md`).

## How to run it
You need Docker installed.

```bash
cp .env.example .env      # make your settings file
openssl rand -base64 32   # make a random key; put it in N8N_ENCRYPTION_KEY in .env
docker compose -f docker-compose.local.yml up -d   # start everything
```
Open http://localhost:5678.

After it's running, you can import the command-hub automations from the S-OS repo.

Suggested places to host it, cheapest first:
1. your own computer
2. a rented server (or Coolify)
3. Railway, Render or Fly.io

Only use bigger setups like Kubernetes if you really need them.

## Current status and known gaps
- The local setup and the Telegram approval automation are included.
- These are ideas, not built yet:
  - Monday.com and Gmail approval flows
  - an AI router
  - a Telegram mini-app
  - a revenue dashboard and usage stats
- Whether a live copy is running, and where: not yet confirmed.

## Where things live
| Folder / file | What's in it |
|---|---|
| `workflows/` | Automation files to import into n8n |
| `n8n/` | n8n-specific settings |
| `scripts/` | Helper and check scripts |
| `tests/` | Automated checks |
| `docs/` | Guides, including `docs/CONTROL-SURFACE.md` (a quick overview without opening n8n) |
| `.do/` | DigitalOcean hosting settings |
| `docker-compose.local.yml` | Local setup |
| `.env.example`, `ENV_TEMPLATE.md` | Settings template and explanation |
| `RUNBOOK.md`, `PRODUCTION.md`, `SCALING.md`, `DEPLOY_TO_DO.md` | Running and hosting guides |

License: see `LICENSE`.
