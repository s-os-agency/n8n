# Version comparison and acceptance gap — 2026-10-07

## Decision

Retain **2.3.2** as the single provisional repository baseline. Remove `latest`
from the local and starter paths. This is configuration reconciliation only;
neither a new production deployment nor confirmation of the existing runtime.
`2.41.7` is the requested comparison candidate, not an accepted upgrade.
GitHub's latest non-prerelease release API now reports `2.42.4`, published on
2026-10-07 at 07:22:03 UTC. A moving upstream latest tag cannot serve as the
launch version contract.

## Reviewed upstream changes

Reviewed GitHub release metadata/bodies covering 2.3.2 through 2.41.7, including
migration and deprecation entries. The following are concrete items requiring
attention; this list is not a runtime compatibility certification or a complete
audit of all source changes and security advisories.

| Release/change | Relevance and required verification |
| --- | --- |
| [2.20.0](https://github.com/n8n-io/n8n/releases/tag/n8n%402.20.0): PostgreSQL variable-values migration | Restore the actual database and run candidate migrations; inspect variable-dependent expressions and values. Do not infer safety from JSON syntax checks. |
| [2.27.0](https://github.com/n8n-io/n8n/releases/tag/n8n%402.27.0): execution_entity index migration | Upstream flags possible multi-minute migration time on large instances. Measure restored production data and size; allow a suitable startup/maintenance window. |
| [2.30.0](https://github.com/n8n-io/n8n/releases/tag/n8n%402.30.0): `$getPairedItem` deprecation | Inspect exported live workflows, community nodes and expressions for usage; test item pairing/output equivalence. Repo assets alone do not cover live workflows. |
| [2.33.0](https://github.com/n8n-io/n8n/releases/tag/n8n%402.33.0): activate/deactivate public API endpoints deprecated | Audit external activation clients/import scripts; test trigger registration and controlled activation against the candidate API. Deprecation is not proof of removal in 2.41.7. |
| [2.33.0](https://github.com/n8n-io/n8n/releases/tag/n8n%402.33.0): concurrent startup migration-race fix | In queue deployments, test startup order and migration readiness before launching workers/runners; record main/worker version parity. |
| [2.36.7](https://github.com/n8n-io/n8n/releases/tag/n8n%402.36.7): workflow-history list API offset parameter removed | Audit history/reporting clients for offset-based pagination; not seen in the repository workflow assets, live clients remain unknown. |
| [2.39.6](https://github.com/n8n-io/n8n/releases/tag/n8n%402.39.6): warning for deprecated N8N_DB_PING_TIMEOUT | Not configured in checked-in deployment files; check the existing private deployment configuration without exposing values. |
| [2.39.6](https://github.com/n8n-io/n8n/releases/tag/n8n%402.39.6): v3 storage-directory breaking-change detection rule | A future-version detection rule, not evidence that 2.41.7 renames the storage directory. Do not apply v3 migration steps speculatively. |
| [2.41.7](https://github.com/n8n-io/n8n/releases/tag/n8n%402.41.7): API-key variable scope grant fix | Validate least-required API access and variable scopes with actual bound credentials. The patch's notes do not establish safety of the whole 2.3.2→2.41.7 interval. |

Both versions are already 2.x. Do not apply every 1.x→2.0 instruction as if it
were a newly introduced change between these versions. If the actual runtime
turns out to be 1.x, separately assess that major migration.

## Repository workflow inventory

The five checked-in workflow files use Gmail Trigger v1, Schedule Trigger v1/v1.2,
Telegram Trigger/Telegram v1, Manual Trigger v1, Set v3, Google Sheets v4.6, Code
v2, Switch v3.2 and HTTP Request v4.2. No checked-in node uses the removed
Spontit/Crowd.dev/Kitemaker/Automizy integrations. This inventory is not a live
workflow export and does not prove node semantics or credential compatibility.

The hourly orchestrator has Code nodes, Google Sheets bindings and HTTP calls:
exercise both manual and scheduled paths with isolated fixtures, routing and
receipt/write-back checks. Verify retry/error behavior and duplicate side-effect
handling. Its source remains inactive. Telegram and Gmail triggers need private
credential binding and a controlled integration test. Queue mode and external
runners exist in App Platform examples but not in local Compose; test the actual
selected topology and runner image parity if deployed.

## Acceptance record

- Configuration consistency: enforced by `scripts/validate-versions.py` in CI.
- Workflow JSON and existing regression checks: static checks only.
- Running production version/deployment ID/digests: **not available**.
- Database migration on a restored snapshot: **not executed**.
- Credential decryption, node execution, trigger delivery and recovery: **not executed**.
- Candidate security-advisory review: **pending** before release selection.
- Resume trigger/deadline: obtain authorized access to the existing deployment,
  capture inventory, and perform isolated acceptance before the 2026-10-08 freeze.
  If access is unavailable at freeze, retain unverified status and exclude claims
  of runtime acceptance. Do not alter live deployments or activate workflows.

See [VERSION.md](../VERSION.md) for inventory commands, promotion and rollback
requirements.
