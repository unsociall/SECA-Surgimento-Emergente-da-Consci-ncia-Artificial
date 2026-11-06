import unittest
from pathlib import Path
import subprocess
import sys
import tempfile
from E001_lif_current_response import LIF, run, sweep

class TestLIFExperiment(unittest.TestCase):
    def test_no_input(self):
        self.assertEqual(run(0)["spikes"], 0)
    def test_subthreshold(self):
        self.assertEqual(run(14)["spikes"], 0)
    def test_suprathreshold(self):
        self.assertGreater(run(20)["spikes"], 0)
    def test_reproducible(self):
        self.assertEqual(sweep(), sweep())
    def test_monotonic(self):
        rates = [r["rate_hz"] for r in sweep()]
        self.assertEqual(rates, sorted(rates))
    def test_bad_timestep(self):
        with self.assertRaises(ValueError):
            LIF().step(0, dt_ms=0)

    def test_invalid_duration(self):
        for value in (0, -1, 1.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                run(20, value)

    def test_cli_reproduces_versioned_csv_from_another_directory(self):
        folder = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "response.csv"
            result = subprocess.run(
                [sys.executable, str(folder / "E001_lif_current_response.py"), "--output", str(output)],
                cwd=directory, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_bytes(), (folder / "E001_results.csv").read_bytes())

if __name__ == "__main__":
    unittest.main()
