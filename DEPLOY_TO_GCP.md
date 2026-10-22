# Deploy n8n to GCP VM (canonical)

**This is the live deployment.** The n8n instance this repo describes runs on the GCP box at `34.139.100.169` (Tailscale `100.86.90.80`), Ubuntu, Docker container `n8nio/n8n:2.42.3`, bound to localhost port 5678.

All DigitalOcean App Platform specs are parked under [zz-ARCHIVE/digitalocean/](zz-ARCHIVE/digitalocean/) for a possible later stage. Do not deploy from them.

## What is running

| Item | Value |
|------|-------|
| Host | GCP VM `cloud-pc-a50933c6`, public IP 34.139.100.169 |
| Tailscale | 100.86.90.80, tag `s.soub@` |
| Container image | `n8nio/n8n:2.42.3` |
| Bind | 127.0.0.1:5678 (localhost only) |
| Data volume | Docker volume for `/home/node/.n8n` |
| Workflows dir | mounted from repo `workflows/` |
| Database | PostgreSQL (see `.env` on host) |
| Queue | Redis (see `.env` on host) |

## Access

- From the tailnet: `http://100.86.90.80:5678`
- From the box itself: `http://127.0.0.1:5678`
- No public port 5678. No reverse proxy in front yet.

## Operations

```bash
# SSH in
ssh ubuntu@34.139.100.169

# Status
docker ps | grep n8n

# Logs
docker logs -f n8n

# Restart
docker restart n8n

# Pull new image (must match .n8n-version policy — update that file first)
docker pull n8nio/n8n:2.42.3
docker stop n8n && docker rm n8n
# re-run with same volume/env mounts as before
```

## Version policy

Image tags are pinned in [.n8n-version](.n8n-version) and validated by CI (scripts/validate-versions.py). The running container on GCP is 2.42.3; the repo's compose files still reference 2.3.2 — that drift is tracked and should be reconciled.

## Env

Secrets live in `.env` on the host only. [.env.example](.env.example) is the template. Never commit real values.

## Health check

`scripts/healthcheck.sh` hits `/healthz/readiness` on 127.0.0.1:5678. Wire it into whatever supervisor you use on the box.

## Webhooks

Because n8n is bound to localhost, external webhook callers need either Tailscale or a tunnel. No public webhook URL is configured yet — `WEBHOOK_URL` should be set once one exists.

## Next steps

1. Reconcile image tag 2.3.2 → 2.42.3 across compose files and `.n8n-version`
2. Decide on persistent storage beyond the Docker volume (MariaDB is already on this box — could point n8n at it instead of Postgres)
3. Expose via Tailscale Funnel or a reverse proxy if webhooks need to be public
4. Back up the `n8n_data` volume
