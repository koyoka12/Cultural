import enum

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
            return
        current = self.root
        while True:
            if new_node.artifact < current.artifact:
                if current.left:
                    current = current.left
                else:
                    current.left = new_node
                    break
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = new_node
                    break

    def remove_artifact(self, artifact_id):
        def remove_helper(node, artifact_id):
            if not node:
                return None
            if node.artifact.artifact_id == artifact_id:
                if not node.left and not node.right:
                    return None
                elif not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                else:
                    successor = self.find_min(node.right)
                    node.artifact = successor.artifact
                    node.right = remove_helper(node.right, successor.artifact.artifact_id)
                    return node
            elif artifact_id < node.artifact.artifact_id:
                node.left = remove_helper(node.left, artifact_id)
                return node
            else:
                node.right = remove_helper(node.right, artifact_id)
                return node

        self.root = remove_helper(self.root, artifact_id)

    def find_min(self, node):
        while node.left:
            node = node.left
        return node

    def search_artifacts_by_type_and_significance(self, artifact_type, significance):
        found_artifacts = []
        def search_helper(node, artifact_type, significance):
            if not node:
                return
            if node.artifact.artifact_type == artifact_type and node.artifact.significance == significance:
                found_artifacts.append(node.artifact)
            search_helper(node.left, artifact_type, significance)
            search_helper(node.right, artifact_type, significance)

        search_helper(self.root, artifact_type, significance)
        return found_artifacts
       