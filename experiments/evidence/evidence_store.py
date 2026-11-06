"""Offline evidence ledger, separate from biological memory simulation."""
from datetime import datetime, timezone
import hashlib
import json
import sqlite3

SCHEMA = """CREATE TABLE IF NOT EXISTS evidence (
id TEXT PRIMARY KEY, experiment TEXT NOT NULL, kind TEXT NOT NULL,
payload TEXT NOT NULL, sha256 TEXT NOT NULL,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
checksum_version INTEGER NOT NULL DEFAULT 1)"""


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _digest(identifier, experiment, kind, payload, created_at, version):
    if version == 1:
        data = payload
    elif version == 2:
        data = _canonical({"id": identifier, "experiment": experiment, "kind": kind,
                           "payload": json.loads(payload), "created_at": created_at,
                           "checksum_version": version})
    else:
        raise ValueError("unsupported evidence checksum version")
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

class EvidenceStore:
    def __init__(self, path, *, clock=None):
        self._clock = clock if clock is not None else lambda: datetime.now(timezone.utc)
        self.conn = sqlite3.connect(str(path))
        try:
            with self.conn:
                self.conn.execute(SCHEMA)
                columns = {row[1] for row in self.conn.execute("PRAGMA table_info(evidence)")}
                if "checksum_version" not in columns:
                    self.conn.execute(
                        "ALTER TABLE evidence ADD COLUMN checksum_version INTEGER NOT NULL DEFAULT 1"
                    )
        except BaseException:
            self.conn.close()
            raise

    def append(self, identifier, experiment, kind, payload):
        if not all(isinstance(x, str) and x.strip() for x in (identifier, experiment, kind)):
            raise ValueError("id, experiment and kind must be nonempty strings")
        canonical = _canonical(payload)
        now = self._clock()
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("evidence clock must return a timezone-aware datetime")
        created_at = now.astimezone(timezone.utc).isoformat(timespec="microseconds")
        digest = _digest(identifier, experiment, kind, canonical, created_at, 2)
        with self.conn:
            self.conn.execute(
                "INSERT INTO evidence(id,experiment,kind,payload,sha256,created_at,checksum_version) "
                "VALUES(?,?,?,?,?,?,?)",
                (identifier, experiment, kind, canonical, digest, created_at, 2),
            )
        return digest

    def get(self, identifier):
        row = self.conn.execute(
            "SELECT id,experiment,kind,payload,sha256,created_at,checksum_version "
            "FROM evidence WHERE id=?", (identifier,),
        ).fetchone()
        if row is None:
            return None
        identifier, experiment, kind, payload, digest, created_at, version = row
        if _digest(identifier, experiment, kind, payload, created_at, version) != digest:
            raise ValueError("evidence checksum mismatch")
        return {"id": identifier, "experiment": experiment, "kind": kind,
                "payload": json.loads(payload), "sha256": digest, "created_at": created_at,
                "checksum_version": version,
                "integrity_scope": "envelope" if version == 2 else "payload_only"}

    def list_experiment(self, experiment):
        rows = self.conn.execute("SELECT id FROM evidence WHERE experiment=? ORDER BY created_at,id", (experiment,)).fetchall()
        return [self.get(row[0]) for row in rows]

    def close(self):
        self.conn.close()
