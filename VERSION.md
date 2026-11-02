# n8n versions and upgrades

## Documented versions

The repository pin in [.n8n-version](.n8n-version) is **2.3.2**. [docs/AGENT-ACCESS.md](docs/AGENT-ACCESS.md) records a later running image, **2.42.3**. Neither statement is a fresh observation of the server. Check the running version before changing it; do not deploy the older pin over a newer database.

The 7 October 2026 review inspected revision `a5dffb6cf606e762333d8daf599d93af34122310`. Production, queue and runner templates used `2.3.2`; local and starter templates had used `latest`. That review selected `2.3.2` as a configuration baseline, not as proof of the deployed version. It noted `2.41.7` as a comparison candidate and `2.42.4` as the latest non-prerelease observed on 7 October. Those are historical observations, not today's upgrade recommendations.

Local Compose used PostgreSQL 16; the archived DigitalOcean templates used PostgreSQL 17. Those template settings do not establish the current database or deployment. Do not deploy files under `zz-ARCHIVE/digitalocean/`.

## Check the running version

Use the existing authenticated server connection and the Compose file actually running that server. Inspect the n8n version, container image and image digest without pulling images, recreating services or printing secrets.

For a Docker deployment, use the actual container and image IDs:

```bash
docker exec CONTAINER_ID n8n --version
docker inspect --format '{{.Config.Image}} {{.Image}}' CONTAINER_ID
docker image inspect --format '{{json .RepoDigests}}' IMAGE_ID
```

Record the time, host, version, image digest, repository revision when available, and observed service response. Keep credentials, full logs and database backups private. These commands are examples; this document does not claim they ran.

This inspection is required before a version change because deploying an older binary against a newer database can break the service. It does not block documentation fixes or other independent authorized work. The old 8 October launch deadline is historical and imposes no current waiting period.

## Change the version safely

1. Identify the running version and resolve its difference from `.n8n-version` before selecting an upgrade.
2. Read the candidate's release notes, intervening breaking changes and security guidance. The [7 October comparison](docs/VERSION-REVIEW-2026-10-07.md) is historical context.
3. Preserve a current database backup, persistent data and the existing encryption key securely. Keep the previous image and a matching database snapshot available for recovery. An old image against a migrated database is not a complete rollback.
4. Inspect actual configuration, migration requirements and existing operational evidence. Do not add or run software test suites or test-only workflows. Do not turn a missing observation into a success claim.
5. For an authorized version change, update the relevant pin, environment examples and active Compose/runner tags together. `python3 scripts/validate-versions.py` is the existing configuration inspector and requires `PyYAML==6.0.3`; inspect its current scope before use. Never print the full `.env` or resolved Compose configuration.
6. Deploy through the existing authorized route. Inspect the provider result, running version, health response and actual workflow records. Keep existing workflow activation settings unless the requested change includes changing them.

Carry authorized work through completion. Ask only for a specific missing authorization or essential fact that available sources cannot resolve. A spreadsheet, reviewer assignment or named stage must not create another approval wait. Record source changes, deployment and observed service operation separately.

Updated by Codex on 2 November 2026. Documentation wording was corrected; no server version, credential, network permission or running service was changed by this edit.

Sources: [n8n releases](https://github.com/n8n-io/n8n/releases), [release notes](https://docs.n8n.io/changelog/release-notes), [Docker installation](https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker.md).
