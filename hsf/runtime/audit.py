"""Append-only JSONL audit log with line-level traceability."""
from __future__ import annotations
import datetime as _dt
import hashlib, json
from pathlib import Path

class AuditLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, **entry):
        entry["ts"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
        line = json.dumps(entry, sort_keys=True, default=str)
        entry_hash = hashlib.sha256(line.encode()).hexdigest()[:16]
        with self.path.open("a") as f:
            f.write(json.dumps({"h": entry_hash, **entry}, sort_keys=True, default=str) + "\n")
