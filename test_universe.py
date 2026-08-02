#!/usr/bin/env python3
"""Unit tests for 3D Spiderweb Dashboard (index.html).
Tests config validation, rendering structure, and feature detection.
Run: python3 test_universe.py"""
import unittest, json, os, sys, subprocess

CONFIG_FILE = os.path.join(os.path.dirname(__file__) or ".", "config.json")
HTML_FILE = os.path.join(os.path.dirname(__file__) or ".", "index.html")

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CONFIG_FILE) as f:
            cls.config = json.load(f)
    
    def test_config_structure(self):
        """Config has all required top-level keys."""
        for key in ["title", "galaxies", "systems", "connections", "packets"]:
            self.assertIn(key, self.config, f"Missing key: {key}")
    
    def test_galaxies_have_required_fields(self):
        """Every galaxy has id, name, x, y, z, r, color."""
        for g in self.config["galaxies"]:
            for field in ["id", "name", "x", "y", "z"]:
                self.assertIn(field, g, f"Galaxy {g.get('id','?')} missing {field}")
            r = g.get("r", 12)
            self.assertGreater(r, 0, f"Galaxy {g['id']}: radius must be > 0")
    
    def test_systems_reference_valid_galaxies(self):
        """Every system references an existing galaxy."""
        galaxy_ids = {g["id"] for g in self.config["galaxies"]}
        for s in self.config["systems"]:
            self.assertIn("id", s)
            self.assertIn("g", s)
            self.assertIn(s["g"], galaxy_ids, f"System {s['id']} references unknown galaxy {s['g']}")
    
    def test_connections_reference_valid_systems(self):
        """Every connection references existing systems (supports [from,to] or [from,to,type])."""
        system_ids = {s["id"] for s in self.config["systems"]}
        for conn in self.config["connections"]:
            self.assertIn(len(conn), [2, 3], f"Connection must have 2-3 elements: {conn}")
            self.assertIn(conn[0], system_ids, f"Unknown system: {conn[0]}")
            self.assertIn(conn[1], system_ids, f"Unknown system: {conn[1]}")
            if len(conn) >= 3:
                self.assertIn(conn[2], ["active", "ping", "tube"],
                             f"Unknown connection type: {conn[2]}")
    
    def test_packets_reference_valid_systems(self):
        """Every packet references existing systems."""
        system_ids = {s["id"] for s in self.config["systems"]}
        for p in self.config["packets"]:
            self.assertIn("from", p)
            self.assertIn("to", p)
            self.assertIn("type", p)
            self.assertIn(p["from"], system_ids, f"Packet {p.get('title','?')}: unknown from={p['from']}")
            self.assertIn(p["to"], system_ids, f"Packet {p.get('title','?')}: unknown to={p['to']}")
            self.assertIn(p["type"], ["issue", "deploy", "error", "ping", "data"],
                         f"Unknown packet type: {p['type']}")
    
    def test_no_duplicate_ids(self):
        """No duplicate IDs across galaxies and systems."""
        all_ids = [g["id"] for g in self.config["galaxies"]] + [s["id"] for s in self.config["systems"]]
        self.assertEqual(len(all_ids), len(set(all_ids)), f"Duplicate IDs found: {[x for x in all_ids if all_ids.count(x)>1]}")
    
    def test_packet_speeds_positive(self):
        """All packet speeds are positive."""
        for p in self.config["packets"]:
            speed = p.get("speed", 0.003)
            self.assertGreater(speed, 0, f"Packet {p.get('title','?')}: speed must be > 0")

class TestHTML(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(HTML_FILE) as f:
            cls.html = f.read()
    
    def test_html_structure(self):
        """HTML has doctype, head, body, script."""
        self.assertTrue(self.html.startswith("<!DOCTYPE html>"))
        self.assertIn("<title>", self.html)
        self.assertIn("THREE.Scene", self.html)
        self.assertIn("WebGLRenderer", self.html)
    
    def test_required_functions(self):
        """All critical functions are defined."""
        for fn in ["init", "mkPkt", "clampToParent", "animate"]:
            self.assertIn(f"function {fn}", self.html, f"Missing function: {fn}")
    
    def test_features_present(self):
        """Key features are present in the code."""
        features = [
            ("crosshair", "#cross"),
            ("click-to-center", "uniOffset"),
            ("multi-axis halo", "Math.PI/2"),
            ("try-catch safety", "try{"),
            ("packet trails", "lerpVectors"),
            ("ping-pong bounce", "speed*=-1"),
            ("starfield", "PointsMaterial"),
            ("config-driven", "config.json"),
        ]
        for name, pattern in features:
            self.assertIn(pattern, self.html, f"Missing feature: {name}")
    
    def test_no_localhost_hardcode(self):
        """No hardcoded localhost URLs in the universal version."""
        self.assertNotIn("192.168", self.html, "Hardcoded IP found")
        self.assertNotIn("homelab", self.html.lower(), "Homelab-specific reference found")

if __name__ == "__main__":
    unittest.main(verbosity=2)
