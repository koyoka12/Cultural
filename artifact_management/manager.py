import sys

sys.path.append("E:\Cultural") 
import pandas as pd 
from artifact_management.artifact_tree import ArtifactTree  
from artifact_management.visitors import VisitorGroup,  Significance
from artifact_management.queue import TourQueue
from artifact_management.artifact import Artifact
class CulturalHeritageSiteManager:
    def __init__(self):
        self.artifact_tree = ArtifactTree()
        self.tour_queue = TourQueue()

    def load_artifacts(self):
        file_path = r"../file/cultural_heritage_artifacts.csv"
        try:
            data = pd.read_csv(file_path)
            print(list(data.columns))
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            return
        except pd.errors.EmptyDataError:
            print("The file is empty.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

        for _, row in data.iterrows():
            try:
                artifact = Artifact(
                    row['artifact_id'],
                    row['name'],
                    row['era'],
                    row['significance'],
                    row['artifact_type']
                )
                self.artifact_tree.add_artifact(artifact)
            except KeyError as e:
                print(f"Missing column in CSV: {e}")

    def load_visitors(self):
        file_path = r"../file/cultural_heritage_visitors.csv"
        try:
            data = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            return
        except pd.errors.EmptyDataError:
            print("The file is empty.")
            return

        for _, row in data.iterrows():
            visitor_group = VisitorGroup(
                row['group_id'],
                row['arrival_time'],
                row['reservation_priority']
            )
            self.tour_queue.add_group(visitor_group)

    def prioritize_tour_scheduling(self, preferred_era):
        pass

    def display_artifacts_tree(self):
        def display_helper(node, indent=0):
            if node:
                print(" " * indent + str(node.artifact))
                display_helper(node.left, indent + 4)
                display_helper(node.right, indent + 4)

        display_helper(self.artifact_tree.root)

    def display_visitor_queue(self):
        for group in self.tour_queue.queue:
            print(group)

    def remove_artifact(self, artifact_id):
        self.artifact_tree.remove_artifact(artifact_id)

    def remove_visitor_group(self):
        self.tour_queue.remove_group()
