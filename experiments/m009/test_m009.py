import unittest
from math import isclose
from m009 import step

class Tests(unittest.TestCase):
    def test_empty(self): self.assertEqual(step([]),([],0))
    def test_coincident(self): self.assertEqual(step([(0,0),(0,0)])[1],1)
    def test_repulsion(self):
        p,_=step([(0,0),(.5,0)]);self.assertGreater(p[1][0]-p[0][0],.5)
    def test_attraction(self):
        p,_=step([(0,0),(1.2,0)]);self.assertLess(p[1][0]-p[0][0],1.2)
    def test_far(self): self.assertEqual(step([(0,0),(3,0)])[0],[(0.,0.),(3.,0.)])
    def test_centroid(self):
        q=[(-1.,2.),(.2,-.3),(1.5,2.)];p,_=step(q)
        for k in (0,1): self.assertTrue(isclose(sum(x[k] for x in q),sum(x[k] for x in p),abs_tol=1e-12))
    def test_rotation(self):
        q=[(0.,0.),(.6,.2),(1.,.5)];p,_=step(q)
        rotated=[(-y,x) for x,y in q];r,_=step(rotated)
        for (x,y),(a,b) in zip(p,r):
            self.assertAlmostEqual(-y,a);self.assertAlmostEqual(x,b)
    def test_translation(self):
        q=[(0.,0.),(.6,.2)];p,_=step(q);r,_=step([(x+3,y-2) for x,y in q])
        for (x,y),(a,b) in zip(p,r):
            self.assertAlmostEqual(x+3,a);self.assertAlmostEqual(y-2,b)
    def test_invalid(self):
        for kwargs in ({'dt':0},{'radius':-1},{'reach':.5},{'repulsion':-1}):
            with self.assertRaises(ValueError):step([(0,0)],**kwargs)
    def test_nonfinite(self):
        with self.assertRaises(ValueError):step([(float('nan'),0)])
    def test_many(self):
        q=[(i*.13,(i%7)*.19) for i in range(40)]
        for _ in range(30):q,_=step(q)
        self.assertEqual(len(q),40)

if __name__=='__main__':unittest.main()
