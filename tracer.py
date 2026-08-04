#!/usr/bin/env python3
"""Live Log Tracer: Caddy + Proxmox + HA → trace-events.json with traceId chains."""
import json, subprocess, urllib.request, time, os, sys, ssl, hashlib, re
from datetime import datetime, timezone

# ─── Config ───
TRACE_FILE = "/tmp/tracing-events.json"
DEPLOY_HOST = "192.168.2.147"
DEPLOY_CT = "105"
DEPLOY_PATH = "/opt/tracing-events.json"
POLL_INTERVAL = 10  # seconds
LOG_WINDOW = 3600   # seconds of recent logs to fetch (1 hour)
MAX_EVENTS = 200    # keep last N events

PROXMOX_NODES = {"proxmox": "192.168.2.200", "acemagic": "192.168.2.120", "xshaka": "192.168.2.147"}
CADDY_HOST = "192.168.2.200"  # CT 251 is on proxmox node
CADDY_CT = "251"
CADDY_LOG_CMD = "journalctl _SYSTEMD_UNIT=caddy.service --no-pager -n 50 --output=short-iso 2>/dev/null"

# ─── IP → System-ID mapping ───
IP_MAP = {
    "222": "ct100", "188": "ct101", "241": "ct241", "242": "ct242", "243": "ct243",
    "250": "ct250", "251": "ct251", "185": "vm106",
    "178": "ct102", "223": "ct103", "183": "ct104", "162": "ct109", "173": "vm120",
    "184": "ct105", "186": "ct107", "108": "ct108", "111": "ct111", "112": "ct112", "115": "ct115",
    "200": "proxmox-n1", "120": "acemagic-n2", "147": "xshaka-n3",
    "40": "knx-if", "31": "viessmann", "154": "shelly-rack", "138": "shelly-garten",
    "32": "anker-solar", "191": "womni",
}

def ssh(host, cmd, timeout=8):
    try:
        r = subprocess.run(["sshpass", "-p", "Bashment+13", "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=3", f"root@{host}", cmd],
            capture_output=True, text=True, timeout=timeout)
        return r.stdout if r.returncode == 0 else ""
    except: return ""

def pct_exec(ct, cmd, timeout=8):
    return ssh(DEPLOY_HOST, f"pct exec {ct} -- {cmd}", timeout)

def make_trace_id(prefix="trc"):
    return f"{prefix}-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"

def fetch_caddy_logs():
    """Get recent Caddy access log entries via journald."""
    lines = ssh(CADDY_HOST, f"pct exec {CADDY_CT} -- {CADDY_LOG_CMD}", timeout=10)
    events = []
    now = time.time()
    for line in lines.strip().split("\n"):
        if not line: continue
        # journalctl short-iso: "2026-08-04T18:30:34+0000 hostname proc[pid]: message"
        m = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})[^ ]* .*?:\s*(.*)', line)
        if not m: continue
        ts_str, msg = m.groups()
        try:
            ts = datetime.fromisoformat(ts_str).timestamp()
        except: continue
        # Accept all recent logs (journalctl -n already limits to newest)

        # Try to parse as JSON log line (Caddy structured logging)
        try:
            entry = json.loads(msg)
            status = entry.get("status", 0)
            req = entry.get("request", {})
            host = req.get("host", "")
            method = req.get("method", "")
            uri = req.get("uri", "")
            remote = req.get("remote_ip", "")
            remote_oct = remote.split(".")[-1] if remote else ""
            remote_id = IP_MAP.get(remote_oct, f"ip-{remote_oct}")
            host_clean = host.split(".")[0] if host else ""
            known = {"homepage": "184", "gitea": "241", "nextcloud": "242", "paperless": "222",
                     "grafana": "186", "ntfy": "111", "gatus": "112", "pihole": "188",
                     "vaultwarden": "243", "ollama": "183", "searxng": "108"}
            target_oct = known.get(host_clean, "251")
            target_id = IP_MAP.get(target_oct, f"svc-{target_oct}")
            title = f"{method} {uri}" if uri else f"{method} {host_clean}"
            events.append({
                "traceId": make_trace_id("caddy"),
                "title": f"🌐 {title}",
                "status": "error" if status >= 500 else "warning" if status >= 400 else "success",
                "timestamp": [ts_str, ts_str],
                "source": {"id": remote_id, "name": remote, "ipLast": remote_oct or "ext"},
                "target": {"id": target_id, "name": host_clean, "ipLast": target_oct},
                "what": f"Caddy Proxy: {method} {uri} → {host_clean}",
                "why": f"Request von {remote}",
                "protocol": f"HTTPS ({status})",
                "rawLog": msg[:500],
            })
        except (json.JSONDecodeError, KeyError):
            # Plain text log line
            events.append({
                "traceId": make_trace_id("caddy"),
                "title": f"🌐 Caddy: {msg[:60]}",
                "status": "error" if "error" in msg.lower() else "success",
                "timestamp": [ts_str, ts_str],
                "source": {"id": "ct251", "name": "caddy", "ipLast": "251"},
                "target": {"id": "ct251", "name": "caddy", "ipLast": "251"},
                "what": f"Caddy Log: {msg[:100]}",
                "why": "Reverse-Proxy Log-Eintrag",
                "protocol": "HTTP",
                "rawLog": msg[:500],
            })
    return events

