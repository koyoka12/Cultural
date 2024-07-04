import sys
import os
import unittest
from artifact_management.artifact import Artifact, ArtifactType, Significance


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

class TestArtifact(unittest.TestCase):
    def setUp(self):
        # 初始化测试所需的 Artifact 实例
        self.artifact1 = Artifact(1, "Artifact1", "Era1", Significance.HIGH, ArtifactType.SCULPTURE)
        self.artifact2 = Artifact(2, "Artifact2", "Era2", Significance.MEDIUM, ArtifactType.PAINTING)

    def test_artifact_initialization(self):
        # 测试 Artifact 的初始化
        self.assertEqual(self.artifact1.artifact_id, 1)
        self.assertEqual(self.artifact1.name, "Artifact1")
        self.assertEqual(self.artifact1.era, "Era1")
        self.assertEqual(self.artifact1.significance, Significance.HIGH)
        self.assertEqual(self.artifact1.artifact_type, ArtifactType.SCULPTURE)

    def test_artifact_equality(self):
        # 测试 Artifact 的相等性
        self.assertEqual(self.artifact1, self.artifact1)  # 同一个对象应相等
        self.assertNotEqual(self.artifact1, self.artifact2)  # 不同对象应不相等

    def test_artifact_less_than(self):
        # 测试 Artifact 的小于比较
        self.assertLess(self.artifact1, self.artifact2)  # 根据定义的规则，artifact1 应该小于 artifact2

    def test_artifact_representation(self):
        # 测试 Artifact 的字符串表示
        self.assertEqual(str(self.artifact1), "Artifact(ID=1, Name=Artifact1, Era=Era1, Significance=HIGH, Type=SCULPTURE)")

if __name__ == "__main__":
    unittest.main()