import pandas as pd
from datetime import datetime
from enum import Enum
import os

class Significance(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class ArtifactType(Enum):
    SCULPTURE = 1
    PAINTING = 2
    DOCUMENT = 3

class Artifact:
    def __init__(self, artifact_id, name, era, significance, artifact_type):
        self.artifact_id = artifact_id
        self.name = name
        self.era = era
        if isinstance(significance, Significance):
            self.significance = significance
        else:
            self.significance = Significance[significance]
        if isinstance(artifact_type, ArtifactType):
            self.artifact_type = artifact_type
        else:
            self.artifact_type = ArtifactType[artifact_type]

    def __repr__(self):
        return (f"Artifact(ID={self.artifact_id}, Name={self.name}, Era={self.era}, "
                f"Significance={self.significance.name}, Type={self.artifact_type.name})")

    def __eq__(self, other):
        if isinstance(other, Artifact):
            return self.artifact_id == other.artifact_id
        return False

    def __lt__(self, other):
        if isinstance(other, Artifact):
            return (self.era, self.significance.value, self.artifact_type.value) < \
                   (other.era, other.significance.value, other.artifact_type.value)

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
        return (f"VisitorGroup(Group ID={self.group_id}, Arrival Time={self.arrival_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Priority={self.reservation_priority.name}, Preference={self.preference})")

    def __eq__(self, other):
        if isinstance(other, VisitorGroup):
            return self.group_id == other.group_id
        return False

    def __lt__(self, other):
        if isinstance(other, VisitorGroup):
            return (self.arrival_time, self.reservation_priority.value) < (other.arrival_time, other.reservation_priority.value)
        return False


class CulturalHeritageSiteManager:
    def __init__(self):
        self.artifacts = []
        self.visitor_queue = []

    def load_artifacts(self, filename=r"E:\jiedang\第一单\file\cultural_heritage_artifacts.csv"):
        data = pd.read_csv(filename)
        for _, row in data.iterrows():
            significance_name = row['significance'].strip()
            artifact_type_name = row['artifact_type'].strip()
            artifact = Artifact(
                row['artifact_id'],
                row['name'],
                row['era'],
                significance_name,
                artifact_type_name
            )
            self.artifacts.append(artifact)

    def display_artifacts(self):
        print("Artifacts:")
        for artifact in sorted(self.artifacts, key=lambda x: (x.era, x.significance.value, x.artifact_type.value)):
            print(artifact)

    def load_visitors(self, filename=r"E:\jiedang\第一单\file\cultural_heritage_visitors.csv"):
        data = pd.read_csv(filename)
        for _, row in data.iterrows():
            preference = row['preference'].strip() if 'preference' in row and pd.notna(row['preference']) else None
            visitor_group = VisitorGroup(
                row['group_id'],
                row['arrival_time'],
                row['reservation_priority'],
                preference
            )
            self.visitor_queue.append(visitor_group)

    def display_visitor_queue(self):
        print("\nVisitor Queue (sorted by arrival time and priority):")
        for group in sorted(self.visitor_queue, key=lambda x: (x.arrival_time, x.reservation_priority.value)):
            print(group)

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        self.artifacts.sort()

    def add_visitor_group(self, visitor_group):
        self.visitor_queue.append(visitor_group)
        self.visitor_queue.sort(key=lambda x: (x.arrival_time, x.reservation_priority.value))

    def remove_artifact(self, artifact_id):
        self.artifacts = [artifact for artifact in self.artifacts if artifact.artifact_id != artifact_id]

    def remove_visitor_group(self, group_id):
        self.visitor_queue = [group for group in self.visitor_queue if group.group_id != group_id]

    def reschedule_visitor_group(self, group_id, new_arrival_time, new_priority_name):
        new_priority = Significance[new_priority_name]
        for group in self.visitor_queue:
            if group.group_id == group_id:
                group.arrival_time = datetime.strptime(new_arrival_time, '%Y-%m-%d %H:%M:%S')
                group.reservation_priority = new_priority
                self.visitor_queue.sort(key=lambda x: (x.arrival_time, x.reservation_priority.value))
                break

    def search_artifacts_by_era(self, era):
        return [artifact for artifact in self.artifacts if artifact.era == era]

    def save_to_csv(self, filename, data):
        pd.DataFrame(data).to_csv(filename, index=False)

def main():
    manager = CulturalHeritageSiteManager()
    manager.load_artifacts()
    manager.load_visitors()
    manager.display_artifacts()
    manager.display_visitor_queue()

if __name__ == "__main__":
    main()
