#!/usr/bin/env python3
"""
Live State Adapter: Prometheus → state.json für 3D Homelab Universe

Fragt CPU/RAM/Disk von Prometheus ab und generiert eine state.json,
die das Dashboard via /api/universe-state einliest.

Laufzeit: alle 5 Sekunden (via systemd timer oder while-loop)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

PROMETHEUS = "http://192.168.2.186:9090"
OUTPUT_DIR = Path(os.environ.get("STATE_OUTPUT_DIR", "/opt"))
OUTPUT_FILE = OUTPUT_DIR / "universe-state.json"
SCRAPE_INTERVAL = int(os.environ.get("SCRAPE_INTERVAL", "5"))

# ─── IP → System-ID Mapping (Prometheus targets → homelab.json systems) ───
TARGET_MAP = {
    "192.168.2.222:9100": "node-a1",   # paperless-ngx CT100
    "192.168.2.188:9100": "node-a2",   # pihole CT101
    "192.168.2.230:9100": "node-a3",   # paperless-ai CT103
    "192.168.2.184:9100": "node-b1",   # dashboard CT105
    "192.168.2.186:9100": "node-c1",   # grafana CT107
    "192.168.2.241:9100": "node-d1",   # gitea CT241
    "192.168.2.242:9100": "node-e1",   # nextcloud CT242
    "192.168.2.178:9101": "node-c2",   # shelly
}

# ─── PromQL Queries ───
QUERIES = {
    "up": "up",
    "cpu_percent": '100 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100',
    "ram_percent": '100 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100',
    "disk_percent": '100 - (node_filesystem_avail_bytes{mountpoint="/",fstype!="tmpfs"} / node_filesystem_size_bytes{mountpoint="/",fstype!="tmpfs"}) * 100',
    "network_rx": 'rate(node_network_receive_bytes_total{device!="lo"}[1m])',
    "network_tx": 'rate(node_network_transmit_bytes_total{device!="lo"}[1m])',
}


def prometheus_query(query: str) -> dict:
    """Run an instant PromQL query, return parsed results."""
    url = f"{PROMETHEUS}/api/v1/query?query={urllib.request.quote(query)}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        if data.get("status") != "success":
            return {}
        results = {}
        for r in data["data"]["result"]:
            instance = r["metric"].get("instance", "unknown")
            try:
                value = float(r["value"][1])
            except (IndexError, ValueError, TypeError):
                value = 0.0
            results[instance] = value
        return results
    except Exception as e:
        print(f"[adapter] Prometheus query failed: {e}", file=sys.stderr)
        return {}


def collect_metrics() -> dict:
    """Collect all metrics from Prometheus and build state dict."""
    cpu_data = prometheus_query(QUERIES["cpu_percent"])
    ram_data = prometheus_query(QUERIES["ram_percent"])
    disk_data = prometheus_query(QUERIES["disk_percent"])
    up_data = prometheus_query(QUERIES["up"])
    rx_data = prometheus_query(QUERIES["network_rx"])
    tx_data = prometheus_query(QUERIES["network_tx"])

    nodes = []
    for instance, system_id in TARGET_MAP.items():
        cpu = cpu_data.get(instance, 0.0)
        ram = ram_data.get(instance, 0.0)
        disk = disk_data.get(instance, 0.0)
        online = bool(up_data.get(instance, 0))
        rx = rx_data.get(instance, 0.0)
        tx = tx_data.get(instance, 0.0)

        # Determine threshold level
        max_load = max(cpu, ram, disk)
        if max_load > 85:
            level = "critical"
        elif max_load > 50:
            level = "warning"
        else:
            level = "normal"

        nodes.append({
            "id": system_id,
            "instance": instance,
            "online": online,
            "cpu": round(cpu, 1),
            "ram": round(ram, 1),
            "disk": round(disk, 1),
            "network_rx_kbps": round(rx / 1024, 1),
            "network_tx_kbps": round(tx / 1024, 1),
            "level": level,
        })

    state = {
        "timestamp": time.time(),
        "nodes": nodes,
        "node_count": len(nodes),
        "online_count": sum(1 for n in nodes if n["online"]),
        "pipeline": [],  # placeholder for CI/CD pipeline status
        "issues_open": 0,
        "paperless_docs": 0,
    }
    return state


def main():
    print(f"[adapter] Starting, Prometheus={PROMETHEUS}, output={OUTPUT_FILE}, interval={SCRAPE_INTERVAL}s")
    while True:
        try:
            state = collect_metrics()
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            tmp = OUTPUT_FILE.with_suffix(".tmp")
            tmp.write_text(json.dumps(state, indent=2))
            tmp.rename(OUTPUT_FILE)
            online = state["online_count"]
            total = state["node_count"]
            print(f"[adapter] State updated: {online}/{total} nodes online")
        except Exception as e:
            print(f"[adapter] Error: {e}", file=sys.stderr)
        time.sleep(SCRAPE_INTERVAL)


if __name__ == "__main__":
    main()
