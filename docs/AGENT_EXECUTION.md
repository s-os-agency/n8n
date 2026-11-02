# n8n — Work instructions and current evidence

**Portfolio:** 4/16 (source row 4); **Proposed lead (not dispatched):** Gemini; **specialty:** GCP/n8n operations and provider integrations; **Proposed reviewer (not dispatched):** ChatGPT (Workflow contracts and risk review).
**Repository:** https://github.com/s-os-agency/n8n
**Existing work-item records:** https://docs.google.com/spreadsheets/d/1MMk4Tx0k5rS7e_vOIFg-Dg022VEqXsdwqHibT9-3uOI/edit#gid=20261034
**Existing release record:** https://docs.google.com/spreadsheets/d/1MMk4Tx0k5rS7e_vOIFg-Dg022VEqXsdwqHibT9-3uOI/edit#gid=20261035
**Suggested work:** Check the actual server and workflows; **Proposed human role (not staffed):** Workflow Automation Engineer.

## Execution rule — 2 November 2026

Carry the authorized task through to its requested result. Fill in records while working; a form, named stage, unavailable reviewer or proposed staffing role is not a reason to stop. A check is required only when omitting it would cause a specific failure, break an existing access restriction or exceed the owner's authorization. State that concrete reason.

Use existing authorized access. Do not broaden permissions, disclose credentials or infer approval from silence. If a necessary fact is missing, retrieve it from available sources first. If one action still needs owner input, identify the exact action and continue independent authorized work.

Inspect source and saved changes for documentation work. For a live release, also inspect the provider's deployment result and the running service. Keep source changes, deployment and observed operation as separate facts. Do not add or run software test suites. Record the actual improvement, its evidence and the executing agent. Administrative records may follow execution; they do not create another approval queue.

## Rules for actual work
- Existing root AGENTS.md owner instruction controls: do not add, restore or run software test suites, test-only workflows or scaffolding. Existing spreadsheet references to tests are superseded: obtain real source/build/configuration and operational readback evidence within the owner policy. Never claim tests were run or passed.
- Inspect canonical README, source, existing diffs and deployments before changes. Make the smallest reversible implementation change required. Do not merely write plans or invent launch statuses.
- The named lead is a proposed execution assignment, **not proof of an active external agent session**, OpenRouter invocation, or authority to use another agent's account. A reviewer is an independent second-pass assignment, not an approval already provided.
- Use only scoped provider access actually available. No blind deployment, destructive migrations, new permissions, purchases or exposure of credentials. Preserve backups and rollback.
- Attach evidence URL, UTC date, version/commit, deployed environment and observed result to the corresponding work-item record. Mark VERIFIED only for evidence-backed completion. Leave other gates OPEN; no fabricated real customer, revenue, PayPal or Ziina status.
- Production launch requires a provider-backed deployment receipt and actual live runtime observation, not a green document or UI screenshot.

## Work that still needs evidence

### Work item 4.1 — INVENTORY
**Action:** Check documented GCP host, current production container version, images, databases, queue and backup before changes.
**Acceptance outcome:** Read-only host status, version, db persistence, configuration and backups captured with timestamps.
**Proof needed:** Real source or commit, environment, time and observed result; add independent review only if it actually happened. Record verified results in the existing sheet. **Recorded state: OPEN; not rechecked here.**

### Work item 4.2 — SOURCE
**Action:** Pin version and validate Compose services, migrations, environment requirements and workflow imports.
**Expected result:** Review actual Compose configuration and imports, and capture permitted operational evidence without upgrading production or running software tests.
**Proof needed:** Real source or commit, environment, time and observed result; add independent review only if it actually happened. Record verified results in the existing sheet. **Recorded state: OPEN; not rechecked here.**

### Work item 4.3 — SECURITY
**Action:** Confirm webhook authentication, managed credentials, network/firewall controls and least-privilege accounts.
**Acceptance outcome:** Anonymous access denied to private webhooks, no secrets in logs/source.
**Proof needed:** Real source or commit, environment, time and observed result; add independent review only if it actually happened. Record verified results in the existing sheet. **Recorded state: OPEN; not rechecked here.**

### Work item 4.4 — INTEGRATE
**Action:** Import one approved S-OS command gateway workflow and register idempotent event correlation.
**Acceptance outcome:** Dry-run command flows through webhook and returns exactly one persistent receipt.
**Proof needed:** Real source or commit, environment, time and observed result; add independent review only if it actually happened. Record verified results in the existing sheet. **Recorded state: OPEN; not rechecked here.**

### Work item 4.5 — DEPLOY
**Action:** Start/preserve existing canonical GCP deployment, only change version with restore point and authorized cutover.
**Expected result:** Confirm actual server health, stored Postgres/Redis data and an available rollback procedure without running software tests.
**Proof needed:** Real source or commit, environment, time and observed result; add independent review only if it actually happened. Record verified results in the existing sheet. **Recorded state: OPEN; not rechecked here.**

### Work item 4.6 — LIVE PROOF
**Action:** Trigger safe live workflow, verify execution history survives refresh/restart and failure retry.
**Acceptance outcome:** Timestamped execution ID, output, durable receipt, and controlled retry evidence recorded.
**Proof needed:** Real source or commit, environment, time and observed result; add independent review only if it actually happened. Record verified results in the existing sheet. **Recorded state: OPEN; not rechecked here.**

### Work item 4.7 — COMMERCIAL
**Action:** Only customer-facing service packages require buyer/order evidence; n8n itself is internal delivery runtime.
**Acceptance outcome:** No direct n8n customer or payment claim without customer-level delivery acceptance or settled invoice.
**Proof needed:** Real source or commit, environment, time and observed result; add independent review only if it actually happened. Record verified results in the existing sheet. **Recorded state: OPEN; not rechecked here.**

## How to report completed work
Record completed work and evidence in the existing sheet when available. An unavailable sheet must not stop authorized implementation. Distinguish implementation from launch, customer acceptance from inquiries and settled payments from checkout creation. The lead produces the change receipt; the reviewer checks evidence independently. Report the requested outcome as complete only when its applicable acceptance criteria have direct evidence. Do not make unrelated commercial items or a proposed reviewer prerequisites for internal work. Report any unavoidable external authorization boundary specifically.

**Original document author:** GPT-6. This text does not prove a launch, an agent assignment or any running service.
