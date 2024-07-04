import sys
import os
import unittest
from artifact_management.artifact import Artifact, ArtifactType, Significance
from artifact_management.visitors import VisitorGroup
from artifact_management.artifact_tree import ArtifactTree
from artifact_management.queue import TourQueue
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

class TestArtifactTree(unittest.TestCase):
    def setUp(self):
        self.tree = ArtifactTree()

    def test_add_artifact(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", "HIGH", "SCULPTURE")
        artifact2 = Artifact(2, "Artifact2", "Era2", "MEDIUM", "PAINTING")
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        self.assertEqual(self.tree.root.artifact.artifact_id, 1)
        self.assertEqual(self.tree.root.right.artifact.artifact_id, 2)

    def test_remove_artifact(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", "HIGH", "SCULPTURE")
        artifact2 = Artifact(2, "Artifact2", "Era2", "MEDIUM", "PAINTING")
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        self.tree.remove_artifact(1)
        self.assertEqual(self.tree.root.artifact.artifact_id, 2)

    def test_search_artifacts_by_type_and_significance(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", "HIGH", "SCULPTURE")
        artifact2 = Artifact(2, "Artifact2", "Era2", "MEDIUM", "PAINTING")
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        found = self.tree.search_artifacts_by_type_and_significance(ArtifactType.PAINTING, Significance.MEDIUM)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].artifact_id, 2)

    def test_search_artifacts_by_era(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", "HIGH", "SCULPTURE")
        artifact2 = Artifact(2, "Artifact2", "Era2", "MEDIUM", "PAINTING")
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        found = self.tree.search_artifacts_by_era("Era1")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].artifact_id, 1)

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
