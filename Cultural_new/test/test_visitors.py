
import unittest
from datetime import datetime
from Cultural_new.artifact_management.visitors import VisitorGroup, Significance

class TestVisitorGroup(unittest.TestCase):
    def setUp(self):
        self.group = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)


    def test_equality(self):
        group2 = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)
        self.assertEqual(self.group, group2)

if __name__ == "__main__":
    unittest.main()