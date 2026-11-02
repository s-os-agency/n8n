# Access to the private n8n server

This file explains how authorized agents connect to the existing n8n server. It does not give anyone access or prove that a connection works.

Use `N8N_BASE_URL` for the server address in code. Do not copy the IP address into other source files.

## Server details

| Setting | Value |
|---|---|
| Private Tailscale address | `100.86.90.80` |
| Public IP | `34.139.100.169` (SSH only; n8n is not public) |
| Port | `5678` |
| Bind address | `127.0.0.1` only |
| Connection | `http` over encrypted Tailscale |
| Timezone | `Asia/Dubai` |
| Last documented container image | `n8nio/n8n:2.42.3` |
| Compose file | `docker-compose.gcp.yml` |
| Start command | `docker compose -f docker-compose.gcp.yml up -d` |

These are documented settings, not a fresh check of the running server.

## Settings for connected services

```bash
N8N_BASE_URL=http://100.86.90.80:5678
N8N_HOST=100.86.90.80
N8N_PROTOCOL=http
N8N_PORT=5678
```

`doneai-daros` reads `N8N_BASE_URL` in `src/connectors/n8n.connector.js`. Other integrations should read the same setting rather than store the address in code.

## Check whether the server responds

- `GET /healthz/readiness`: a responding server should return HTTP 200 when ready.
- `GET /healthz`: a responding server should return HTTP 200.
- `scripts/healthcheck.sh` provides the existing health check.

These are connection checks, not evidence that any agent has editing permission. No check was run as part of this documentation edit.

## Existing workflow files

| File | Purpose | How it starts |
|---|---|---|
| `s-orchestrator-hourly.json` | Assigns hourly work and asks workers to report results; existing names include `Route-to-Worker` and `HOURLY-ACCEPTANCE` | Hourly schedule |
| `telegram-approval.json` | Requests a person's approval through Telegram | Webhook |
| `gmail-approval-template.json` | Example Gmail approval workflow | Template |
| `monday-sync-template.json` | Example Monday.com sync | Template |
| `ai-router-template.json` | Example AI work routing | Template |
| `n8n-apex-router.workflow.json` | Existing router from `clawi-telegram-runtime` | Manual |

To import a workflow, use `bash scripts/import-workflows.sh` or n8n's Workflows → Import option. A file in this repository does not prove its workflow is imported or running.

## Projects that use or intend to use n8n

- **doneai-daros:** Connector for checking n8n and triggering webhooks.
- **S-OS:** Intended place for core workflows and commands.
- **AgentEmpire:** Uses or plans n8n automation actions.
- **s-cloudflare-workers:** Workers intended to coordinate through n8n.
- **OUTS-83:** Existing reference for Assistant Hub's hourly scheduling worker (`S-PASS-20260911-005`).
- **OUTS-93:** Binance activation work is pending; do not call it connected or live without evidence.

Descriptions of intended use are not proof of a live connection.

## Who may request editing access

**Owner instruction, 24 October 2026:** Seif invites compatible platform agents and S/Agency agents to work together through n8n. He authorizes arranging properly limited workflow editing access for agents that authenticate successfully. This invitation does **not** create an account, password, connection or permission.

| Invited agent or group | Intended work | Verified n8n editor access |
|---|---|---|
| ChatGPT / GPT assistant | Workflows | Not verified |
| Gemini | Workflows | Not verified |
| Claude / Claude Code | Workflows | Not verified |
| Grok | Workflows | Not verified |
| Codex | Workflows | Not verified |
| Manus | Workflows | Not verified |
| Kimi | Workflows | Not verified |
| Sovereign | Coordinate S/Agency work | Not verified |
| Individually identified S/Agency agents | Workflows within their approved access | Not verified |

Other agents may be invited later. Each agent must have an identifiable, authenticated account or supported connection. A model's name alone is not proof of identity or access.

## How agent access should work

1. Confirm the agent's identity and supported connection method. It may use an authorized plugin, MCP connection or HTTP service.
2. Give it only the permissions it needs through an authenticated n8n project role or a properly secured server-side service. **This document grants no permissions.**
3. Confirm what the actual connection can do before claiming it can read, create, edit or run a workflow.
4. Keep credentials out of GitHub, browser code and prompts. Keep existing production approval requirements and records of changes. Do not bypass owner authorization.
5. If an operation is unavailable, say why: `unsupported`, `unconfigured` or `permission_denied`. Do not report an invitation as a successful connection.
6. Record only real steps completed, such as an authenticated connection, a confirmed read or a confirmed edit. Do not assume the next step happened.
7. A newly discovered agent must not receive credentials or editing rights automatically.

**Not implemented or verified here:** A future `GET /capabilities` endpoint that would show available operations, authentication, allowed actions, approval rules and records. The proposed server-side connection would support `health`, `list_workflows`, `get_workflow`, `create_workflow`, `update_workflow`, `validate_workflow`, `execute_workflow`, `get_execution` and `get_agent_status`. These are proposed interface names, **not proof that the functions exist**. Automatic agent-list updates are also not verified.

Use the existing private GCP n8n server and Tailscale connection. Do not create a second server, expose this one publicly or weaken approval rules to make a connection seem ready.

## Rules that must remain in force

1. Use `N8N_BASE_URL` or this file for the address.
2. Keep port `5678` private. Access is through Tailscale; do not open the public firewall. Tailscale Funnel would need a deliberate, separately authorized decision.
3. Check the version before upgrading. The last documented running image is `2.42.3`, but `.n8n-version` says `2.3.2`. Resolve that difference before any upgrade. The existing command is `python3 scripts/validate-versions.py`; do not treat a documented command as something run.
4. Keep secrets in the server's `.env`, never in this repository. `.env.example` lists expected setting names.
5. Do not deploy archived DigitalOcean files under `zz-ARCHIVE/digitalocean/`.
6. Follow the owner's 25 October 2026 ban: do not add, restore or run software tests, test suites, test workflows or test-only tooling. Inspect source, saved changes and existing operational evidence instead. Do not claim tests passed.

## Optional manual connection check

```bash
curl -s -o /dev/null -w "%{http_code}" http://100.86.90.80:5678/healthz/readiness
```

Expected response, when connected and ready: `200`. This command is an example, not a record that it was executed.
