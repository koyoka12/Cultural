import enum
from datetime import datetime

class Significance(enum.Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class VisitorGroup:
    def __init__(self, group_id, arrival_time, reservation_priority, preference=None):
        self.group_id = group_id
        self.arrival_time = self.parse_arrival_time(arrival_time)
        if isinstance(reservation_priority, Significance):
            self.reservation_priority = reservation_priority
        else:
            self.reservation_priority = Significance[reservation_priority.strip().upper()]
        self.preference = preference

    def parse_arrival_time(self, arrival_time):
        try:
            return datetime.strptime(arrival_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                return datetime.strptime(arrival_time, '%H:%M')
            except ValueError:
                raise ValueError(f"Invalid arrival time format: {arrival_time}")

    def __repr__(self):
        return f"VisitorGroup({self.group_id}, {self.arrival_time}, {self.reservation_priority}, Preference={self.preference})"

    def __eq__(self, other):
        if isinstance(other, VisitorGroup):
            return self.group_id == other.group_id
        return False

    def __lt__(self, other):
        if isinstance(other, VisitorGroup):
            return (self.arrival_time, self.reservation_priority.value) < (other.arrival_time, other.reservation_priority.value)
        return False
