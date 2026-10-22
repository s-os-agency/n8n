# n8n Operating Stack

Version policy: all n8n and runner images use the explicit pin in
[.n8n-version](.n8n-version). See [VERSION.md](VERSION.md) before deploying or
recovering an existing instance; the running production version is unverified.


[![Stack](https://img.shields.io/badge/part%20of-Operator%20Stack-0f766e)](docs/ECOSYSTEM.md)
[![Pairs with](https://img.shields.io/badge/control%20plane-S--OS-blue)](https://github.com/saifsoub/S-OS)
[![Cockpit](https://img.shields.io/badge/cockpit-AgentEmpire-purple)](https://github.com/saifsoub/AgentEmpire)
[![Live host](https://img.shields.io/badge/live-GCP%2034.139.100.169-green)](DEPLOY_TO_GCP.md)

**Canonical deployment: GCP VM** at 34.139.100.169 (Tailscale 100.86.90.80).
n8n 2.42.3 in Docker, localhost:5678, Postgres + Redis. Full runbook:
[DEPLOY_TO_GCP.md](DEPLOY_TO_GCP.md). Compose: [docker-compose.gcp.yml](docker-compose.gcp.yml).

DigitalOcean App Platform specs are **parked** under
[zz-ARCHIVE/digitalocean/](zz-ARCHIVE/digitalocean/) — not for deployment.

Part of the **Operator Stack** — see [docs/ECOSYSTEM.md](docs/ECOSYSTEM.md):

| Repo | Role |
|------|------|
| [S-OS](https://github.com/saifsoub/S-OS) | Control plane (gateway, registry, schemas) |
| **n8n** (this repo) | Workflow engine + ops runbooks |
| [AgentEmpire](https://github.com/saifsoub/AgentEmpire) | Operator dashboard UI |

Import kernel workflows from **S-OS** into this n8n instance after the stack is up.

---

A practical local-first n8n operating repository for:

- Telegram approval workflows
- Revenue operations
- AI automation pipelines
- Persistent PostgreSQL-backed workflows
- Redis queue execution
- Docker-based deployment
- GitHub CI validation

---

## Quick Start (GCP box)

```bash
ssh ubuntu@34.139.100.169
cd /opt/n8n   # or wherever the repo is checked out on the box
cp .env.example .env   # fill secrets
openssl rand -base64 32  # set N8N_ENCRYPTION_KEY
docker compose -f docker-compose.gcp.yml up -d
```

Open via Tailscale: `http://100.86.90.80:5678`

---

## Included

### Infrastructure

- n8n (GCP, canonical)
- PostgreSQL
- Redis
- Docker local stack (`docker-compose.local.yml`)
- Docker GCP stack (`docker-compose.gcp.yml`)
- GitHub validation CI

### Workflow Assets

- Telegram approval workflow
- Workflow import/export directory
- Persistent workflow volume

### Governance

- JSON validation in CI
- Docker compose validation
- Environment template
- Local-first execution

---

## Operator Layer

See:

```txt
docs/CONTROL-SURFACE.md
```

This gives operators and agents a lightweight operational overview without opening n8n first.

---

## Repo Structure

```txt
.github/workflows/       CI validation
workflows/               n8n workflow JSON files
scripts/                 runtime and validation helpers
docs/                    operations and governance
.env.example             environment template
docker-compose.local.yml local runtime stack
docker-compose.gcp.yml   canonical GCP runtime stack
DEPLOY_TO_GCP.md         live deployment runbook
zz-ARCHIVE/digitalocean/ parked DO App Platform specs
```

---

## Telegram Approval Workflow

Included:

```txt
workflows/telegram-approval.json
```

Capabilities:

- Telegram trigger
- Inline approval buttons
- Approval/reject callbacks
- Foundation for agent approvals

---

## Production Notes

Recommended runtime order:

1. Local Docker
2. GCP VM (current)
3. VPS or Coolify
4. Railway / Render / Fly.io
5. Kubernetes only when scale actually requires it

Avoid unnecessary recurring infrastructure costs during early operations.

---

## Validation

GitHub Actions validates:

- Workflow JSON syntax
- Docker compose structure

Workflow file:

```txt
.github/workflows/validate.yml
```

---

## Next Recommended Extensions

- Monday.com integration
- Gmail approval flows
- AI routing agent
- Telegram mini app
- Revenue dashboard
- Workflow execution analytics
- Human approval gates
- Queue workers
- External webhook registry
- Point n8n at MariaDB (already running on the GCP box) instead of Postgres

---

## Philosophy

This repository is designed for:

- operational truth
- low-friction deployment
- real workflow execution
- persistent automation
- zero-fluff infrastructure
