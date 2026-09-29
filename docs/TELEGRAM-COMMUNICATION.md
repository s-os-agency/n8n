# Telegram communication flow

`workflows/telegram-approval.json` is an inactive, importable workflow definition. Source control is not evidence that it has been imported, activated, or delivered a Telegram message.

## Trust boundary

Telegram is a communication transport, not an authority source. The workflow checks the configured owner chat and sender before forwarding a callback. S-OS must then authenticate the n8n credential, apply S/Passport scope, atomically consume the bound, one-time decision token, persist the decision, and return an audit receipt. Only an `accepted` `approve` response with `passport_authorized: true` reaches `/v1/commands/execute-approved`.

Rejected, denied, expired, duplicate, malformed, or wrong-owner callbacks never reach the command endpoint. Tokens are opaque, contain no authority claims, are bound server-side to the task, approval, action, owner, chat, and expiry, and must be generated independently for approve and reject.

## Outbound contract

POST an envelope to `/webhook/s-agency/outbound/v1`. The workflow passes it to `POST /v1/communications/authorize`; the gateway returns the authorized canonical envelope below. This indirection authenticates the producer and keeps the webhook channel-neutral so another adapter such as WhatsApp can be added without changing the producer contract.

Required for every kind:

| Field | Contract |
|---|---|
| `authorized` | Literal `true`, set only by S-OS |
| `event_id` | Globally unique idempotency ID |
| `kind` | `update`, `decision_request`, or `deliverable` |
| `channel` | `telegram` for this adapter |
| `task_id` / `receipt_id` | S-OS task and audit receipt IDs |
| `title` | Short, non-secret title |
| `expires_at` | Future ISO-8601 timestamp |

An `update` also requires `summary`. A `deliverable` requires an HTTPS `deliverable_url`. A `decision_request` requires `summary`, `approve_token`, and `reject_token`; each token is 8–48 URL-safe opaque characters so the resulting callback remains below Telegram's 64-byte limit. Notifications and deliverables never carry approval buttons.

## Decision response contract

`POST /v1/approvals/decisions` receives the opaque token plus Telegram callback, sender, and chat identifiers. It must perform a single atomic consume-and-record transaction. Its response contains:

* `outcome`: `accepted`, `rejected`, `denied`, `expired`, or `duplicate`;
* `decision`: `approve` or `reject` when accepted;
* `passport_authorized`: boolean;
* `task_id`, `approval_id`, `receipt_id`, and echoed `callback_query_id`.

The command endpoint independently verifies `task_id`, `approval_id`, and `decision_receipt_id`; it must not trust n8n or Telegram to grant authority.

## Private configuration and activation

1. In the private deployment, set `TELEGRAM_OWNER_CHAT_ID`, `TELEGRAM_OWNER_USER_ID`, and `SOS_GATEWAY_URL`. Never put their real values in Git or issue text.
2. Create the Telegram credential named `S-Agency Telegram Bot (private)` and the header-auth credential named `S-OS Passport Gateway (private)`. Grant the latter only communication authorization, decision consumption, and approved-command scopes.
3. Import the workflow, reselect both credentials if the importer cannot resolve names, inspect every expression, and activate it only after the gateway health check succeeds.
4. Record private evidence: import execution/version ID and activation timestamp; outbound `event_id` and Telegram message ID; callback query ID, decision receipt ID, and command receipt ID.
5. Exercise recovery: wrong sender, expired token, and a second use of the same token must produce no command receipt. Temporarily fail the command gateway, verify the n8n error execution is retained, reconcile using the decision receipt (never by consuming the Telegram token again), and record the recovery command receipt.

Do not paste bot tokens, Passport credentials, opaque decision tokens, owner IDs, message contents, or private URLs into tickets, commits, or logs used as public evidence.
