import unittest
from tagging import TagManager

class TestTagging(unittest.TestCase):
    def setUp(self):
        self.tm = TagManager()

    def test_valid_instrument_tags(self):
        self.assertTrue(self.tm.validate_tag("10-LIT-01", "instrument"))
        self.assertTrue(self.tm.validate_tag("99-PT-02", "instrument"))
        self.assertTrue(self.tm.validate_tag("01-FV-10", "instrument"))
        
        # Valid add
        tag = self.tm.add_tag("10-LIT-01", "instrument")
        self.assertEqual(tag, "10-LIT-01")
        
    def test_invalid_instrument_tags(self):
        self.assertFalse(self.tm.validate_tag("10-XIT-01", "instrument")) # Doesn't start with PTLF
        self.assertFalse(self.tm.validate_tag("1-LIT-01", "instrument")) # Not 2 digits loop
        
        with self.assertRaises(ValueError):
            self.tm.add_tag("INVALID", "instrument")

    def test_valid_equipment_tags(self):
        self.assertTrue(self.tm.validate_tag("TK-101", "equipment"))
        self.assertTrue(self.tm.validate_tag("P-101A", "equipment"))
        self.assertTrue(self.tm.validate_tag("FV-101", "equipment"))

    def test_duplicate_tags(self):
        self.tm.add_tag("10-LIT-01", "instrument")
        with self.assertRaises(ValueError):
            self.tm.add_tag("10-LIT-01", "instrument")

    def test_auto_generate_tags(self):
        tag1 = self.tm.generate_tag("instrument", "LIT", "10")
        self.assertEqual(tag1, "10-LIT-01")
        
        tag2 = self.tm.generate_tag("instrument", "LIT", "10")
        self.assertEqual(tag2, "10-LIT-02")
        
        tag3 = self.tm.generate_tag("equipment", "TK")
        self.assertEqual(tag3, "TK-101")
        
        tag4 = self.tm.generate_tag("equipment", "TK")
        self.assertEqual(tag4, "TK-102")

    def test_link_loop(self):
        sensor = self.tm.add_tag("10-LIT-01")
        controller = self.tm.add_tag("10-LIC-01")
        valve = self.tm.add_tag("10-LV-01")
        
        self.tm.link_loop("10", sensor, controller, valve)
        
        self.assertEqual(self.tm.loops["10"]["sensor"], "10-LIT-01")
        
        with self.assertRaises(ValueError):
            self.tm.link_loop("11", "11-LIT-01", None, None) # tag not registered

if __name__ == "__main__":
    unittest.main()
