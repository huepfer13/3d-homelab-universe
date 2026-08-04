#!/usr/bin/env python3
"""Homelab Scanner v2: Pi-hole + Proxmox + MAC-Deduplication → config.local.json.
Prevents duplicate entries via MAC fingerprinting and alias matching."""
import json, subprocess, urllib.request, time, os, sys

PIHOLE = "http://192.168.2.188"
TARGET = "/tmp/config.local.json"
DEPLOY_HOST = "192.168.2.147"
DEPLOY_CT = "105"
DEPLOY_PATH = "/opt/config.local.json"

PROXMOX_NODES = {"proxmox": "192.168.2.200", "acemagic": "192.168.2.120", "xshaka": "192.168.2.147"}
NODE_IPS = {"proxmox": "200", "acemagic": "120", "xshaka": "147"}

# ─── Alias & MAC Registry: canonical ID → [aliases, macs] ───
# Prevents duplicate entries when devices appear under different names
DEVICE_REGISTRY = {
    "proxmox-n1":    {"aliases": ["proxmox", "pve", "proxmox.lan"],        "macs": ["68:1d:ef:44:f7:6d"]},
    "acemagic-n2":   {"aliases": ["acemagic", "acemagic.lan"],             "macs": ["68:1d:ef:49:fd:b6"]},
    "xshaka-n3":     {"aliases": ["xshaka", "xshaka.lan"],                 "macs": ["8c:89:a5:0d:49:51"]},
    "ct102":         {"aliases": ["hermesagent", "hermes-agent"],           "macs": ["bc:24:11:10:41:ff"]},
    "ct104":         {"aliases": ["ollama", "ollama.lan"],                  "macs": []},
    "ct105":         {"aliases": ["homepage", "dashboard"],                 "macs": ["bc:24:11:0e:57:94"]},
    "ct107":         {"aliases": ["grafana", "grafana.lan"],                "macs": ["bc:24:11:6a:33:e7"]},
    "ct100":         {"aliases": ["paperless-ngx", "paperless"],            "macs": ["bc:24:11:f4:5b:99"]},
    "ct241":         {"aliases": ["gitea", "gitea.lan"],                    "macs": ["bc:24:11:19:f7:43"]},
    "ct242":         {"aliases": ["nextcloud", "nextcloud.lan"],            "macs": ["bc:24:11:63:0b:70"]},
    "ct243":         {"aliases": ["vaultwarden"],                           "macs": ["bc:24:11:fe:23:5d"]},
    "ct250":         {"aliases": ["wireguard", "wg"],                       "macs": ["bc:24:11:f9:20:a8"]},
    "ct251":         {"aliases": ["caddy", "proxy"],                        "macs": ["bc:24:11:19:06:9f"]},
    "vm106":         {"aliases": ["homeassistant", "haos", "ha"],           "macs": ["02:f9:e7:d4:92:e6"]},
    "ct103":         {"aliases": ["paperless-test", "paperless-v3"],        "macs": ["bc:24:11:43:ee:3e"]},
    "ct109":         {"aliases": ["hermes-worker", "worker"],               "macs": ["bc:24:11:59:75:54"]},
    "ct108":         {"aliases": ["searxng", "search"],                     "macs": []},
    "vm120":         {"aliases": ["win11vm", "ets6", "windows"],            "macs": []},
    "knx-if":        {"aliases": ["knx", "knx-ip", "KNX-IPIF"],             "macs": []},
    "viessmann":     {"aliases": ["heizung", "vicare"],                     "macs": []},
    "shelly-rack":   {"aliases": ["homelabrack", "rackpower"],              "macs": []},
    "shelly-garten": {"aliases": ["garten", "garten-shelly"],               "macs": []},
    "anker-solar":   {"aliases": ["anker", "solix", "solarbank"],           "macs": []},
    "womni":         {"aliases": ["xomni", "womni.lan"],                    "macs": ["38:8d:3d:54:12:a6"]},
    "nipogi":        {"aliases": ["nipogi", "pve-mini", "mini-pc"],         "macs": []},
}

def ssh(host, cmd, timeout=10):
    try:
        r = subprocess.run(["sshpass", "-p", "Bashment+13", "ssh", "-o", "StrictHostKeyChecking=no",
            "-o", "ConnectTimeout=3", f"root@{host}", cmd],
            capture_output=True, text=True, timeout=timeout)
        return r.stdout if r.returncode == 0 else ""
    except: return ""

def resolve_alias(name: str, mac: str = "") -> str:
    """Check if a discovered name/MAC matches a known device. Returns canonical ID or None."""
    name_lower = name.lower().replace(".lan", "").replace(".fritz.box", "")
    for cid, reg in DEVICE_REGISTRY.items():
        if name_lower in [a.lower() for a in reg["aliases"]]:
            return cid
        if mac and mac.lower() in [m.lower() for m in reg["macs"]]:
            return cid
    return None

