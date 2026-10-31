# Manus n8n ↔ server worker routing

## Canonical deployment (do not reinstall)
- n8n source: [this repository](https://github.com/s-os-agency/n8n), `docker-compose.gcp.yml`; container `n8nio/n8n:2.42.3` was last verified on the **Manus** host `cloud-pc-a50933c6` on 2026-10-30. Bind stays `127.0.0.1:5678`. Preserve Postgres, Redis, n8n volume, encryption key and current workflow state; do not replace them with the separate workers' MariaDB.
- Existing server runtime: [SS-agentic-ai-factory](https://github.com/s-os-agency/SS-agentic-ai-factory) supervised by `ss-agentic-ai-factory.timer`, with bounded handlers and execution receipts. Its current worker registry, portfolio and receipts persist in **Manus MariaDB**.
- Worker fleet source of truth: [s-cloudflare-workers](https://github.com/saifsoub/s-cloudflare-workers), not S-OS or an n8n fork. Cloudflare workers retain their existing cloud execution environment; do not migrate them onto Manus to count them active.
- Governance/control: [S-OS](https://github.com/saifsoub/S-OS) and Agent Passport; project control via Workers Control and S/PM.
- Agent and workflow access rules: [docs/AGENT-ACCESS.md](AGENT-ACCESS.md) and [docs/HOURLY-ACCEPTANCE.md](HOURLY-ACCEPTANCE.md).

## Safe read-only runtime check

On the **existing Manus server** (not an arbitrary CI runner), in this repository checkout:

```bash
node scripts/audit-server-worker-runtime.mjs
```

The audit checks the local n8n readiness URL, factory timer state and actual running Docker containers; emits a machine-readable JSON receipt with observation time, observed status and error classification. Exit 0 means these **three local checks** passed; it does **not** mean all workers in all repositories are active.

## Runtime activation requirements by repository

| Repository / group | Existing authority | Operational acceptance |
| --- | --- | --- |
| `s-os-agency/n8n` | n8n persisted workflows and existing compose | Container readiness, canonical workflow enabled only after its acceptance tests, actual execution receipts |
| `s-os-agency/SS-agentic-ai-factory` | Manus timer, server-side handlers and MariaDB receipts | Timer running, real job claims/executions/receipts; verified consumer link from n8n when a workflow is enabled |
| `saifsoub/s-cloudflare-workers` | Cloudflare's existing worker fleet | Each deployed worker's platform status/heartbeat/real outcome, without moving its source or hosting |
| `saifsoub/S-OS` and `s-agent-passport` | Governing orchestration and identity | Verified dispatch, authorized passport, real execution receipt |
| Other repository workloads | Existing 77-repository registry on Manus | Reconcile exact checkout/runner, service identity, passport, fresh heartbeat and execution evidence individually; do not infer from a repository's presence |

**No broad auto-activation on import:** n8n's hourly workflow explicitly remains NOT ACTIVE until live manual and scheduled acceptance, independent approvals and write-back receipts pass. No superseded workflow is automatically re-enabled. Do not claim the 43 registered workers are all running: the stored roster states, runtime heartbeats and deployed processes are distinct. Link workers using existing private authenticated gateway and `N8N_BASE_URL` contract, never public port 5678, credential commits or per-agent duplicated orchestration.

## Evidence boundary

Last historical verified Manus runtime (2026-10-30): n8n, university and gateway returned HTTP 200 in a timer health receipt, and MariaDB receipts were being recorded. This document links sources and adds a read-only checker. It does **not** certify a fresh server audit, all 77 repositories activated, or a newly deployed n8n workflow. Only a fresh host-side receipt can establish those outcomes.
