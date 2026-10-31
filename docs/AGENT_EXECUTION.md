# n8n — Agent execution instructions

**Portfolio:** 4/16 (source row 4); **Lead agent:** Gemini; **specialty:** GCP/n8n operations and provider integrations; **independent reviewer:** ChatGPT (Workflow contracts and risk review).
**Repository:** https://github.com/s-os-agency/n8n
**Authoritative gates:** https://docs.google.com/spreadsheets/d/1MMk4Tx0k5rS7e_vOIFg-Dg022VEqXsdwqHibT9-3uOI/edit#gid=20261034
**Release dashboard:** https://docs.google.com/spreadsheets/d/1MMk4Tx0k5rS7e_vOIFg-Dg022VEqXsdwqHibT9-3uOI/edit#gid=20261035
**Disposition:** VERIFY / RUN; **accountable proposed engineering role:** Workflow Automation Engineer.

## Mandatory operating rules
- Existing root AGENTS.md owner instruction controls: do not add, restore or run software test suites, test-only workflows or scaffolding. Existing spreadsheet references to tests are superseded: obtain real source/build/configuration and operational readback evidence within the owner policy. Never claim tests were run or passed.
- Inspect canonical README, source, existing diffs and deployments before changes. Make the smallest reversible implementation change required. Do not merely write plans or invent launch statuses.
- The named lead is a proposed execution assignment, **not proof of an active external agent session**, OpenRouter invocation, or authority to use another agent's account. A reviewer is an independent second-pass assignment, not an approval already provided.
- Use only scoped provider access actually available. No blind deployment, destructive migrations, new permissions, purchases or exposure of credentials. Preserve backups and rollback.
- Attach evidence URL, UTC date, version/commit, deployed environment and observed result to the corresponding Exact Completion Gates row. Mark VERIFIED only for evidence-backed completion. Leave other gates OPEN; no fabricated real customer, revenue, PayPal or Ziina status.
- Production launch requires a provider-backed deployment receipt and actual live runtime observation, not a green document or UI screenshot.

## Exact execution order

### Gate 4.1 — INVENTORY
**Action:** Check documented GCP host, current production container version, images, databases, queue and backup before changes.
**Acceptance outcome:** Read-only host status, version, db persistence, configuration and backups captured with timestamps.
**Evidence required:** actual source/commit, environment, timestamp, direct output/receipt, and reviewer; record in sheet. **Initial state: OPEN.**

### Gate 4.2 — SOURCE
**Action:** Pin version and validate Compose services, migrations, environment requirements and workflow imports.
**Acceptance outcome:** Controlled isolated compose start and lint/import tests pass without production upgrade.
**Evidence required:** actual source/commit, environment, timestamp, direct output/receipt, and reviewer; record in sheet. **Initial state: OPEN.**

### Gate 4.3 — SECURITY
**Action:** Confirm webhook authentication, managed credentials, network/firewall controls and least-privilege accounts.
**Acceptance outcome:** Anonymous access denied to private webhooks, no secrets in logs/source.
**Evidence required:** actual source/commit, environment, timestamp, direct output/receipt, and reviewer; record in sheet. **Initial state: OPEN.**

### Gate 4.4 — INTEGRATE
**Action:** Import one approved S-OS command gateway workflow and register idempotent event correlation.
**Acceptance outcome:** Dry-run command flows through webhook and returns exactly one persistent receipt.
**Evidence required:** actual source/commit, environment, timestamp, direct output/receipt, and reviewer; record in sheet. **Initial state: OPEN.**

### Gate 4.5 — DEPLOY
**Action:** Start/preserve existing canonical GCP deployment, only change version with restore point and authorized cutover.
**Acceptance outcome:** Deployment remains healthy; Postgres/Redis persist, rollback documented and tested.
**Evidence required:** actual source/commit, environment, timestamp, direct output/receipt, and reviewer; record in sheet. **Initial state: OPEN.**

### Gate 4.6 — LIVE PROOF
**Action:** Trigger safe live workflow, verify execution history survives refresh/restart and failure retry.
**Acceptance outcome:** Timestamped execution ID, output, durable receipt, and controlled retry evidence recorded.
**Evidence required:** actual source/commit, environment, timestamp, direct output/receipt, and reviewer; record in sheet. **Initial state: OPEN.**

### Gate 4.7 — COMMERCIAL
**Action:** Only customer-facing service packages require buyer/order evidence; n8n itself is internal delivery runtime.
**Acceptance outcome:** No direct n8n customer or payment claim without customer-level delivery acceptance or settled invoice.
**Evidence required:** actual source/commit, environment, timestamp, direct output/receipt, and reviewer; record in sheet. **Initial state: OPEN.**

## Completion handoff
Update each gate's verification state in Google Sheets and attach proof. Distinguish implementation from launch, customer acceptance from inquiries and settled payments from checkout creation. The lead produces the change receipt; the reviewer checks evidence independently. Do not announce completion until all required applicable gates pass. Report any unavoidable external authorization boundary specifically.

**Agent document author:** GPT-6 (instructions only; not a launch attestation).
