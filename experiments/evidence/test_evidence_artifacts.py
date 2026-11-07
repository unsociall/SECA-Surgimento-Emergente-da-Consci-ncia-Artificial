from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from evidence_store import EvidenceStore


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.outputs = self.root / "outputs"
        self.outputs.mkdir()
        self.database = self.root / "source.sqlite3"
        stamp = datetime(2026, 11, 6, tzinfo=timezone.utc)
        self.store = EvidenceStore(self.database, clock=lambda: stamp)
        self.store.append("b", "M013", "result", {"value": 2, "note": "ação"})
        self.store.append("a", "CONTROL", "result", {"value": 1})

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def assert_outputs(self, *names):
        self.assertEqual(sorted(p.name for p in self.outputs.iterdir()), sorted(names))

    def assert_metadata(self, path, info, records):
        self.assertEqual(info["records"], records)
        self.assertEqual(info["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(info["size_bytes"], path.stat().st_size)
        self.assertTrue(info["file_fsynced"])
        self.assertIsInstance(info["directory_fsynced"], bool)

    def test_export_is_deterministic_sorted_and_verified(self):
        first, second = self.outputs / "first.jsonl", self.outputs / "second.jsonl"
        info = self.store.export_jsonl(first)
        repeated = self.store.export_jsonl(second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(info["sha256"], repeated["sha256"])
        rows = [json.loads(line) for line in first.read_text().splitlines()]
        self.assertEqual([r["id"] for r in rows], ["a", "b"])
        self.assertEqual(rows, [self.store.get("a"), self.store.get("b")])
        self.assertEqual(rows[1]["payload"]["note"], "ação")
        self.assertEqual(info["legacy_records"], 0)
        self.assert_metadata(first, info, 2)
        self.assertFalse(self.store.conn.in_transaction)
        self.assertEqual(self.store.conn.execute("SELECT COUNT(*) FROM evidence").fetchone()[0], 2)
        self.assert_outputs(first.name, second.name)

    def test_export_can_select_an_experiment(self):
        path = self.outputs / "selected.jsonl"
        info = self.store.export_jsonl(path, experiment="M013")
        self.assert_metadata(path, info, 1)
        self.assertEqual(json.loads(path.read_text())["id"], "b")

    def test_empty_export_is_a_valid_empty_artifact(self):
        path = self.outputs / "empty.jsonl"
        info = self.store.export_jsonl(path, experiment="missing")
        self.assertEqual(path.read_bytes(), b"")
        self.assert_metadata(path, info, 0)

    def test_invalid_experiment_does_not_create_files(self):
        for value in ("", "  ", 1, []):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.store.export_jsonl(self.outputs / "invalid.jsonl", experiment=value)
        self.assert_outputs()

    def test_corrupt_evidence_does_not_replace_previous_artifacts(self):
        with self.store.conn:
            self.store.conn.execute("UPDATE evidence SET kind='changed' WHERE id='b'")
        for name in ("export_jsonl", "backup_sqlite"):
            path = self.outputs / name
            path.write_bytes(b"previous artifact")
            with self.subTest(method=name), self.assertRaisesRegex(ValueError, "checksum mismatch"):
                getattr(self.store, name)(path)
            self.assertEqual(path.read_bytes(), b"previous artifact")
            self.assertFalse(self.store.conn.in_transaction)
        self.assert_outputs("export_jsonl", "backup_sqlite")

    def test_unknown_record_version_is_not_archived(self):
        with self.store.conn:
            self.store.conn.execute("UPDATE evidence SET checksum_version=99 WHERE id='b'")
        for name in ("export_jsonl", "backup_sqlite"):
            with self.subTest(method=name), self.assertRaisesRegex(ValueError, "unsupported"):
                getattr(self.store, name)(self.outputs / name)
        self.assert_outputs()

    def test_caller_transaction_is_neither_committed_nor_rolled_back(self):
        self.store.conn.execute("BEGIN")
        for name in ("export_jsonl", "backup_sqlite"):
            with self.subTest(method=name), self.assertRaises(RuntimeError):
                getattr(self.store, name)(self.outputs / name)
            self.assertTrue(self.store.conn.in_transaction)
        self.store.conn.rollback()
        self.assert_outputs()

    def test_live_database_and_sidecars_cannot_be_destinations(self):
        for name in ("export_jsonl", "backup_sqlite"):
            for suffix in ("", "-wal", "-shm", "-journal"):
                with self.subTest(method=name, suffix=suffix), self.assertRaisesRegex(ValueError, "overlaps"):
                    getattr(self.store, name)(str(self.database) + suffix)
        self.assertEqual(self.store.get("b")["payload"]["value"], 2)
        self.assert_outputs()

    def test_hardlink_to_live_database_is_rejected(self):
        path = self.outputs / "alias.sqlite3"
        try:
            os.link(self.database, path)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(str(exc))
        for name in ("export_jsonl", "backup_sqlite"):
            with self.subTest(method=name), self.assertRaisesRegex(ValueError, "overlaps"):
                getattr(self.store, name)(path)
        self.assertEqual(self.store.get("a")["payload"], {"value": 1})

    def test_symlink_destination_is_rejected_without_touching_its_target(self):
        target = self.outputs / "original"
        target.write_bytes(b"keep")
        path = self.outputs / "link"
        try:
            path.symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(str(exc))
        for name in ("export_jsonl", "backup_sqlite"):
            with self.subTest(method=name), self.assertRaisesRegex(ValueError, "symlink"):
                getattr(self.store, name)(path)
        self.assertTrue(path.is_symlink())
        self.assertEqual(target.read_bytes(), b"keep")

    def test_temporary_file_permission_failure_has_no_in_place_fallback(self):
        path = self.outputs / "existing"
        path.write_bytes(b"keep")
        with mock.patch("evidence_io.os.open", side_effect=PermissionError("denied")) as opener:
            with self.assertRaises(PermissionError):
                self.store.export_jsonl(path)
        opener.assert_called_once()
        self.assertEqual(path.read_bytes(), b"keep")
        self.assert_outputs(path.name)

    def test_temporary_name_collision_is_not_reused_or_removed(self):
        path = self.outputs / "existing"
        path.write_bytes(b"keep")
        planted = self.outputs / ".existing.fixed.partial"
        planted.write_bytes(b"belongs to another operation")
        with mock.patch("evidence_io.uuid4", return_value=SimpleNamespace(hex="fixed")):
            with self.assertRaises(FileExistsError):
                self.store.export_jsonl(path)
        self.assertEqual(path.read_bytes(), b"keep")
        self.assertEqual(planted.read_bytes(), b"belongs to another operation")
        self.assert_outputs(path.name, planted.name)

    def test_file_fsync_failure_preserves_previous_artifact(self):
        for name in ("export_jsonl", "backup_sqlite"):
            path = self.outputs / name
            path.write_bytes(b"keep")
            with self.subTest(method=name), mock.patch("evidence_io.os.fsync", side_effect=OSError("sync failed")):
                with self.assertRaises(OSError):
                    getattr(self.store, name)(path)
            self.assertEqual(path.read_bytes(), b"keep")
        self.assert_outputs("export_jsonl", "backup_sqlite")

    def test_replace_failure_preserves_previous_artifact(self):
        path = self.outputs / "existing.jsonl"
        path.write_bytes(b"keep")
        with mock.patch("evidence_io.os.replace", side_effect=PermissionError("rename refused")):
            with self.assertRaises(PermissionError):
                self.store.export_jsonl(path)
        self.assertEqual(path.read_bytes(), b"keep")
        self.assert_outputs(path.name)

    def test_directory_sync_limitation_is_reported_after_publication(self):
        path = self.outputs / "result.jsonl"
        with mock.patch("evidence_io._sync_directory", return_value=False):
            info = self.store.export_jsonl(path)
        self.assertFalse(info["directory_fsynced"])
        self.assert_metadata(path, info, 2)

    def test_export_snapshot_excludes_a_mid_export_wal_commit(self):
        self.store.conn.execute("PRAGMA journal_mode=WAL")
        writer = EvidenceStore(self.database)
        original = self.store._verified_record
        written = False

        def verify(row):
            nonlocal written
            if not written:
                writer.append("c", "M013", "later", {"value": 3})
                written = True
            return original(row)

        try:
            with mock.patch.object(self.store, "_verified_record", side_effect=verify):
                path = self.outputs / "snapshot.jsonl"
                info = self.store.export_jsonl(path)
            self.assertEqual([json.loads(line)["id"] for line in path.read_text().splitlines()], ["a", "b"])
            self.assertEqual(info["records"], 2)
            self.assertIsNotNone(self.store.get("c"))
        finally:
            writer.close()

    def test_backup_contains_committed_wal_rows_and_reopens_as_one_file(self):
        self.store.conn.execute("PRAGMA journal_mode=WAL")
        self.store.conn.execute("PRAGMA wal_autocheckpoint=0")
        self.store.append("c", "M013", "result", {"value": 3})
        self.assertGreater(Path(str(self.database) + "-wal").stat().st_size, 0)
        path = self.outputs / "snapshot.sqlite3"
        info = self.store.backup_sqlite(path)
        self.assert_metadata(path, info, 3)
        restored = EvidenceStore(path)
        try:
            self.assertEqual(restored.get("c"), self.store.get("c"))
            self.assertEqual(restored.conn.execute("PRAGMA journal_mode").fetchone()[0], "delete")
        finally:
            restored.close()
        self.assert_outputs(path.name)

    def test_in_memory_database_can_be_backed_up(self):
        memory = EvidenceStore(":memory:")
        path = self.outputs / "memory.sqlite3"
        try:
            memory.append("m", "M013", "test", {"memory": True})
            info = memory.backup_sqlite(path)
        finally:
            memory.close()
        restored = EvidenceStore(path)
        try:
            self.assertEqual(restored.get("m")["payload"], {"memory": True})
            self.assert_metadata(path, info, 1)
        finally:
            restored.close()

    def test_legacy_record_scope_and_hash_survive_export_and_backup(self):
        payload = '{"legacy":true}'
        checksum = hashlib.sha256(payload.encode()).hexdigest()
        with self.store.conn:
            self.store.conn.execute(
                "INSERT INTO evidence VALUES(?,?,?,?,?,?,?)",
                ("old", "M011", "test", payload, checksum, "2026-11-06 00:00:00", 1),
            )
        export = self.outputs / "legacy.jsonl"
        backup = self.outputs / "legacy.sqlite3"
        for info in (self.store.export_jsonl(export), self.store.backup_sqlite(backup)):
            self.assertEqual(info["legacy_records"], 1)
        rows = [json.loads(line) for line in export.read_text().splitlines()]
        legacy = next(row for row in rows if row["id"] == "old")
        self.assertEqual(legacy["sha256"], checksum)
        self.assertEqual(legacy["integrity_scope"], "payload_only")
        restored = EvidenceStore(backup)
        try:
            self.assertEqual(restored.get("old"), legacy)
        finally:
            restored.close()

    def test_backup_copy_deadline_preserves_old_output(self):
        path = self.outputs / "existing.sqlite3"
        path.write_bytes(b"old backup")
        with mock.patch("evidence_store.time.monotonic", side_effect=[0, 11]):
            with self.assertRaises(TimeoutError):
                self.store.backup_sqlite(path, timeout_s=10)
        self.assertEqual(path.read_bytes(), b"old backup")
        self.assert_outputs(path.name)

    def test_invalid_backup_timeout_does_not_create_files(self):
        for value in (0, -1, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.store.backup_sqlite(self.outputs / "invalid", timeout_s=value)
        self.assert_outputs()

    @unittest.skipUnless(os.name == "posix", "POSIX file permissions")
    def test_artifacts_are_private_files_on_posix(self):
        for name in ("export_jsonl", "backup_sqlite"):
            path = self.outputs / name
            getattr(self.store, name)(path)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_missing_parent_is_not_silently_created(self):
        path = self.outputs / "missing" / "artifact"
        with self.assertRaises(FileNotFoundError):
            self.store.export_jsonl(path)
        self.assertFalse(path.parent.exists())


if __name__ == "__main__":
    unittest.main()
