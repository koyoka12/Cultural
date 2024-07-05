
import unittest
from datetime import datetime
from Cultural_new.artifact_management.manager import CulturalHeritageSiteManager, Artifact, VisitorGroup, Significance, ArtifactType


class TestCulturalHeritageSiteManager(unittest.TestCase):
    def setUp(self):
        self.manager = CulturalHeritageSiteManager()

    def test_add_artifact(self):
        artifact = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        self.manager.add_artifact(artifact)
        self.assertEqual(len(self.manager.artifacts), 1)
        self.assertEqual(self.manager.artifacts[0].artifact_id, 1)

    def test_remove_artifact(self):
        artifact = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        self.manager.add_artifact(artifact)
        self.manager.remove_artifact(1)
        self.assertEqual(len(self.manager.artifacts), 0)

    def test_add_visitor_group(self):
        visitor_group = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)
        self.manager.add_visitor_group(visitor_group)
        self.assertEqual(len(self.manager.visitor_queue), 1)
        self.assertEqual(self.manager.visitor_queue[0].group_id, 1)

    def test_remove_visitor_group(self):
        visitor_group = VisitorGroup(1, "2024-07-04 10:00:00", Significance.HIGH)
        self.manager.add_visitor_group(visitor_group)
        self.manager.remove_visitor_group(1)
        self.assertEqual(len(self.manager.visitor_queue), 0)

    def test_search_artifacts_by_era(self):
        artifact1 = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        artifact2 = Artifact(2, "Artifact2", "Era2", Significance.MEDIUM, ArtifactType.PAINTING)
        self.manager.add_artifact(artifact1)
        self.manager.add_artifact(artifact2)
        found = self.manager.search_artifacts_by_era("Era1")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].artifact_id, 1)

if __name__ == "__main__":
    unittest.main()