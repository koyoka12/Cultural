import sys
import pandas as pd
from artifact_management.artifact_tree import ArtifactTree
from artifact_management.visitors import VisitorGroup, Significance
from artifact_management.queue import TourQueue
from artifact_management.artifact import Artifact, ArtifactType

# 添加项目目录到 sys.path，确保只执行一次
sys.path.append("E:\\Cultural")

class CulturalHeritageSiteManager:
    def __init__(self):
        self.artifact_tree = ArtifactTree()
        self.tour_queue = TourQueue()

    def load_artifacts(self):
        file_path = "E:\\Cultural\\file\\cultural_heritage_artifacts.csv"
        try:
            data = pd.read_csv(file_path)
            for _, row in data.iterrows():
                # 假设 CSV 文件中的 artifact_type 列包含的是数字，对应 ArtifactType 枚举的成员
                artifact_type_value = int(row['artifact_type'])
                artifact_type = ArtifactType(artifact_type_value)  # 根据数字访问枚举成员

                artifact = Artifact(
                    row['artifact_id'],
                    row['name'],
                    row['era'],
                    Significance[row['significance'].strip()],
                    artifact_type  # 使用访问得到的枚举成员
                )
                self.artifact_tree.add_artifact(artifact)
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except ValueError as e:
            print(f"Invalid artifact type value: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_visitors(self):
        file_path = "E:\\Cultural\\file\\cultural_heritage_visitors.csv"
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
        # 假设实现，您需要根据 ArtifactTree 类的实际实现来填充
        print("Artifacts tree display logic here.")

    def display_visitor_queue(self):
        # 假设实现，您需要根据 TourQueue 类的实际实现来填充
        for group in self.tour_queue.queue:
            print(group)

    def remove_artifact(self, artifact_id):
        # 假设实现，您需要根据 ArtifactTree 类的实际实现来填充
        print(f"Remove artifact logic with ID {artifact_id}.")

    def remove_visitor_group(self):
        # 假设实现，您需要根据 TourQueue 类的实际实现来填充
        print("Remove visitor group logic from queue.")

def main():
    # 创建文化遗产遗址管理器实例
    manager = CulturalHeritageSiteManager()
    
    # 加载文物和游客数据
    manager.load_artifacts()
    manager.load_visitors()

    # 显示初始状态
    print("Initial Artifacts Tree:")
    manager.display_artifacts_tree()
    print("\nInitial Visitor Queue:")
    manager.display_visitor_queue()

    # 执行操作，例如删除文物和游客组
    artifact_id_to_remove = 1  # 示例文物 ID
    manager.remove_artifact(artifact_id_to_remove)
    print(f"\nArtifact with ID {artifact_id_to_remove} has been removed.")

    # 从队列中移除一个游客组
    manager.remove_visitor_group()
    print("\nA visitor group has been removed from the queue.")

    # 显示操作后的状态
    print("\nFinal Artifacts Tree:")
    manager.display_artifacts_tree()
    print("\nFinal Visitor Queue:")
    manager.display_visitor_queue()

if __name__ == "__main__":
    main()