import unittest
from seca.cells import generations
from seca.neuron import LIFNeuron

class TestCells(unittest.TestCase):
    def test_binary_divisions(self):
        self.assertEqual(len(generations(5)), 32)
        self.assertEqual(len({c.identifier for c in generations(5)}), 32)

    def test_negative_generations(self):
        with self.assertRaises(ValueError):
            generations(-1)

class TestLIF(unittest.TestCase):
    def test_no_input_no_spikes(self):
        n = LIFNeuron()
        self.assertFalse(any(n.step(0) for _ in range(100)))

    def test_constant_input_spikes(self):
        n = LIFNeuron()
        self.assertTrue(any(n.step(40) for _ in range(100)))

    def test_invalid_dt(self):
        with self.assertRaises(ValueError):
            LIFNeuron().step(0, 0)

if __name__ == "__main__":
    unittest.main()
