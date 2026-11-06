import math
import unittest
from lineage import Lineage

class LineageTests(unittest.TestCase):
    def test_initial(self):
        l=Lineage(); self.assertEqual(len(l.cells),1); self.assertEqual(l.centroid(),(0.,0.))
    def test_two_daughters(self):
        l=Lineage(); a,b=l.divide(0); self.assertEqual((a.parent,b.parent),(0,0)); self.assertEqual((a.generation,b.generation),(1,1))
    def test_midpoint(self):
        l=Lineage(); a,b=l.divide(0,2.,.7); self.assertAlmostEqual((a.x+b.x)/2,0); self.assertAlmostEqual((a.y+b.y)/2,0)
    def test_separation(self):
        l=Lineage(); a,b=l.divide(0,2.,.7); self.assertAlmostEqual(math.hypot(a.x-b.x,a.y-b.y),2)
    def test_missing(self):
        with self.assertRaises(KeyError): Lineage().divide(99)
    def test_bad_parameters(self):
        for s,a in [(0,0),(-1,0),(float('nan'),0),(1,float('inf'))]:
            with self.subTest(s=s,a=a), self.assertRaises(ValueError): Lineage().divide(0,s,a)
    def test_determinism(self):
        a,b=Lineage(),Lineage(); self.assertEqual(a.divide(0,1,.3),b.divide(0,1,.3))
    def test_second_generation(self):
        l=Lineage(); a,b=l.divide(0); c,d=l.divide(a.identifier); self.assertEqual(len(l.cells),3); self.assertEqual((c.generation,d.generation),(2,2))
    def test_unique_ids(self):
        l=Lineage(); a,b=l.divide(0); l.divide(a.identifier); self.assertEqual(len(l.cells),len(set(l.cells)))

if __name__=='__main__': unittest.main()
