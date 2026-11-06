"""Offline evidence ledger; not a model of biological memory."""
import hashlib
import json
import sqlite3

SCHEMA = """CREATE TABLE IF NOT EXISTS evidence (
id TEXT PRIMARY KEY, experiment TEXT NOT NULL, kind TEXT NOT NULL,
payload TEXT NOT NULL, sha256 TEXT NOT NULL,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"""

class EvidenceStore:
    def __init__(self, path):
        self.conn = sqlite3.connect(str(path))
        self.conn.execute(SCHEMA)
        self.conn.commit()

    def append(self, identifier, experiment, kind, payload):
        if not all(isinstance(x, str) and x.strip() for x in (identifier, experiment, kind)):
            raise ValueError("id, experiment and kind must be nonempty strings")
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        with self.conn:
            self.conn.execute("INSERT INTO evidence(id,experiment,kind,payload,sha256) VALUES(?,?,?,?,?)",
                              (identifier, experiment, kind, canonical, digest))
        return digest

    def get(self, identifier):
        row = self.conn.execute("SELECT experiment,kind,payload,sha256 FROM evidence WHERE id=?", (identifier,)).fetchone()
        if row is None:
            return None
        experiment, kind, payload, digest = row
        if hashlib.sha256(payload.encode("utf-8")).hexdigest() != digest:
            raise ValueError("evidence checksum mismatch")
        return {"id": identifier, "experiment": experiment, "kind": kind,
                "payload": json.loads(payload), "sha256": digest}

    def list_experiment(self, experiment):
        rows = self.conn.execute("SELECT id FROM evidence WHERE experiment=? ORDER BY created_at,id", (experiment,)).fetchall()
        return [self.get(row[0]) for row in rows]

    def close(self):
        self.conn.close()
