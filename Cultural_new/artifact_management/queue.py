import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
import unittest
from Cultural_new.artifact_management.artifact import Significance
from datetime import datetime

class TourQueue:
    def __init__(self):
        self.queue = []

    def add_group(self, group):
        self.queue.append(group)
        self.queue.sort()

    def remove_group(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def peek_next_group(self):
        if self.queue:
            return self.queue[0]
        return None

    def reschedule_group(self, group_id, new_arrival_time, new_reservation_priority):
        new_arrival_time = self.parse_arrival_time(new_arrival_time)
        new_reservation_priority = Significance[new_reservation_priority.strip().upper()]
        for group in self.queue:
            if group.group_id == group_id:
                group.arrival_time = new_arrival_time
                group.reservation_priority = new_reservation_priority
                self.queue.sort()
                break

    def parse_arrival_time(self, arrival_time):
        try:
            return datetime.strptime(arrival_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                return datetime.strptime(arrival_time, '%H:%M')
            except ValueError:
                raise ValueError(f"Invalid arrival time format: {arrival_time}")