def get_pihole_devices():
    """Get all devices from Pi-hole API with MAC → {ip, name} mapping."""
    devices = {}
    try:
        req = urllib.request.Request(f"{PIHOLE}/api/network/devices")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        for dev in data.get("devices", []):
            mac = dev.get("hwaddr", "").lower()
            for ip_info in dev.get("ips", []):
                ip = ip_info.get("ip", "")
                name = ip_info.get("name", "")
                if ip.startswith("192.168.2."):
                    last = ip.split(".")[-1]
                    clean = (name or "").replace(".lan", "").replace(".fritz.box", "")
                    # Deduplicate: check alias registry first
                    canonical = resolve_alias(clean, mac)
                    devices[last] = {"name": canonical or clean, "mac": mac, "ip": ip}
    except Exception as e:
        print(f"[pihole] {e}", file=sys.stderr)
    return devices

def get_proxmox_cts(node):
    """Get running CTs on a Proxmox node."""
    host = PROXMOX_NODES[node]
    if node == "proxmox":
        out = ssh(PROXMOX_NODES["xshaka"],
            f"for f in /etc/pve/nodes/proxmox/lxc/*.conf; do id=$(basename $f .conf); name=$(grep -oP 'hostname:\\s*\\K.*' $f 2>/dev/null); echo \"$id $name\"; done", timeout=10)
    else:
        out = ssh(host, "pct list 2>/dev/null", timeout=8)
    cts = []
    for line in out.strip().split("\n"):
        parts = line.split()
        if len(parts) >= 2:
            vmid, name = parts[0], parts[-1]
            if vmid.isdigit(): cts.append({"vmid": vmid, "name": name})
    return cts

def get_proxmox_vms(node):
    """Get running VMs on a Proxmox node."""
    host = PROXMOX_NODES[node]
    if node == "proxmox":
        out = ssh(PROXMOX_NODES["xshaka"],
            f"for f in /etc/pve/nodes/proxmox/qemu-server/*.conf; do id=$(basename $f .conf); name=$(grep -oP '^name:\\s*\\K.*' $f 2>/dev/null); echo \"$id $name\"; done", timeout=10)
    else:
        out = ssh(host, "qm list 2>/dev/null", timeout=8)
    vms = []
    for line in out.strip().split("\n"):
        parts = line.split()
        if len(parts) >= 2:
            vmid, name = parts[0], parts[-1]
            if vmid.isdigit(): vms.append({"vmid": vmid, "name": name})
    return vms

