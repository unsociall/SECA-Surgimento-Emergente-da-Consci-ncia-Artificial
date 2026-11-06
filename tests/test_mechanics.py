import unittest
from math import hypot
from seca.mechanics import Cell2D, step, center

class TestMechanics(unittest.TestCase):
    def test_empty(self): self.assertEqual(step([]), [])
    def test_isolated(self): self.assertEqual(step([Cell2D(2,3)]), [Cell2D(2,3)])
    def test_repulsion(self):
        a,b=step([Cell2D(0,0),Cell2D(.2,0)])
        self.assertGreater(b.x-a.x,.2)
    def test_attraction(self):
        a,b=step([Cell2D(0,0),Cell2D(1.2,0)])
        self.assertLess(b.x-a.x,1.2)
    def test_distant(self):
        self.assertEqual(step([Cell2D(0,0),Cell2D(10,0)]),[Cell2D(0,0),Cell2D(10,0)])
    def test_center(self):
        cells=[Cell2D(0,0),Cell2D(.3,.4),Cell2D(1,0)]
        before=center(cells);after=center(step(cells))
        for x,y in zip(before,after): self.assertAlmostEqual(x,y)
    def test_coincident(self):
        a,b=step([Cell2D(0,0),Cell2D(0,0)])
        self.assertGreater(hypot(a.x-b.x,a.y-b.y),0)
    def test_invalid(self):
        with self.assertRaises(ValueError): step([Cell2D(0,0)],dt=0)
        with self.assertRaises(ValueError): step([Cell2D(0,0,0)])
        with self.assertRaises(ValueError): step([Cell2D(float('nan'),0)])
    def test_no_input_mutation(self):
        cells=[Cell2D(0,0),Cell2D(.5,0)]
        step(cells)
        self.assertEqual(cells,[Cell2D(0,0),Cell2D(.5,0)])
    def test_two_cell_center(self):
        cells=[Cell2D(0,0),Cell2D(.2,0)]
        self.assertEqual(center(step(cells)),center(cells))

if __name__=='__main__': unittest.main()
