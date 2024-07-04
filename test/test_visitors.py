import unittest
from datetime import datetime
from your_module import VisitorGroup, Significance  # 请将 your_module 替换为实际的模块名

class TestVisitorGroup(unittest.TestCase):
    def setUp(self):
        self.group = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)

    def test_initialization(self):
        self.assertEqual(self.group.group_id, 1)
        self.assertEqual(self.group.arrival_time, datetime.strptime("2024-07-04 10:00:00", '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(self.group.reservation_priority, Significance.HIGH)
        self.assertIsNone(self.group.preference)

    def test_initialization_with_string_priority(self):
        group = VisitorGroup(2, "2024-07-04 10:00:00", "HIGH")
        self.assertEqual(group.group_id, 2)
        self.assertEqual(group.arrival_time, datetime.strptime("2024-07-04 10:00:00", '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(group.reservation_priority, Significance.HIGH)
        self.assertIsNone(group.preference)

    def test_parse_arrival_time(self):
        group = VisitorGroup(3, "10:00", Significance.MEDIUM)
        self.assertEqual(group.arrival_time, datetime.strptime("10:00", '%H:%M'))

    def test_invalid_arrival_time(self):
        with self.assertRaises(ValueError):
            VisitorGroup(4, "invalid time", Significance.LOW)

    def test_equality(self):
        group2 = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)
        self.assertEqual(self.group, group2)

    def test_inequality(self):
        group2 = VisitorGroup(2, "2024-07-04 10:00:00", Significance.HIGH)
        self.assertNotEqual(self.group, group2)

    def test_less_than(self):
        group2 = VisitorGroup(2, "2024-07-04 09:00:00", Significance.HIGH)
        self.assertTrue(group2 < self.group)

    def test_repr(self):
        expected_repr = "VisitorGroup(1, 2024-07-04 10:00:00, Significance.HIGH, Preference=None)"
        self.assertEqual(repr(self.group), expected_repr)

if __name__ == "__main__":
    unittest.main()