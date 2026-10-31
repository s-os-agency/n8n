#!/usr/bin/env node
/**
 * Read-only local audit. Run on the server that actually hosts n8n and the
 * factory timer. No login, tokens, source changes, workflow activation or
 * container restarts. Emits evidence JSON, never guesses worker readiness.
 */
import { execFileSync } from "node:child_process";

function command(bin, args) {
  try {
    return { ok: true, output: execFileSync(bin, args, { encoding: "utf8", timeout: 8000 }).trim() };
  } catch (error) {
    return { ok: false, error: error.code ?? "execution_failed" };
  }
}
async function health(url) {
  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(5000), redirect: "error" });
    return { reachable: true, httpStatus: response.status, ready: response.status === 200 };
  } catch (error) {
    return { reachable: false, ready: false, error: error.name ?? "request_failed" };
  }
}

const observedAt = new Date().toISOString();
const n8n = await health("http://127.0.0.1:5678/healthz/readiness");
const timer = command("systemctl", ["is-active", "ss-agentic-ai-factory.timer"]);
const docker = command("docker", ["ps", "--format", "{{.Names}}|{{.Image}}|{{.Status}}"]);
const containers = docker.ok ? docker.output.split("\n").filter(Boolean).map(row => {
  const [name, image, status] = row.split("|");
  return { name, image, status };
}) : [];
const report = {
  schema: "s-agency.server-worker-audit.v1",
  observedAt,
  runtimeTarget: "local-host-only",
  n8n: { localReadiness: n8n },
  factory: { timerActive: timer.ok && timer.output === "active", timerObserved: timer },
  docker: { accessible: docker.ok, containers, error: docker.ok ? null : docker.error },
  workerRoster: { state: "not_verified_by_this_audit", note: "Use the canonical Manus MariaDB registry, passports, heartbeats and execution receipts; Docker process count is not an all-workers-live claim." },
};
console.log(JSON.stringify(report, null, 2));
if (!n8n.ready || !report.factory.timerActive || !docker.ok) process.exitCode = 1;
