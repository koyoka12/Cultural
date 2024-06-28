import sys  
sys.path.append("E:\Cultural") 
import unittest
from artifact_management.artifact import Significance


class TourQueue:
    def __init__(self):
        self.queue = []

    def add_group(self, group):
        self.queue.append(group)
        self.queue.sort(key=lambda x: (x.arrival_time, x.reservation_priority.value))

    def remove_group(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def peek_next_group(self):
        if self.queue:
            return self.queue[0]
        return None

    def reschedule_group(self, group_id, new_arrival_time, new_reservation_priority):
        for group in self.queue:
            if group.group_id == group_id:
                group.arrival_time = new_arrival_time
                group.reservation_priority = Significance[new_reservation_priority.strip().upper()]
                self.queue.sort(key=lambda x: (x.arrival_time, x.reservation_priority.value))
                break
