from datetime import datetime, timedelta, timezone
import hashlib
from pathlib import Path
import sqlite3
import tempfile
import unittest

from evidence_store import EvidenceStore


class EnvelopeIntegrityTests(unittest.TestCase):
    def test_each_context_field_is_bound_to_the_checksum(self):
        for field, replacement in (("id", "changed"), ("experiment", "M999"),
                                   ("kind", "other"), ("created_at", "2020-01-01")):
            with self.subTest(field=field):
                store = EvidenceStore(":memory:")
                try:
                    store.append("a", "M012", "observation", {"result": 7})
                    # Field comes only from the fixed allowlist above.
                    store.conn.execute(f"UPDATE evidence SET {field}=? WHERE id='a'", (replacement,))
                    key = replacement if field == "id" else "a"
                    with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                        store.get(key)
                finally:
                    store.close()

    def test_equal_payloads_with_different_ids_have_different_hashes(self):
        store = EvidenceStore(":memory:", clock=lambda: datetime(2026, 11, 6, tzinfo=timezone.utc))
        try:
            self.assertNotEqual(store.append("a", "M012", "test", {}),
                                store.append("b", "M012", "test", {}))
        finally:
            store.close()

    def test_clock_is_normalized_to_utc_and_verified(self):
        stamp = datetime(2026, 11, 6, 12, tzinfo=timezone(timedelta(hours=-3)))
        store = EvidenceStore(":memory:", clock=lambda: stamp)
        try:
            store.append("a", "M012", "test", {})
            row = store.get("a")
            self.assertEqual(row["created_at"], "2026-11-06T15:00:00.000000+00:00")
            self.assertEqual(row["checksum_version"], 2)
            self.assertEqual(row["integrity_scope"], "envelope")
        finally:
            store.close()

    def test_naive_clock_does_not_write_record(self):
        store = EvidenceStore(":memory:", clock=lambda: datetime(2026, 11, 6))
        try:
            with self.assertRaises(ValueError):
                store.append("a", "M012", "test", {})
            self.assertIsNone(store.get("a"))
        finally:
            store.close()

    def test_unknown_checksum_version_fails_closed(self):
        store = EvidenceStore(":memory:")
        try:
            store.append("a", "M012", "test", {})
            store.conn.execute("UPDATE evidence SET checksum_version=99")
            with self.assertRaisesRegex(ValueError, "unsupported"):
                store.get("a")
        finally:
            store.close()

    def test_old_database_is_preserved_and_new_rows_use_envelopes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.sqlite3"
            payload = '{"result":7}'
            digest = hashlib.sha256(payload.encode()).hexdigest()
            conn = sqlite3.connect(path)
            conn.execute("CREATE TABLE evidence (id TEXT PRIMARY KEY, experiment TEXT NOT NULL, "
                         "kind TEXT NOT NULL, payload TEXT NOT NULL, sha256 TEXT NOT NULL, "
                         "created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            conn.execute("INSERT INTO evidence VALUES(?,?,?,?,?,?)",
                         ("old", "M011", "test", payload, digest, "2026-11-06 00:00:00"))
            conn.commit()
            conn.close()
            store = EvidenceStore(path)
            try:
                old = store.get("old")
                self.assertEqual(old["sha256"], digest)
                self.assertEqual(old["payload"], {"result": 7})
                self.assertEqual(old["integrity_scope"], "payload_only")
                self.assertEqual(old["checksum_version"], 1)
                store.append("new", "M012", "test", {"result": 7})
            finally:
                store.close()
            reopened = EvidenceStore(path)
            try:
                self.assertEqual(reopened.get("old")["sha256"], digest)
                self.assertEqual(reopened.get("new")["integrity_scope"], "envelope")
            finally:
                reopened.close()


if __name__ == "__main__":
    unittest.main()
