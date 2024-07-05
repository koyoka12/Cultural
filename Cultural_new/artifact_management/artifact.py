import enum

class Significance(enum.Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class ArtifactType(enum.Enum):
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
        return f"Artifact(ID={self.artifact_id}, Name={self.name}, Era={self.era}, Significance={self.significance.name}, Type={self.artifact_type.name})"

    def __eq__(self, other):
        if isinstance(other, Artifact):
            return self.artifact_id == other.artifact_id
        return False

    def __lt__(self, other):
        if isinstance(other, Artifact):
            if self.era < other.era:
                return True
            elif self.era == other.era:
                if self.significance.value < other.significance.value:
                    return True
                elif self.significance.value == self.significance.value:
                    if self.artifact_type.value < other.artifact_type.value:
                        return True
        return False
