"""Integration checks for experiment selection and import isolation."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestSuiteRunner(unittest.TestCase):
    def run_fixture(self, suites):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            shutil.copyfile(Path(__file__).resolve().parents[1] / "tools/run_tests.py",
                            root / "tools/run_tests.py")
            (root / "tests").mkdir()
            (root / "tests/test_baseline.py").write_text(
                "import unittest\nclass TestBaseline(unittest.TestCase):\n"
                " def test_baseline(self): self.assertTrue(True)\n"
            )
            for suite, files in suites.items():
                folder = root / suite
                folder.mkdir(parents=True, exist_ok=True)
                for name, text in files.items():
                    (folder / name).write_text(text)
            return subprocess.run([sys.executable, str(root / "tools/run_tests.py")],
                                  capture_output=True, text=True, check=False)

    def test_failure_in_experiment_fails_the_runner(self):
        result = self.run_fixture({"experiments/failing": {"test_failure.py":
            "import unittest\nclass TestFailure(unittest.TestCase):\n"
            " def test_sentinel(self): self.fail('experiment sentinel')\n"}})
        self.assertEqual(result.returncode, 1)
        self.assertIn("experiment sentinel", result.stderr)
        self.assertIn("experiments/failing", result.stderr)

    def test_suites_with_same_module_names_are_isolated(self):
        suites = {}
        for folder, value in (("experiments/first", 1), ("experiments/second", 2)):
            suites[folder] = {"shared.py": f"VALUE = {value}\n", "test_shared.py":
                "import unittest\nfrom shared import VALUE\n"
                f"class TestShared(unittest.TestCase):\n def test_value(self): self.assertEqual(VALUE, {value})\n"}
        result = self.run_fixture(suites)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr.count("Ran 1 test"), 3)


if __name__ == "__main__":
    unittest.main()
