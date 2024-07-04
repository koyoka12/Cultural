import unittest
from artifact_management.queue import TourQueue
from artifact_management.visitors import VisitorGroup
from datetime import datetime
import time

class TestTourQueue(unittest.TestCase):
    def setUp(self):
        self.queue = TourQueue()

    def test_add_group(self):
        group1 = VisitorGroup(1, time.time(), "HIGH")
        group2 = VisitorGroup(2, time.time() + 10, "LOW")
        self.queue.add_group(group1)
        self.queue.add_group(group2)
        self.assertEqual(self.queue.queue[0], group1)
        self.assertEqual(self.queue.queue[1], group2)

    def test_remove_group(self):
        group1 = VisitorGroup(1, time.time(), "HIGH")
        group2 = VisitorGroup(2, time.time() + 10, "LOW")
        self.queue.add_group(group1)
        self.queue.add_group(group2)
        removed = self.queue.remove_group()
        self.assertEqual(removed, group1)

    def test_peek_next_group(self):
        group1 = VisitorGroup(1, time.time(), "HIGH")
        group2 = VisitorGroup(2, time.time() + 10, "LOW")
        self.queue.add_group(group1)
        self.queue.add_group(group2)
        peeked = self.queue.peek_next_group()
        self.assertEqual(peeked, group1)

    def test_reschedule_group(self):
        group1 = VisitorGroup(1, time.time(), "HIGH")
        group2 = VisitorGroup(2, time.time() + 10, "LOW")
        self.queue.add_group(group1)
        self.queue.add_group(group2)
        self.queue.reschedule_group(1, time.time() + 20, "LOW")
        self.assertEqual(self.queue.queue[0], group2)
        self.assertEqual(self.queue.queue[1], group1)

if __name__ == "__main__":
    unittest.main()