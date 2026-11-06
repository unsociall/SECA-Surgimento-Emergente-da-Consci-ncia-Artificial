import unittest, math
from collision import pair_forces, step
class TestCollision(unittest.TestCase):
    def test_coincident_separate(self):
        p=step([(0.,0.),(0.,0.)],.1)
        self.assertGreater(math.dist(*p),0)
    def test_conservation(self):
        p=[(0,0),(0,0),(.2,.4),(3,2)]
        f=pair_forces(p)
        self.assertAlmostEqual(sum(v[0] for v in f),0)
        self.assertAlmostEqual(sum(v[1] for v in f),0)
    def test_centroid(self):
        p=[(0,0),(0,0),(.2,.4)]
        q=step(p,.1)
        for axis in (0,1):
            self.assertAlmostEqual(sum(x[axis] for x in p),sum(x[axis] for x in q))
    def test_no_contact(self): self.assertEqual(pair_forces([(0,0),(3,0)]),[(0,0),(0,0)])
    def test_reproducible(self):
        p=[(0,0)]*4
        self.assertEqual(pair_forces(p),pair_forces(p))
    def test_invalid(self):
        with self.assertRaises(ValueError): step([(0,0)],0)
        with self.assertRaises(ValueError): pair_forces([(float('nan'),0)])
    def test_finite(self):
        p=[(0.,0.)]*20
        for _ in range(100): p=step(p,.005)
        self.assertTrue(all(math.isfinite(v) for x in p for v in x))
if __name__=='__main__': unittest.main()
