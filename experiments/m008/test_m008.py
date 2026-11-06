import unittest
from m008 import forces,step

class MechanicsTests(unittest.TestCase):
 def test_overlap(self):
  f,n=forces([(0,0),(.5,0)],[.5,.5]);self.assertLess(f[0][0],0);self.assertEqual(n,0)
 def test_action_reaction(self):
  f,_=forces([(0,0),(.5,.1),(2,0)],[.5]*3);self.assertAlmostEqual(sum(x for x,y in f),0);self.assertAlmostEqual(sum(y for x,y in f),0)
 def test_translation(self):
  p=[(0,0),(.5,.2)];a,_=forces(p,[.5]*2);b,_=forces([(x+5,y-2) for x,y in p],[.5]*2)
  for (x,y),(u,v) in zip(a,b):self.assertAlmostEqual(x,u);self.assertAlmostEqual(y,v)
 def test_rotation(self):
  p=[(0,0),(.5,.2)];a,_=forces(p,[.5]*2);b,_=forces([(-y,x) for x,y in p],[.5]*2)
  for (x,y),(u,v) in zip(a,b):self.assertAlmostEqual(-y,u);self.assertAlmostEqual(x,v)
 def test_coincident_explicit(self):
  f,n=forces([(0,0),(0,0)],[.5,.5]);self.assertEqual(n,1);self.assertEqual(f,[[0,0],[0,0]])
 def test_centroid(self):
  p=[(0,0),(.5,.1),(2,0)];q,n=step(p,[.5]*3);self.assertAlmostEqual(sum(x for x,y in p),sum(x for x,y in q))
 def test_invalid(self):
  with self.assertRaises(ValueError):forces([(0,0)],[0])
  with self.assertRaises(ValueError):step([(0,0)],[1],dt=0)
 def test_distant(self):self.assertEqual(forces([(0,0),(10,0)],[.5,.5])[0],[[0,0],[0,0]])

if __name__=='__main__':unittest.main()
