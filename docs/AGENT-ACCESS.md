# Agent Access Contract — n8n on GCP

Single source of truth for any agent, worker, or runtime that needs to reach the live n8n instance. Do not hardcode URLs elsewhere; read from here or from the `N8N_BASE_URL` env var it defines.

## Live instance

| Key | Value |
|-----|-------|
| Host (Tailscale) | `100.86.90.80` |
| Public IP | `34.139.100.169` (SSH only — n8n is **not** exposed publicly) |
| Port | `5678` |
| Bind | `127.0.0.1` only |
| Protocol | `http` (Tailscale mesh is already encrypted) |
| Timezone | `Asia/Dubai` |
| Container image | `n8nio/n8n:2.42.3` |
| Compose file | `docker-compose.gcp.yml` (this repo, root) |
| Deploy command | `docker compose -f docker-compose.gcp.yml up -d` |

## Env contract (for connectors)

```bash
N8N_BASE_URL=http://100.86.90.80:5678
N8N_HOST=100.86.90.80
N8N_PROTOCOL=http
N8N_PORT=5678
```

`doneai-daros` already reads `N8N_BASE_URL` via `src/connectors/n8n.connector.js` and pings `/healthz`. New agents should do the same — never embed the IP in code.

## Health endpoints

- Readiness: `GET http://100.86.90.80:5678/healthz/readiness` → expect `200`
- Liveness: `GET http://100.86.90.80:5678/healthz` → expect `200`
- Repo script: `scripts/healthcheck.sh` wraps the same check

## Workflow surfaces (import from `workflows/`)

| File | Role | Trigger |
|------|------|--------|
| `s-orchestrator-hourly.json` | Hourly dispatcher — Route-to-Worker node, HOURLY-ACCEPTANCE protocol (workers must return receipts) | Schedule (hourly) |
| `telegram-approval.json` | Human approval gate over Telegram | Webhook |
| `gmail-approval-template.json` | Gmail-based approval | Template |
| `monday-sync-template.json` | Monday.com sync | Template |
| `ai-router-template.json` | AI routing | Template |
| `n8n-apex-router.workflow.json` | Apex router (lives in `clawi-telegram-runtime`, imports here) | Manual |

Import with: `bash scripts/import-workflows.sh` (or paste JSON in the n8n UI under Workflows → Import).

## Who depends on this

- **doneai-daros** — `n8n.connector.js` health ping + webhook trigger
- **S-OS** — kernel workflows imported into this engine; gateway commands route here
- **AgentEmpire** — operator cockpit consumes n8n for automation actions
- **s-cloudflare-workers** — fleet workers (control-room-feed, migration-auditor, second-brain-keeper, watchdog) coordinate via n8n surfaces
- **OUTS-83** (Assistant Hub hourly engine) — owner of the n8n Scheduler Worker (S-PASS-20260911-005)
- **OUTS-93** (Binance runtime activation) — pending; will use n8n as orchestration layer once live

## Universal agent collaboration and editor onboarding

**Owner authorization (2026-10-24):** The owner invites native-platform agents and S/Agency agents to collaborate via n8n and requests workflow edit capability for each authenticated, compatible agent. Participation is voluntary. This policy is an invitation and authorization to provision scoped access; **it is not evidence that an account, credential, connector, or live permission has been created**.

### Initial invited roster

| Agent or group | Intended role | Verified n8n editor access |
|---|---|---|
| ChatGPT / GPT assistant | Agent collaborator, workflow author/editor | Not verified |
| Gemini | Agent collaborator, workflow author/editor | Not verified |
| Claude / Claude Code | Agent collaborator, workflow author/editor | Not verified |
| Grok | Agent collaborator, workflow author/editor | Not verified |
| Codex | Agent collaborator, workflow author/editor | Not verified |
| Manus | Agent collaborator, workflow author/editor | Not verified |
| Kimi | Agent collaborator, workflow author/editor | Not verified |
| Sovereign | S/Agency orchestrator | Not verified |
| S/Agency specialist agents (as individually identified in the current roster) | Scoped workflow authors/editors | Not verified |

The list is extensible, not exhaustive. Keep each agent's native platform identity distinct; do not assume a model name alone identifies a callable, persistent agent.

### Portable access contract

Any invited agent can opt in using a compatible tool/plugin/MCP/HTTP connector. The agent should be able to discover its capabilities without platform-specific prompt assumptions:

- `GET /capabilities` (future broker contract): return supported operations, connector/auth method, granted scopes, approval requirements, and audit behavior; **not currently deployed**.
- Minimum operations to implement through the authenticated broker: `health`, `list_workflows`, `get_workflow`, `create_workflow`, `update_workflow`, `validate_workflow`, `execute_workflow`, `get_execution`, `get_agent_status`.
- Never claim an operation is available until it has passed an actual connector call. If unsupported, report `unsupported` with reason; if not configured, `unconfigured`; if forbidden, `permission_denied`.
- The user authorizes onboarding and edit capability in principle. Actual n8n editor rights must be provisioned using an authenticated project role or scoped server-side broker, not by this documentation. Keep credentials out of GitHub, browser code, and prompts.
- Production changes require existing approval/audit gates; allow test workflow edits and validation within granted scope. Keep rollback and immutable execution receipts.
- Registry status must be derived from verified events: `invited` → `authenticated` → `read_verified` → `edit_verified`; track last heartbeat, granted scopes, and receipts. Never infer success from an invitation.
- New agents discovered through user interactions may be proposed for registry inclusion, but cannot silently receive credentials or permissions; onboarding needs verified identity and a supported authorization path.

**Integration target:** reuse the existing GCP n8n engine and its private Tailscale route. The portable broker/capability discovery and automatic roster sync are **requirements, not completed features**. Do not expose n8n publicly or bypass approvals to make a platform appear compatible.

## Rules

1. **One URL, one source.** `N8N_BASE_URL` or this file. Nothing else.
2. **No public exposure.** Port 5678 stays on localhost; agents reach it over Tailscale. If you need external access, use Tailscale Funnel deliberately — never open the firewall.
3. **Version pin matters.** `.n8n-version` is canonical. Running box is 2.42.3; repo pin still says 2.3.2 — reconcile before any upgrade (`python3 scripts/validate-versions.py`).
4. **Secrets stay in `.env`** on the box, never in this repo. `.env.example` shows the shape.
5. **DigitalOcean configs are archived** under `zz-ARCHIVE/digitalocean/` — do not deploy from them.

## Quick verify from any agent shell

```bash
curl -s -o /dev/null -w "%{http_code}" http://100.86.90.80:5678/healthz/readiness
# expect: 200
```
