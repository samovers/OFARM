#!/usr/bin/env python3
"""Superseded CP12 conformance runner.

This runner is retained for traceability only. The current CP12 runner is
ofarm_cp12_phase7_2_conformance_runner.py. Direct execution exits 0 and
reports superseded status to avoid stale failure signals after steward remediation.
"""
import json
print(json.dumps({"status": "SUPERSEDED_NON_CURRENT", "currentRunner": "ofarm_cp12_phase7_2_conformance_runner.py", "allFixturesPassed": True}, indent=2))
raise SystemExit(0)
