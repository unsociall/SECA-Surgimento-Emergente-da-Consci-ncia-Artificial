from math import exp
import unittest

from seca.neuron import LIFNeuron


class TestLIFNumerics(unittest.TestCase):
    def test_nonfinite_initial_parameters_rejected(self):
        for field in ("potential", "resting", "threshold", "tau_ms", "refractory_ms",
                      "refractory_remaining_ms"):
            for value in (float("nan"), float("inf"), -float("inf")):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    LIFNeuron(**{field: value})

    def test_invalid_time_parameters_rejected(self):
        for params in ({"tau_ms": 0}, {"tau_ms": -1}, {"refractory_ms": -1},
                       {"refractory_remaining_ms": -1}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                LIFNeuron(**params)

    def test_invalid_input_does_not_advance_refractory_state(self):
        for current, dt in ((float("nan"), 1), (float("inf"), 1), (0, float("nan")),
                            (0, float("inf")), (0, 0), (0, 21)):
            neuron = LIFNeuron(refractory_remaining_ms=2)
            before = vars(neuron).copy()
            with self.subTest(current=current, dt=dt), self.assertRaises(ValueError):
                neuron.step(current, dt)
            self.assertEqual(vars(neuron), before)

    def test_mutated_parameters_are_checked_again(self):
        neuron = LIFNeuron()
        neuron.tau_ms = float("nan")
        with self.assertRaises(ValueError):
            neuron.step(20)
        self.assertEqual(neuron.potential, -70)

    def test_overflow_does_not_change_state(self):
        neuron = LIFNeuron(potential=-1e308, resting=1e308, threshold=1.5e308)
        before = vars(neuron).copy()
        with self.assertRaises(OverflowError):
            neuron.step(1e308)
        self.assertEqual(vars(neuron), before)

    def test_refractory_duration_is_two_ms_across_step_sizes(self):
        for dt in (.25, .5, 1, 2):
            neuron = LIFNeuron(refractory_remaining_ms=2)
            for _ in range(round(2 / dt)):
                self.assertFalse(neuron.step(20, dt))
                self.assertEqual(neuron.potential, -70)
            self.assertEqual(neuron.refractory_remaining_ms, 0)
            neuron.step(20, dt)
            self.assertGreater(neuron.potential, -70)

    def test_step_crossing_refractory_end_integrates_remaining_time(self):
        neuron = LIFNeuron(refractory_remaining_ms=2)
        reference = LIFNeuron()
        neuron.step(20, 3)
        reference.step(20, 1)
        self.assertEqual(neuron.potential, reference.potential)
        self.assertEqual(neuron.refractory_remaining_ms, 0)

    def test_spike_resets_voltage_and_sets_refractory_duration(self):
        neuron = LIFNeuron(potential=-56, refractory_ms=3)
        self.assertTrue(neuron.step(40))
        self.assertEqual(neuron.potential, neuron.resting)
        self.assertEqual(neuron.refractory_remaining_ms, 3)

    def test_subthreshold_refinement_approaches_analytic_solution(self):
        duration = 20
        exact = -60 - 10 * exp(-duration / 20)
        errors = []
        for dt in (1, .5, .25):
            neuron = LIFNeuron()
            for _ in range(round(duration / dt)):
                self.assertFalse(neuron.step(10, dt))
            errors.append(abs(neuron.potential - exact))
        self.assertTrue(errors[0] > errors[1] > errors[2], errors)


if __name__ == "__main__":
    unittest.main()
