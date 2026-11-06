import unittest
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

if __name__ == "__main__":
    unittest.main()
