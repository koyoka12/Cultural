import sys
import os
import unittest
from datetime import datetime
from artifact_management.visitors import VisitorGroup, Significance

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

class TestVisitorGroup(unittest.TestCase):
    def setUp(self):
        self.group = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)

    def test_initialization(self):
        self.assertEqual(self.group.group_id, 1)
        self.assertEqual(self.group.arrival_time, "2024-07-04 10:00:00")
        self.assertEqual(self.group.reservation_priority, Significance.HIGH)
        self.assertIsNone(self.group.preference)

    def test_equality(self):
        group2 = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)
        self.assertEqual(self.group, group2)

if __name__ == "__main__":
    unittest.main()