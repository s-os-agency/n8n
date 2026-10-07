# n8n version policy

## Release baseline — 2026-10-07

The canonical repository configuration pin is **2.3.2**, recorded in
[.n8n-version](.n8n-version). Local Compose, `.env.example`, every DigitalOcean
App Platform template (including starter), queue workers, and external runners
must match it. Floating tags and shell overrides of the Compose image are not
part of the release path. CI rejects drift with `scripts/validate-versions.py`.

This retains the existing production-template baseline while removing local and
starter drift. It is **not a production runtime acceptance, upgrade approval,
or proof that 2.3.2 is currently deployed**. Do not deploy this baseline to an
existing database until the running version is established. In particular, do
not downgrade a newer runtime/database to 2.3.2 using these templates.

| Item | Evidence/status |
| --- | --- |
| Inspected repository revision | `a5dffb6cf606e762333d8daf599d93af34122310` |
| Previous production/queue/runner template tags | `2.3.2` |
| Previous local/starter selection | `.env.example` and three App Platform templates used `latest` |
| Actual production binary version/image digest | **Unknown; no authenticated runtime evidence available in this review** |
| Selected configuration baseline | `2.3.2`, provisional until runtime inventory and compatibility acceptance |
| Upgrade comparison candidate | `2.41.7`, released 2026-10-05; not selected for deployment |
| Upstream latest non-prerelease observed | `2.42.4`, published 2026-10-07 07:22:03 UTC; not selected for deployment |
| Runtime migration/workflow compatibility | **Not executed**; requires an isolated runtime and a database restore |

The historical Amsterdam/PostgreSQL 17/instance-size claims in this document
were template details, not live deployment evidence. Local Compose uses
PostgreSQL 16; App Platform templates use PostgreSQL 17. Version alignment alone
does not establish deployment-topology or database compatibility.

## Capture the actual runtime before acceptance

Use the authorized deployment route already operating the instance. Keep raw
app specs, logs, database snapshots and secrets private; record only the fields
below in the evidence receipt.

For the existing Docker Compose host (from its actual project directory, without
pulling images or recreating services):

```bash
docker compose -f docker-compose.local.yml exec -T n8n n8n --version
docker compose -f docker-compose.local.yml ps -q n8n
# Use that container ID for narrowly scoped inspection:
docker inspect --format '{{.Config.Image}} {{.Image}}' CONTAINER_ID
docker image inspect --format '{{json .RepoDigests}}' IMAGE_ID
```

For DigitalOcean App Platform: inspect the active deployment ID, active spec
image tags and resolved image digests in the authenticated console/API, then run
`n8n --version` in the running main and each workflow worker container. Capture
runner image/version evidence too. A submitted spec or an old successful CI run
alone does not prove the active binary version. Do not create a new app to obtain
this inventory.

Record: UTC timestamp, platform/app or host identity, active deployment ID,
repository revision (if available), main/worker/runner versions, resolved image
digests and evidence source. Until collected, runtime acceptance is held. Trigger
to resume: authorized access to the existing runtime and its sanitized inventory;
resolve before the 2026-10-08 launch freeze. If unavailable at freeze, keep runtime
acceptance unverified and do not represent the launch path as accepted.

## Change and upgrade policy

1. Collect the actual runtime inventory. If it differs from the pin, reconcile
   the baseline in a new reviewed change; do not redeploy or downgrade blindly.
2. Select one explicit candidate. Review every intervening release, applicable
   migration/breaking-change guidance and security advisories for that candidate.
   See [the 2.41.7 comparison](docs/VERSION-REVIEW-2026-10-07.md).
3. Back up the deployed database and persistent data; preserve the existing
   encryption key securely. Test restore before migration. Keep the snapshot
   private and disable schedules/webhooks/outbound effects in the isolated copy.
4. Run the candidate on the isolated restored database. Record migration logs,
   readiness, credentials decryption, workflow import/export, Code node execution,
   representative triggers, approvals, routing and write-back receipts. Test the
   actual worker/runner topology and PostgreSQL version, not just local JSON.
5. Test recovery to the pre-upgrade image **and pre-upgrade database snapshot**.
   Restarting an old image against the migrated database is not a rollback test.
6. After compatibility acceptance, update `.n8n-version`, `.env.example`, Compose,
   all App Platform n8n/runner tags and this document together. Run:
   `python3 scripts/validate-versions.py` (requires `PyYAML==6.0.3`). For local
   startup also reconcile the private `.env` and run the validator with
   `--check-env`; never print the entire `.env` or full resolved Compose config.
7. Deploy only through the established route, then capture binary versions/image
   digests again and attach execution receipts. Keep existing workflows inactive
   until their own acceptance gates pass.

Sources: [upstream releases](https://github.com/n8n-io/n8n/releases),
[2.41.7](https://github.com/n8n-io/n8n/releases/tag/n8n%402.41.7),
[2.42.4](https://github.com/n8n-io/n8n/releases/tag/n8n%402.42.4),
[release notes](https://docs.n8n.io/changelog/release-notes),
[Docker installation](https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker.md).
