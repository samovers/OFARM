"""The construction report uses one pinned JSON schema artifact."""

import json
from pathlib import Path


REPORT_SCHEMA = json.loads((Path(__file__).resolve().parent / 'construction-report.schema.json').read_bytes())