def fetch_proxmox_logs():
    """Get recent Proxmox syslog entries (via xshaka which has fast SSH)."""
    host = PROXMOX_NODES["xshaka"]
    now = time.time()
    since = datetime.fromtimestamp(now - LOG_WINDOW).strftime("%Y-%m-%d %H:%M:%S")
    lines = ssh(host, f"journalctl --since='{since}' -n 80 --no-pager 2>/dev/null", timeout=10)
    events = []
    matched = 0
    for line in lines.strip().split("\n"):
        if not line: continue
        m = re.search(r'(\w{3}\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+?)\[?\d*\]?:?\s*(.*)', line)
        if not m: continue
        matched += 1
        ts_str, hostname, service, msg = m.groups()
        svc_lower = service.lower()
        # Accept systemd, sshd, kernel, and Proxmox-specific events
        if any(k in svc_lower for k in ('systemd', 'sshd', 'kernel', 'pve', 'pct', 'qm', 'corosync')):
            event_type = svc_lower.split('-')[0] if '-' in svc_lower else svc_lower
        elif 'error' in msg.lower() or 'fail' in msg.lower() or 'oom' in msg.lower():
            event_type = "error"
        else:
            continue

        status = "error" if "error" in msg.lower() or "fail" in msg.lower() else "success"
        host_id = IP_MAP.get({"xshaka":"147","acemagic":"120","proxmox":"200"}.get(hostname,""), f"node-{hostname}")
        events.append({
            "traceId": make_trace_id("pve"),
            "title": f"🖥️ [{hostname}] {service}: {msg[:60]}",
            "status": status,
            "timestamp": [ts_str, ts_str],
            "source": {"id": host_id, "name": hostname, "ipLast": {"xshaka":"147","acemagic":"120","proxmox":"200"}.get(hostname,"?")},
            "target": {"id": host_id, "name": hostname, "ipLast": {"xshaka":"147","acemagic":"120","proxmox":"200"}.get(hostname,"?")},
            "what": f"Proxmox {event_type}: {msg[:100]}",
            "why": f"System-Event auf {hostname}",
            "protocol": "syslog",
            "rawLog": line[:500],
        })
    return events

def correlate(events):
    """Link events with parent/child by time proximity (<2s) and IP overlap."""
    if len(events) < 2: return events
    events.sort(key=lambda e: e["timestamp"][0] if isinstance(e["timestamp"], list) else e["timestamp"])
    for i in range(len(events) - 1):
        e1, e2 = events[i], events[i+1]
        try:
            t1 = datetime.fromisoformat((e1["timestamp"][0] if isinstance(e1["timestamp"], list) else e1["timestamp"]).replace("Z", "+00:00"))
            t2 = datetime.fromisoformat((e2["timestamp"][0] if isinstance(e2["timestamp"], list) else e2["timestamp"]).replace("Z", "+00:00"))
        except: continue
        delta = abs((t2 - t1).total_seconds())
        if delta < 2.0:
            # Link if e2's source matches e1's target (causal chain)
            if e1.get("target", {}).get("ipLast") == e2.get("source", {}).get("ipLast") or \
               e1.get("source", {}).get("ipLast") == e2.get("source", {}).get("ipLast"):
                if "children" not in e1: e1["children"] = []
                e2["parentId"] = e2.get("parentId") or e1["traceId"]
                e1["children"].append(e2)

    # Return only root events (no parentId) with their children
    roots = [e for e in events if not e.get("parentId")]
    return roots

def main():
    print(f"[tracer] Starting log poller (interval={POLL_INTERVAL}s)", file=sys.stderr)
    while True:
        all_events = []
        try:
            caddy = fetch_caddy_logs()
            all_events.extend(caddy)
            print(f"[tracer] Caddy: {len(caddy)} entries", file=sys.stderr)
        except Exception as e:
            print(f"[tracer] Caddy error: {e}", file=sys.stderr)

        try:
            pve = fetch_proxmox_logs()
            all_events.extend(pve)
            print(f"[tracer] Proxmox: {len(pve)} entries", file=sys.stderr)
        except Exception as e:
            print(f"[tracer] Proxmox error: {e}", file=sys.stderr)

        if all_events:
            # Correlate into causal chains
            roots = correlate(all_events)
            roots = roots[:MAX_EVENTS]

            # Write local
            with open(TRACE_FILE, "w") as f:
                json.dump({"events": roots, "updated": datetime.now(timezone.utc).isoformat()}, f)
            print(f"[tracer] Written {len(roots)} chains ({len(all_events)} raw)", file=sys.stderr)

            # Deploy to CT105
            try:
                subprocess.run(["sshpass", "-p", "Bashment+13", "scp", "-o", "StrictHostKeyChecking=no",
                    TRACE_FILE, f"root@{DEPLOY_HOST}:/tmp/te.json"], timeout=10)
                subprocess.run(["sshpass", "-p", "Bashment+13", "ssh", "-o", "StrictHostKeyChecking=no",
                    f"root@{DEPLOY_HOST}", f"pct push {DEPLOY_CT} /tmp/te.json {DEPLOY_PATH}"], timeout=10)
            except: pass

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
