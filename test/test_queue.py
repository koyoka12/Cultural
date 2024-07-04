import unittest
from datetime import datetime
from artifact_management.artifact import Significance, TourQueue

class Group:
    def __init__(self, group_id, arrival_time, reservation_priority):
        self.group_id = group_id
        self.arrival_time = arrival_time
        self.reservation_priority = reservation_priority

    def __lt__(self, other):
        if self.reservation_priority == other.reservation_priority:
            return self.arrival_time < other.arrival_time
        return self.reservation_priority > other.reservation_priority

class TestTourQueue(unittest.TestCase):
    def setUp(self):
        self.queue = TourQueue()
        self.group1 = Group(1, datetime.strptime('2024-07-04 10:00:00', '%Y-%m-%d %H:%M:%S'), Significance.HIGH)
        self.group2 = Group(2, datetime.strptime('2024-07-04 09:00:00', '%Y-%m-%d %H:%M:%S'), Significance.MEDIUM)
        self.group3 = Group(3, datetime.strptime('2024-07-04 11:00:00', '%Y-%m-%d %H:%M:%S'), Significance.LOW)

    def test_add_group(self):
        self.queue.add_group(self.group1)
        self.queue.add_group(self.group2)
        self.queue.add_group(self.group3)
        self.assertEqual(self.queue.queue, [self.group1, self.group2, self.group3])

    def test_remove_group(self):
        self.queue.add_group(self.group1)
        self.queue.add_group(self.group2)
        self.queue.add_group(self.group3)
        removed_group = self.queue.remove_group()
        self.assertEqual(removed_group, self.group1)
        self.assertEqual(self.queue.queue, [self.group2, self.group3])

    def test_peek_next_group(self):
        self.queue.add_group(self.group1)
        self.queue.add_group(self.group2)
        self.queue.add_group(self.group3)
        next_group = self.queue.peek_next_group()
        self.assertEqual(next_group, self.group1)

    def test_reschedule_group(self):
        self.queue.add_group(self.group1)
        self.queue.add_group(self.group2)
        self.queue.add_group(self.group3)
        self.queue.reschedule_group(2, '2024-07-04 08:00:00', 'HIGH')
        self.assertEqual(self.queue.queue[0].group_id, 2)
        self.assertEqual(self.queue.queue[0].arrival_time, datetime.strptime('2024-07-04 08:00:00', '%Y-%m-%d %H:%M:%S'))
        self.assertEqual(self.queue.queue[0].reservation_priority, Significance.HIGH)

    def test_parse_arrival_time(self):
        parsed_time = self.queue.parse_arrival_time('2024-07-04 10:00:00')
        self.assertEqual(parsed_time, datetime.strptime('2024-07-04 10:00:00', '%Y-%m-%d %H:%M:%S'))
        parsed_time = self.queue.parse_arrival_time('10:00')
        self.assertEqual(parsed_time, datetime.strptime('10:00', '%H:%M'))
        with self.assertRaises(ValueError):
            self.queue.parse_arrival_time('invalid time format')

if __name__ == '__main__':
    unittest.main()