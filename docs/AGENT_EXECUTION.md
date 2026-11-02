# n8n — Finish the work

Use the existing n8n server and the owner's current instructions in [AGENTS.md](../AGENTS.md). Complete authorized work without waiting for a form, a named stage, a proposed reviewer or a staffing assignment. If one action cannot proceed, state the specific missing access or fact and continue the work that can.

## Existing records

- Repository: https://github.com/s-os-agency/n8n
- Work items: https://docs.google.com/spreadsheets/d/1MMk4Tx0k5rS7e_vOIFg-Dg022VEqXsdwqHibT9-3uOI/edit#gid=20261034
- Release results: https://docs.google.com/spreadsheets/d/1MMk4Tx0k5rS7e_vOIFg-Dg022VEqXsdwqHibT9-3uOI/edit#gid=20261035
- Server connection instructions: [AGENT-ACCESS.md](AGENT-ACCESS.md)

The earlier portfolio assignment named Gemini as a proposed lead and ChatGPT as a proposed reviewer. Those labels do not establish access or a running session. Use the agent that has the required authorized tools. An unavailable reviewer must not stop implementation.

## Working rules

- Read the current source, changes and service configuration before editing. Preserve work already completed by another agent.
- Use existing authorized access. Do not expand permissions, reveal credentials or treat silence as approval.
- Make the smallest reversible change that completes the requested task. Preserve the existing service, data and recovery copy.
- Do not create, restore or run software tests, test commands, test workflows or test-only files. Older spreadsheet requests for them are superseded by the owner's 25 October instruction.
- Inspect the saved change. For a deployment, also inspect the provider's result and the running service. Record each as a separate fact.
- Record the specific result, source revision, time, evidence location and executing agent. Do not report an assignment, plan, screenshot or successful command as a completed user outcome.
- Finish the work before updating its records when recording would otherwise cause a delay. A record is not another approval step.

## Remaining work

Keep the existing item numbers so earlier records remain usable. These are work descriptions, not additional approval stages. This documentation edit does not mark any server operation complete.

| Item | Do this | Record the actual result |
| --- | --- | --- |
| 4.1 — Server | Inspect the existing host, running image, database, queue and backup before changing them. | Current versions, service responses, storage and backup observations, with timestamps. |
| 4.2 — Configuration | Align the version pin and inspect the existing Compose settings, required variables and workflow imports. | Saved configuration and actual import results. Do not upgrade the running service merely to complete this item. |
| 4.3 — Access | Check private webhook authentication, stored credentials, network restrictions and account permissions. | Which allowed requests work and which anonymous requests are denied. Keep secrets out of source and results. |
| 4.4 — Connection | Import or repair the existing authorized S-OS command workflow. Keep its request identifier so a repeated request does not create duplicate work. | One real request, its returned result and its saved record. |
| 4.5 — Deployment | Preserve the existing deployment. Change its version only within the owner's authorization and with a usable recovery copy. | The actual deployment result, running version and preserved database. Inspect the database in use; do not assume Postgres or Redis is installed. |
| 4.6 — Workflow | Run the requested safe workflow and inspect its saved execution. Inspect existing retry behavior when relevant; do not restart services or inject failures just to create evidence. | Execution ID, time, returned output and saved result. State any unverified recovery behavior separately. |
| 4.7 — Customer delivery | Apply only when the request includes a customer-facing service. It is not a prerequisite for internal n8n work. | A customer acceptance record or settled invoice only when one actually exists. Do not infer revenue from an inquiry or checkout. |

## Completion

Close each requested item when its actual result is verified. Keep incomplete parts open with a specific next action and resume condition. Ask the owner only for authorization that is genuinely missing for the next action; continue independent authorized work.

Do not turn a proposed role, missing administrative field or unrelated customer/payment item into a reason to stop.

Plain-English rewrite implemented by Codex on 2 November 2026. Original document author: GPT-6. This edit changes instructions only; it does not claim a deployment or workflow execution.