def build_config():
    pihole = get_pihole_devices()
    print(f"[scan] Pi-hole: {len(pihole)} devices")

    # Static galaxy definitions
    galaxies = [
        {"id":"proxcluster","name":"🌌 Proxmox Cluster","x":-30,"y":0,"z":-12,"r":30,"color":34543},
        {"id":"speedport","name":"🌌 Speedport (.1)","x":30,"y":0,"z":-15,"r":14,"color":16755200},
        {"id":"meshrepeater","name":"🌌 Mesh AP (.164)","x":0,"y":0,"z":28,"r":12,"color":16711935},
        {"id":"gs308","name":"🌌 GS308Ev4 (Büro)","x":0,"y":0,"z":22,"r":12,"color":43690},
        {"id":"kellerswitch","name":"🌌 Keller-Switch (.30)","x":30,"y":0,"z":22,"r":9,"color":65535},
        {"id":"knx-universe","name":"🌌 KNX Bus-Universum","x":-5,"y":0,"z":-30,"r":12,"color":16744192},
    ]

    systems = []
    connections = [
        {"from":"vm106","to":"knx-if","protocol":"knx","tunnel":"knx-ip","tunnelType":"knx","status":"active","style":{"lineType":"dashed","glowColor":"#ffaa00","tubeOpacity":0.12}},
        {"from":"knx-if","to":"viessmann","protocol":"knx","status":"active","style":{"lineType":"solid","glowColor":"#ffaa00"}},
        {"from":"vm106","to":"viessmann","protocol":"knx","status":"active","style":{"lineType":"solid","glowColor":"#ff8800"}},
        {"from":"vm106","to":"shelly-rack","protocol":"mqtt","status":"active","style":{"lineType":"solid","glowColor":"#00ffcc"}},
        {"from":"ct250","to":"acemagic-n2","protocol":"wireguard","tunnel":"wg-vpn","tunnelType":"wireguard","status":"active","style":{"lineType":"dashed","glowColor":"#0088ff","tubeOpacity":0.10}},
        {"from":"ct101","to":"ct250","protocol":"dns","status":"active","style":{"lineType":"solid","glowColor":"#3388ff"}},
    ]
    packets = [
        {"id":"pkg-knx-1","type":"request","title":"KNX Telegram","from":"vm106","to":"knx-if","speed":0.002,"style":{"color":"#ffaa00","trailLength":45}},
        {"id":"pkg-knx-2","type":"response","title":"KNX ACK","from":"knx-if","to":"vm106","parentPacketId":"pkg-knx-1","speed":0.0025,"style":{"color":"#ff8800","trailLength":50}},
        {"id":"pkg-wg-1","type":"data","title":"VPN Tunnel","from":"ct250","to":"acemagic-n2","speed":0.002,"style":{"color":"#0088ff","trailLength":40}},
    ]

    NODE_POS = {"proxmox":(-16,0,0,180,8),"acemagic":(0,0,3,150,7),"xshaka":(16,0,0,140,7)}
    CT_LAYOUTS = {
        "proxmox": [(-20,4,-4),(-18,-5,5),(-12,5,3),(-14,-3,-5),(-20,3,6),(-12,-6,-2),(-16,6,1),(-18,-2,-6)],
        "acemagic": [(-3,5,0),(3,-4,-4),(5,3,5),(-4,-5,3),(2,6,-5)],
        "xshaka": [(12,5,-3),(18,3,4),(14,-4,-5),(20,-3,2),(13,-6,0),(16,6,-4)],
    }

    node_ids = []
    for node, host in PROXMOX_NODES.items():
        px, py, pz, cap, br = NODE_POS[node]
        nid = f"{node}-n{list(PROXMOX_NODES).index(node)+1}"
        node_ids.append(nid)
        systems.append({"id":nid,"name":f"🖥️ {node.capitalize()}","g":"proxcluster","node":node,
            "ipLast":NODE_IPS[node],"x":px,"y":py,"z":pz,"capacityScore":cap,
            "halos":[{"metricKey":"cpu","active":True,"baseRadius":br}],"color":33823 if node=="proxmox" else 43690 if node=="acemagic" else 65535,"isNode":True})

        # Known IPs from Speedport device list (verified 2026-08-04)
        KNOWN_IPS = {
            "100":"222","101":"188","241":"241","242":"242","243":"243","250":"250","251":"251",
            "102":"178","103":"223","104":"183","109":"162",
            "105":"184","106":"185","107":"186","108":"108","111":"111","112":"112","115":"115",
            "120":"173",
        }
        cts = get_proxmox_cts(node)
        vms = get_proxmox_vms(node)
        layout = CT_LAYOUTS.get(node, [(0,0,0)])
        li = 0

        for ct in cts:
            vmid = ct["vmid"]; name = ct["name"]
            lx, ly, lz = layout[li % len(layout)]; li += 1
            sys = {"id":f"ct{vmid}","name":name,"g":"proxcluster","node":node,
                "x":lx,"y":ly,"z":lz,"capacityScore":80,"halos":[{"metricKey":"cpu","active":True,"baseRadius":3}],"color":65535}
            # Best IP: known table > Pi-hole
            if vmid in KNOWN_IPS:
                sys["ipLast"] = KNOWN_IPS[vmid]
            elif vmid in pihole:
                sys["ipLast"] = pihole[vmid].get("name","") if isinstance(pihole[vmid], dict) else pihole[vmid]
            elif f"ct{vmid}" in pihole:
                sys["ipLast"] = pihole[f"ct{vmid}"].get("name","") if isinstance(pihole[f"ct{vmid}"], dict) else pihole[f"ct{vmid}"]
            systems.append(sys)

        for vm in vms:
            vmid = vm["vmid"]; name = vm["name"]
            lx, ly, lz = layout[li % len(layout)]; li += 1
            sys = {"id":f"vm{vmid}","name":name,"g":"proxcluster","node":node,
                "x":lx,"y":ly,"z":lz,"capacityScore":100,"halos":[{"metricKey":"cpu","active":True,"baseRadius":4}],"color":16755200}
            systems.append(sys)

    # Inter-node connections
    for i in range(len(node_ids)):
        for j in range(i+1, len(node_ids)):
            connections.append({"from":node_ids[i],"to":node_ids[j],"protocol":"ssh","status":"active",
                "style":{"lineType":"solid","glowColor":"#3388ff"}})

    # Auto-connections for known pairs
    known_pairs = [
        ("paperless-ngx","ollama","https","#ffcc00"),
        ("hermesagent","ollama","https","#ffcc00"),
        ("hermesagent","hermes-worker","ssh","#3388ff"),
        ("gitea","caddy","https","#ffcc00"),
        ("nextcloud","caddy","https","#ffcc00"),
        ("dashboard","grafana","https","#00ffcc"),
    ]
    for src_name, dst_name, proto, color in known_pairs:
        src = next((s for s in systems if s["name"]==src_name), None)
        dst = next((s for s in systems if s["name"]==dst_name), None)
        if src and dst:
            conn = {"from":src["id"],"to":dst["id"],"protocol":proto,"status":"active",
                "style":{"lineType":"solid","glowColor":color}}
            if proto in ("https",) and dst_name == "caddy":
                conn["tunnel"] = "caddy"; conn["tunnelType"] = "proxy"
                conn["style"]["lineType"] = "dashed"; conn["style"]["tubeOpacity"] = 0.10
            if not any(c["from"]==conn["from"] and c["to"]==conn["to"] for c in connections):
                connections.append(conn)

    # Static non-Proxmox systems
    static_systems = [
        {"id":"knx-if","name":"KNX Interface","g":"knx-universe","ipLast":"40","x":0,"y":3,"z":0,"capacityScore":40,"halos":[],"color":65535},
        {"id":"viessmann","name":"Viessmann","g":"knx-universe","ipLast":"31","x":0,"y":-3,"z":0,"capacityScore":50,"halos":[],"color":16711935},
        {"id":"anker-solar","name":"Anker Solix","g":"speedport","ipLast":"32","x":5,"y":4,"z":2,"capacityScore":60,"halos":[],"color":16755200},
        {"id":"shelly-garten","name":"Garten Shelly","g":"speedport","ipLast":"138","x":0,"y":-5,"z":2,"capacityScore":40,"halos":[],"color":65535},
        {"id":"shelly-rack","name":"HomeLabRack","g":"meshrepeater","ipLast":"154","x":-5,"y":3,"z":0,"capacityScore":40,"halos":[],"color":65535},
        {"id":"womni","name":"womni","g":"meshrepeater","ipLast":"191","x":5,"y":3,"z":0,"capacityScore":80,"halos":[],"color":16755200},
        {"id":"samsung-tv","name":"Samsung TV","g":"meshrepeater","ipLast":"175","x":0,"y":-3,"z":2,"capacityScore":30,"halos":[],"color":65535},
        {"id":"magenta-tv","name":"MagentaTV ONE","g":"meshrepeater","ipLast":"42","x":3,"y":-3,"z":-2,"capacityScore":30,"halos":[],"color":16755200},
        {"id":"epson","name":"EPSON Drucker","g":"meshrepeater","ipLast":"225","x":-3,"y":-3,"z":-2,"capacityScore":20,"halos":[],"color":65535},
    ]
    for s in static_systems:
        # Update IP from Pi-hole if available
        ip_entry = pihole.get(s.get("ipLast",""), {})
        ip = ip_entry.get("ip","") if isinstance(ip_entry, dict) else ip_entry
        if not ip:
            for last_oct, entry in pihole.items():
                name = entry.get("name","") if isinstance(entry, dict) else entry
                if s["name"].lower().replace(" ","") in str(name).lower().replace(" ",""):
                    ip = last_oct; break
        if ip: s["ipLast"] = str(ip)
        systems.append(s)

    config = {
        "title": "Homelab Universe",
        "version": f"6.0-scan-{time.strftime('%H%M')}",
        "globalConfig": {
            "defaults": {"nodeCapacityScore":100,"nodeColor":65535,"staticHaloOpacity":0},
            "showAllHalos": False,
            "thresholds": [
                {"maxLoad":0.50,"color":"#00ffcc","speedMultiplier":1.0,"label":"NORMAL"},
                {"maxLoad":0.85,"color":"#ffaa00","speedMultiplier":2.2,"label":"WARNING"},
                {"maxLoad":1.00,"color":"#ff3333","speedMultiplier":4.5,"label":"CRITICAL"}
            ]
        },
        "galaxies": galaxies,
        "systems": systems,
        "connections": connections,
        "routingRules": {"forceCoreTransit": True},
        "packets": packets
    }

    with open(TARGET, "w") as f:
        json.dump(config, f, indent=2)
    print(f"[scan] Written {len(systems)} systems to {TARGET}")

def deploy():
    """SCP config to CT105 and restart API."""
    subprocess.run(["sshpass","-p","Bashment+13","scp","-o","StrictHostKeyChecking=no",
        TARGET, f"root@{DEPLOY_HOST}:/tmp/c.json"], check=True, timeout=15)
    subprocess.run(["sshpass","-p","Bashment+13","ssh","-o","StrictHostKeyChecking=no",
        f"root@{DEPLOY_HOST}",
        f"pct push {DEPLOY_CT} /tmp/c.json {DEPLOY_PATH} && pct exec {DEPLOY_CT} -- systemctl restart universe-api"],
        check=True, timeout=20)
    print("[scan] Deployed & restarted universe-api")

if __name__ == "__main__":
    build_config()
    deploy()
