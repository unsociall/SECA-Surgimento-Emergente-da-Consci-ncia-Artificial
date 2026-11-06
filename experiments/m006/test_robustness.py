import unittest
from math import isfinite
from robustness import step,simulate,centroid

class Tests(unittest.TestCase):
    def test_empty(self): self.assertEqual(step([]),[])
    def test_single(self): self.assertEqual(step([(2.,3.)]),[(2.,3.)])
    def test_centroid_asymmetric(self):
        p=[(0.,0.),(.1,.2),(1.,.3),(2.,2.),(-.7,.8)]
        a=centroid(p);b=centroid(simulate(p,100,dt=.005))
        for x,y in zip(a,b): self.assertAlmostEqual(x,y,places=11)
    def test_large_population_finite(self):
        p=[((i%10)*.2,(i//10)*.2) for i in range(100)]
        self.assertTrue(all(isfinite(x) for q in simulate(p,50,dt=.005) for x in q))
    def test_translation(self):
        p=[(0.,0.),(.3,.2),(1.1,0.)];a=step(p);b=step([(x+5,y-3) for x,y in p])
        for (x,y),(u,v) in zip(a,b): self.assertAlmostEqual(u-x,5);self.assertAlmostEqual(v-y,-3)
    def test_permutation(self):
        p=[(0.,0.),(.3,.2),(1.1,0.)]
        for a,b in zip(step(p),reversed(step(list(reversed(p))))):
            self.assertAlmostEqual(a[0],b[0]);self.assertAlmostEqual(a[1],b[1])
    def test_repulsion(self): self.assertGreater(step([(0.,0.),(.2,0.)])[1][0]-step([(0.,0.),(.2,0.)])[0][0],.2)
    def test_distant(self): self.assertEqual(step([(0.,0.),(10.,0.)]),[(0.,0.),(10.,0.)])
    def test_coincident(self): self.assertNotEqual(step([(0.,0.),(0.,0.)]),[(0.,0.),(0.,0.)])
    def test_bad_dt(self):
        with self.assertRaises(ValueError): step([(0.,0.)],dt=0)
    def test_bad_point(self):
        with self.assertRaises(ValueError): step([(float('nan'),0.)])
    def test_bad_steps(self):
        with self.assertRaises(ValueError): simulate([],-1)

if __name__=="__main__": unittest.main()
