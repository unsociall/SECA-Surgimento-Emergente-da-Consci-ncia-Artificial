import unittest
from cell_mechanics import Disc
from stability import simulate, centroid, max_position_error, refinement

class StabilityTests(unittest.TestCase):
    def setUp(self):
        self.cells = [Disc(0,0),Disc(.4,.1),Disc(1.25,.2),Disc(.1,1.1)]
    def test_zero_time(self):
        self.assertEqual(simulate(self.cells,0,.05),self.cells)
    def test_centroid_conserved(self):
        a=centroid(self.cells); b=centroid(simulate(self.cells,.5,.025))
        self.assertAlmostEqual(a[0],b[0],places=12)
        self.assertAlmostEqual(a[1],b[1],places=12)
    def test_refinement(self):
        errors=refinement(self.cells)
        self.assertTrue(all(errors[i+1]<errors[i] for i in range(len(errors)-1)),errors)
    def test_mismatch(self):
        with self.assertRaises(ValueError): max_position_error(self.cells,[])
    def test_invalid_dt(self):
        for dt in (0,-.1,float('nan'),float('inf')):
            with self.subTest(dt=dt),self.assertRaises(ValueError): simulate(self.cells,.5,dt)
    def test_indivisible_time(self):
        with self.assertRaises(ValueError): simulate(self.cells,.53,.1)
    def test_empty_centroid(self):
        with self.assertRaises(ValueError): centroid([])

if __name__=='__main__': unittest.main()
