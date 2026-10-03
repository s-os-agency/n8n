# Assistant Control hourly acceptance

Status: NOT ACTIVE until manual and scheduled runs have independently confirmed
write-back. Repository tests and gateway responses are preflight evidence only.

## Canonical path

Import `workflows/s-orchestrator-hourly.json`. PR #4's bounded routing, decisions,
archive, silent hold, audit and source-row linking use main's S-OS invocation
transport. `orchestrator-hourly-invoke.json` and the PR-only
`assistant-control-hourly-follow-up.json` are superseded. Inventory and deactivate
existing runtime copies before enabling the canonical workflow; deleting a source
file does not deactivate an imported workflow. Preserve execution history.

Select at most five rows in priority order. Obsolete/cancelled rows now reach
archive; sorted rows retain n8n item links. Failed/unverified delivery writes
`delivery_failed` and requires reconciliation before retrying the same revision.

Execute requires Authorized=yes, Approval Status=approved, a nonempty Approval
Reference, and a parseable Updated At revision. Add the two approval columns
after existing A:X without renaming or moving current columns. Missing approval
evidence holds work silently. Do not populate unrelated live rows with approval.
The server must independently validate the reference against the exact action,
owner, scope and expiry. Sheet labels do not grant server authority.

## Private bindings

Use the existing `s-srv-google-001` runtime and verified n8n version. Preserve
private management access, volumes, encryption key and existing credentials.

| Binding | Scope |
| --- | --- |
| Existing Google Sheets credential | This workbook only: read Control, append Activity, update selected source rows |
| ASSISTANT_CONTROL_SHEET_ID | Existing S/ Live Command Sheet ID |
| S_AGENTOS_COMMAND_URL | Verified private executor/adapter; no implicit localhost fallback |
| S_AGENTOS_OPERATOR_KEY | Existing scoped runtime authority |
| ASSISTANT_SEIF_ESCALATION_URL | Governed decision endpoint; acceptance uses a capture sink |
| ASSISTANT_SEIF_ESCALATION_TOKEN | Existing scoped decision credential |
| ASSISTANT_ACCEPTANCE_TASK_IDS | Comma-separated synthetic IDs; excludes all real tasks |

Bind placeholder Sheets IDs privately. If the deployed n8n policy denies these
environment expressions, use scoped credentials/configuration instead of changing
global access controls. Never paste secrets into GitHub, Sheets or Linear. Do not
add paid services or expand endpoint permissions.

The main S-OS JSON gateway resolves routes without executing them. That template
alone cannot pass. The executor/adapter must validate approval references and
durably deduplicate idempotency_key before effects; replay after lost write-back
must return the same effect receipt. Do not claim a server-side lease/dedup gate
from this workflow's cooldowns.

HTTP 2xx alone is insufficient. Executor response contract:

```json
{
  "ok": true,
  "receipt": {
    "id": "safe-receipt-id",
    "taskId": "AC-accept-execute",
    "runId": "actual-n8n-execution-id",
    "idempotency_key": "ac:AC-accept-execute:actual-revision",
    "approval_reference": "independently-validated-approval-id",
    "status": "accepted"
  }
}
```

Accepted proves dispatch, not completion; completed requires a final worker
receipt. The decision sink must return ok:true and a safe receipt ID bound to
taskId/runId. Raw bodies, tokens and transport-error messages are excluded from
the eight audit cells. There are no automatic transport retries.

## Controlled acceptance

1. Record exact repo SHA, imported workflow ID/hash, pinned runtime version,
   prior active workflows and health. Verify executor approval validation,
   durable idempotency and the receipt adapter with a harmless synthetic action.
2. Add four unique synthetic rows in Control: approved execute, ordinary pending
   hold, decision capture, obsolete archive. Bind private endpoints and the
   existing Sheets credential. Set the acceptance allowlist to those four IDs.
   Never dispatch real work or send synthetic notifications to Seif.
3. Run Manual Evidence Run while inactive. Verify all four outcomes, one actual
   worker receipt, no hold notification, captured decision and Archived status.
   Independently read actual Activity and Control cells using the Sheets
   connection; correlate task IDs, run ID, times, dispositions and execution URLs.
4. After manual PASS, prepare fresh synthetic rows/approved revisions and update
   the acceptance allowlist. Cooldown-suppressed or already Archived rows cannot
   count as scheduled branch coverage.
5. Enable only the canonical Every Hour schedule and wait for its real interval.
   Do not shorten the schedule or substitute manual/API invocation. Retain the
   execution's schedule origin, start/end time, workflow ID, Every Hour run data,
   and actual worker/sink receipts.
6. Independently read back Activity and Control cells for that scheduled run.
   Only successful correlated write-back closes scheduled proof. Record it in
   OUTS-83 and the canonical sheet row. On failure, keep NOT ACTIVE and deactivate
   the acceptance schedule.
7. Keep the synthetic allowlist while observing the next scheduled run required
   by the current sheet gate. Broader operation is a separate readiness step;
   clearing the allowlist must not silently authorize live project actions.

Recovery: deactivate acceptance, retain receipts and volumes, reconcile effects
before retry, and restore the previous inactive definition if necessary. Do not
automatically re-enable either superseded hourly workflow.
