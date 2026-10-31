#!/usr/bin/env node
// Read-only fleet integration check. No credential values or private response
// bodies are printed. Does not start paused workers or mutate n8n workflows.
import { writeFileSync } from "node:fs";

const sites = [
  ["workers-control", "https://s-workers-control.alex-008.chatgpt.site/api/live"],
  ["s-pm", "https://seif-paperclip.alex-008.chatgpt.site/api/live"],
  ["repository-intelligence", "https://s-repository-intelligence.alex-008.chatgpt.site/api/live"],
];
const n8nBase = process.env.N8N_BASE_URL || "http://127.0.0.1:5678";
const siteToken = process.env.SITES_SERVICE_TOKEN || "";
const outFile = process.env.FLEET_REPORT_FILE || "";
const result = { schema: "s-agency.fleet-integration-audit.v1", observedAt: new Date().toISOString(), n8n: {}, sites: {}, fleet: { state: "not_verified", workers: [], totals: {} }, overall: "unverified" };

async function get(url, extra = {}) {
  try {
    const response = await fetch(url, { headers: extra, redirect: "error", signal: AbortSignal.timeout(6500) });
    if (!response.ok) return { ok: false, status: response.status, error: response.status === 401 || response.status === 403 ? "authentication_required" : "http_error" };
    const text = await response.text();
    try { return { ok: true, status: response.status, payload: JSON.parse(text) }; }
    catch { return { ok: true, status: response.status, payload: null }; }
  } catch (e) { return { ok: false, error: e.name === "TimeoutError" ? "timeout" : "request_failed" }; }
}

const n8n = await get(new URL("/healthz/readiness", n8nBase).toString());
result.n8n = { ready: n8n.ok, status: n8n.status ?? null, error: n8n.error ?? null };

for (const [name, url] of sites) {
  const auth = siteToken ? { Authorization: `Bearer ${siteToken}` } : {};
  const response = await get(url, auth);
  result.sites[name] = { reachableAndAuthorized: response.ok, status: response.status ?? null, error: response.error ?? null };
  if (name === "workers-control" && response.ok) {
    const p = response.payload;
    const candidates = [p?.workers, p?.data?.workers, p?.registry?.workers, p?.report?.workers, p?.live?.workers];
    const rows = candidates.find(Array.isArray);
    if (rows) {
      result.fleet.workers = rows.map((w, index) => {
        const id = String(w.id ?? w.workerId ?? w.name ?? `unknown-${index}`);
        const declared = String(w.status ?? w.state ?? "unknown").toLowerCase();
        const heartbeat = w.lastHeartbeat ?? w.last_heartbeat ?? w.heartbeatAt ?? null;
        const age = heartbeat ? Date.now() - Date.parse(heartbeat) : NaN;
        const fresh = Number.isFinite(age) && age >= 0 && age <= 15 * 60_000;
        const passport = w.passport?.status ?? w.passportStatus ?? w.passport_status ?? "unverified";
        const verifiedRunning = ["live", "running", "active"].includes(declared) && fresh && String(passport).toLowerCase() === "valid";
        return { id, declared, heartbeatFresh: fresh, passportStatus: String(passport), verifiedRunning };
      });
      const count = result.fleet.workers.length;
      const live = result.fleet.workers.filter(w => w.verifiedRunning).length;
      result.fleet = { ...result.fleet, state: "inspected", totals: { inspected: count, verifiedRunning: live, notVerifiedRunning: count - live } };
    }
  }
}
const sitesReady = Object.values(result.sites).every(x => x.reachableAndAuthorized);
result.overall = result.n8n.ready && sitesReady && result.fleet.state === "inspected" && result.fleet.totals.notVerifiedRunning === 0 ? "passed" : "not_fully_verified";
const rendered = JSON.stringify(result, null, 2);
if (outFile) writeFileSync(outFile, rendered + "\n", { mode: 0o600 });
console.log(rendered);
if (result.overall !== "passed") process.exitCode = 1;
