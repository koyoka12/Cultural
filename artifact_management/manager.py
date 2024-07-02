import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
import pandas as pd
from artifact_management.artifact_tree import ArtifactTree
from artifact_management.visitors import VisitorGroup, Significance
from artifact_management.queue import TourQueue
from artifact_management.artifact import Artifact, ArtifactType

from artifact_management.artifact import Artifact

import sys
import os
import pandas as pd
from enum import Enum

# 假设这些枚举和类在相应的文件中定义，并被正确导入
from artifact_management.artifact import Artifact, ArtifactType
from artifact_management.visitors import VisitorGroup, Significance
from artifact_management.queue import TourQueue

# 确保项目根目录在 sys.path 中
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

class CulturalHeritageSiteManager:
    def __init__(self):
        self.artifact_tree = {}  # 使用字典来存储文物，键为 artifact_id
        self.tour_queue = TourQueue()

    def load_artifacts(self):
        file_path = "file/cultural_heritage_artifacts.csv"
        try:
            data = pd.read_csv(file_path)
            for _, row in data.iterrows():
                artifact_type_name = row['artifact_type'].strip()
                artifact_type = ArtifactType[artifact_type_name]
                
                artifact = Artifact(
                    row['artifact_id'],
                    row['name'],
                    row['era'],
                    Significance[row['significance'].strip()],
                    artifact_type
                )
                self.artifact_tree[artifact.artifact_id] = artifact
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except ValueError as e:
            print(f"Invalid artifact type value: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_visitors(self):
        file_path = "file/cultural_heritage_visitors.csv"
        try:
            data = pd.read_csv(file_path)
            for _, row in data.iterrows():
                visitor_group = VisitorGroup(
                    row['group_id'],
                    pd.to_datetime(row['arrival_time']),
                    Significance[row['reservation_priority'].strip()]
                )
                self.tour_queue.add_group(visitor_group)
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def display_artifacts_tree(self):
        for artifact_id, artifact in self.artifact_tree.items():
            print(f"Artifact ID: {artifact_id}, {artifact}")

    def display_visitor_queue(self):
        print("Visitor Queue:")
        for group in self.tour_queue.queue:
            print(group)

    def remove_artifact(self, artifact_id):
        if artifact_id in self.artifact_tree:
            del self.artifact_tree[artifact_id]
            print(f"Artifact with ID {artifact_id} has been removed.")
        else:
            print(f"No artifact found with ID {artifact_id}.")

    def remove_visitor_group(self):
        if self.tour_queue.queue:
            removed_group = self.tour_queue.queue.pop(0)
            print(f"Visitor group removed: {removed_group}")

def main():
    manager = CulturalHeritageSiteManager()
    manager.load_artifacts()
    manager.load_visitors()

    print("Initial Artifacts Tree:")
    manager.display_artifacts_tree()

    print("\nInitial Visitor Queue:")
    manager.display_visitor_queue()

    # 删除操作
    manager.remove_artifact(1)
    manager.remove_visitor_group()

    print("\nFinal Artifacts Tree:")
    manager.display_artifacts_tree()

    print("\nFinal Visitor Queue:")
    manager.display_visitor_queue()

if __name__ == "__main__":
    main()