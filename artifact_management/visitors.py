
import enum

class Significance(enum.Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class VisitorGroup:
    def __init__(self, group_id, arrival_time, reservation_priority):
        self.group_id = group_id
        self.arrival_time = arrival_time
        if isinstance(reservation_priority, Significance):
            self.reservation_priority = reservation_priority
        else:
            self.reservation_priority = Significance[reservation_priority.strip().upper()]

    def __repr__(self):
        return f"VisitorGroup({self.group_id}, {self.arrival_time}, {self.reservation_priority})"

    def __eq__(self, other):
        if isinstance(other, VisitorGroup):
            return self.group_id == other.group_id
        return False
        pass

