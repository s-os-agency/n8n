# Seif interval control with n8n

This adds `seif-runtime` beside n8n in the existing repository stack. The control page has an n8n readiness indicator, a button to open its editor, and a link to this repository. Python sends interval jobs to an n8n production webhook when a task and endpoint are configured and dispatch is enabled. It continues independently of the page.

From the repository root, after completing its existing `.env` setup:

```sh
docker compose -f docker-compose.local.yml -f docker-compose.seif.yml up -d --build
```

Open http://127.0.0.1:8765 for Settings and http://127.0.0.1:5678 for n8n. Use `http://n8n:5678/webhook/YOUR_PATH` as the Python task endpoint inside this stack. Create and publish the intended webhook workflow in n8n first. Its response confirms dispatch only, not revenue or settlement.

Compose preserves the existing canonical n8n version and database volumes; this addition is not an upgrade. Follow VERSION.md before operating against an existing database. Docker restart policies resume containers when Docker starts. A managed Docker host must stay powered on for continuous operation.

GitHub is the deployment source through this repository. The UI repository link does not enable n8n's native source-control feature or import workflows. No account or financial workflow is activated by adding the service.

Verified locally: Python syntax, frontend syntax, recurring ticks, API settings persistence and local n8n status detection against an isolated test HTTP server. Docker build and n8n integration were not executed in the authoring environment: Docker is unavailable and npm download is blocked (HTTP 403).
