import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from evidence_store import EvidenceStore

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "evidence.sqlite3"
        self.store = EvidenceStore(self.path)
    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()
    def test_roundtrip(self):
        self.store.append("a","M011","test",{"passed":2})
        self.assertEqual(self.store.get("a")["payload"], {"passed":2})
    def test_deterministic_hash(self):
        stamp = datetime(2026, 11, 6, tzinfo=timezone.utc)
        self.store.close()
        self.store = EvidenceStore(self.path, clock=lambda: stamp)
        other = EvidenceStore(Path(self.tmp.name) / "other.sqlite3", clock=lambda: stamp)
        try:
            a = self.store.append("a","M011","test",{"b":2,"a":1})
            b = other.append("a","M011","test",{"a":1,"b":2})
            self.assertEqual(a,b)
        finally:
            other.close()
    def test_duplicate_rejected(self):
        self.store.append("a","M011","test",{})
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.append("a","M011","test",{})
    def test_invalid_identifier(self):
        with self.assertRaises(ValueError):
            self.store.append("","M011","test",{})
    def test_nan_rejected(self):
        with self.assertRaises(ValueError):
            self.store.append("a","M011","test",{"x":float("nan")})
    def test_filter(self):
        self.store.append("a","M011","test",{})
        self.store.append("b","M012","test",{})
        self.assertEqual(len(self.store.list_experiment("M011")),1)
    def test_missing(self):
        self.assertIsNone(self.store.get("missing"))
    def test_persistence(self):
        self.store.append("a","M011","test",{"v":1})
        self.store.close()
        self.store = EvidenceStore(self.path)
        self.assertEqual(self.store.get("a")["payload"]["v"],1)
    def test_tamper_detected(self):
        self.store.append("a","M011","test",{"v":1})
        self.store.conn.execute("UPDATE evidence SET payload=? WHERE id='a'", ("{}",))
        with self.assertRaises(ValueError):
            self.store.get("a")

if __name__ == "__main__":
    unittest.main()
