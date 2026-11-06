import unittest
from convergence import evolve, distance

class ConvergenceTests(unittest.TestCase):
    def test_temporal_refinement(self):
        reference = evolve(.001)
        errors = [distance(evolve(dt),reference) for dt in (.1,.05,.025,.0125)]
        self.assertTrue(all(a>b for a,b in zip(errors,errors[1:])), errors)
    def test_deterministic(self):
        self.assertEqual(evolve(.025),evolve(.025))
    def test_invalid_grid(self):
        with self.assertRaises(ValueError): evolve(.03)

if __name__ == '__main__': unittest.main()
