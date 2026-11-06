import unittest
from emotion_state import AffectState, CATEGORIES

class TestAffectState(unittest.TestCase):
    def test_count(self): self.assertEqual(len(CATEGORIES), 27)
    def test_default(self): self.assertEqual(sum(AffectState().intensities.values()), 0)
    def test_set(self):
        s=AffectState();s.set_intensity('fear',.8);self.assertEqual(s.active(),{'fear':.8})
    def test_decay(self):
        s=AffectState();s.set_intensity('joy',1);s.decay(.25);self.assertEqual(s.intensities['joy'],.25)
    def test_invalid_intensity(self):
        with self.assertRaises(ValueError): AffectState().set_intensity('fear',1.1)
    def test_invalid_category(self):
        with self.assertRaises(KeyError): AffectState().set_intensity('invalid',.5)
    def test_invalid_valence(self):
        with self.assertRaises(ValueError): AffectState(valence=2)
    def test_invalid_decay(self):
        with self.assertRaises(ValueError): AffectState().decay(-.1)
    def test_coexistence(self):
        s=AffectState();s.set_intensity('fear',.7);s.set_intensity('interest',.6);self.assertEqual(len(s.active()),2)

if __name__=='__main__': unittest.main()
