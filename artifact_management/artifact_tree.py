import enum


from artifact import Artifact

class ArtifactTreeNode:
    def __init__(self, artifact):
        self.artifact = artifact
        self.left = None
        self.right = None

class ArtifactTree:
    def __init__(self):
        self.root = None

    def add_artifact(self, artifact):
        new_node = ArtifactTreeNode(artifact)
        if not self.root:
            self.root = new_node
        else:
            self._insert_node(self.root, new_node)

    def _insert_node(self, current, new_node):
        if new_node.artifact < current.artifact:
            if current.left is None:
                current.left = new_node
            else:
                self._insert_node(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
            else:
                self._insert_node(current.right, new_node)

    def remove_artifact(self, artifact_id):
        self.root = self._remove_node(self.root, artifact_id)

    def _remove_node(self, node, artifact_id):
        if node is None:
            return node

        if artifact_id < node.artifact.artifact_id:
            node.left = self._remove_node(node.left, artifact_id)
        elif artifact_id > node.artifact.artifact_id:
            node.right = self._remove_node(node.right, artifact_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_larger_node = self._find_min(node.right)
            node.artifact = min_larger_node.artifact
            node.right = self._remove_node(node.right, min_larger_node.artifact.artifact_id)

        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search_artifacts_by_type_and_significance(self, artifact_type, significance):
        found_artifacts = []
        self._search_helper(self.root, artifact_type, significance, found_artifacts)
        return found_artifacts

    def _search_helper(self, node, artifact_type, significance, found_artifacts):
        if node is not None:
            if node.artifact.artifact_type == artifact_type and node.artifact.significance == significance:
                found_artifacts.append(node.artifact)
            self._search_helper(node.left, artifact_type, significance, found_artifacts)
            self._search_helper(node.right, artifact_type, significance, found_artifacts)

    def display(self, node=None, level=0):
        if node is not None:
            self.display(node.right, level + 1)
            print(' ' * (level * 4) + str(node.artifact))
            self.display(node.left, level + 1)

