import sys
import os
import unittest
from artifact_management.artifact import Artifact, ArtifactType, Significance
from artifact_management.artifact_tree import ArtifactTree

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

class TestArtifactTree(unittest.TestCase):
    def setUp(self):
        self.tree = ArtifactTree()

    def test_add_artifact(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        artifact2 = Artifact(2, "Artifact2", "Era2", Significance.MEDIUM, ArtifactType.PAINTING)
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        self.assertEqual(self.tree.root.artifact.artifact_id, 1)
        self.assertEqual(self.tree.root.right.artifact.artifact_id, 2)

    def test_remove_artifact(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        artifact2 = Artifact(2, "Artifact2", "Era2", Significance.MEDIUM, ArtifactType.PAINTING)
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        self.tree.remove_artifact(1)
        self.assertEqual(self.tree.root.artifact.artifact_id, 2)

    def test_search_artifacts_by_type_and_significance(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        artifact2 = Artifact(2, "Artifact2", "Era2", Significance.MEDIUM, ArtifactType.PAINTING)
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        found = self.tree.search_artifacts_by_type_and_significance(ArtifactType.PAINTING, Significance.MEDIUM)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].artifact_id, 2)

    def test_search_artifacts_by_era(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        artifact2 = Artifact(2, "Artifact2", "Era2", Significance.MEDIUM, ArtifactType.PAINTING)
        self.tree.add_artifact(artifact1)
        self.tree.add_artifact(artifact2)
        found = self.tree.search_artifacts_by_era("Era1")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].artifact_id, 1)

if __name__ == "__main__":
    unittest.main()