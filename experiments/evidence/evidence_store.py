"""Offline evidence ledger, separate from biological memory simulation."""
from datetime import datetime, timezone
from contextlib import closing
import hashlib
import json
from math import isfinite
import sqlite3
import time

if __package__:
    from .evidence_io import publish_artifact
else:
    from evidence_io import publish_artifact

SCHEMA = """CREATE TABLE IF NOT EXISTS evidence (
id TEXT PRIMARY KEY, experiment TEXT NOT NULL, kind TEXT NOT NULL,
payload TEXT NOT NULL, sha256 TEXT NOT NULL,
created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
checksum_version INTEGER NOT NULL DEFAULT 1)"""

_READ_COLUMNS = "id,experiment,kind,payload,sha256,created_at,checksum_version"


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
            f"SELECT {_READ_COLUMNS} FROM evidence WHERE id=?", (identifier,),
        ).fetchone()
        if row is None:
            return None
        return self._verified_record(row)

    @staticmethod
    def _verified_record(row):
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

    def _artifact_preflight(self):
        if self.conn.in_transaction:
            raise RuntimeError("commit or roll back the caller's transaction before creating artifacts")
        protected = []
        for _, _, filename in self.conn.execute("PRAGMA database_list"):
            if filename:
                protected.extend(filename + suffix for suffix in ("", "-wal", "-shm", "-journal"))
        return protected

    def export_jsonl(self, destination, *, experiment=None):
        """Export verified records from one read snapshot, sorted by ID.

        Serialization is streamed per record. A failed validation or write
        does not replace the previous destination. No record is appended.
        """
        if experiment is not None and (not isinstance(experiment, str) or not experiment.strip()):
            raise ValueError("experiment must be a nonempty string or None")
        protected = self._artifact_preflight()

        def produce(handle, staging):
            counts = {"format": "seca-evidence-jsonl-v1", "records": 0, "legacy_records": 0}
            where = " WHERE experiment=?" if experiment is not None else ""
            params = (experiment,) if experiment is not None else ()
            self.conn.execute("BEGIN")
            try:
                with closing(self.conn.execute(
                    f"SELECT {_READ_COLUMNS} FROM evidence{where} ORDER BY id", params,
                )) as cursor:
                    for row in cursor:
                        record = self._verified_record(row)
                        handle.write((_canonical(record) + "\n").encode("utf-8"))
                        counts["records"] += 1
                        counts["legacy_records"] += record["checksum_version"] == 1
            finally:
                self.conn.rollback()
            return counts

        return publish_artifact(destination, produce, protected_paths=protected)

    def backup_sqlite(self, destination, *, timeout_s=10.0):
        """Copy via SQLite's backup API, then validate before publication.

        timeout_s is a cooperative deadline checked between SQLite copy
        steps. Blocking calls, validation and filesystem operations can take
        additional time. The destination must be an inactive artifact file.
        Committed source WAL data is included in the single-file backup.
        """
        if not isfinite(timeout_s) or timeout_s <= 0:
            raise ValueError("timeout_s must be positive and finite")
        protected = self._artifact_preflight()

        def produce(handle, staging):
            deadline = time.monotonic() + timeout_s

            def progress(status, remaining, total):
                if time.monotonic() >= deadline:
                    raise TimeoutError("SQLite backup copy timed out")

            counts = {"format": "seca-evidence-sqlite-v1", "records": 0, "legacy_records": 0}
            with closing(sqlite3.connect(str(staging))) as copied:
                self.conn.backup(copied, pages=128, progress=progress, sleep=min(.05, timeout_s / 10))
                if copied.execute("PRAGMA journal_mode=DELETE").fetchone()[0].lower() != "delete":
                    raise RuntimeError("backup could not be made self-contained")
                if any(row[0] != "ok" for row in copied.execute("PRAGMA quick_check")):
                    raise ValueError("backup SQLite integrity check failed")
                with closing(copied.execute(f"SELECT {_READ_COLUMNS} FROM evidence")) as cursor:
                    for row in cursor:
                        record = self._verified_record(row)
                        counts["records"] += 1
                        counts["legacy_records"] += record["checksum_version"] == 1
            return counts

        return publish_artifact(destination, produce, protected_paths=protected)

    def close(self):
        self.conn.close()
