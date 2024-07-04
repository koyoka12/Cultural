import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog, QMessageBox, QGridLayout
from artifact_management.artifact import Artifact, Significance, ArtifactType
from artifact_management.visitors import VisitorGroup
from artifact_management.manager import CulturalHeritageSiteManager
import warnings

# 忽略弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 设置环境变量
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# 获取当前文件的路径和项目根目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# 定义主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建文化遗产遗址管理器实例
        self.manager = CulturalHeritageSiteManager()
        # 加载数据（如果需要）
        self.manager.load_artifacts()
        self.manager.load_visitors()

        # 设置窗口标题和大小
        self.setWindowTitle("Cultural Heritage Site Management")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        btn_layout = QGridLayout()
        main_layout.addLayout(btn_layout)

        # 创建操作按钮
        self.create_buttons(btn_layout)
        # 创建状态标签
        self.status_label = QLabel("", self)
        main_layout.addWidget(self.status_label)

        self.show()

    def create_buttons(self, layout):
        # 添加文物按钮
        self.btn_add_artifact = QPushButton("Add Artifact", self)
        self.btn_add_artifact.clicked.connect(self.add_artifact)
        layout.addWidget(self.btn_add_artifact, 0, 0)

        # 添加游客组按钮
        self.btn_add_visitor = QPushButton("Add Visitor Group", self)
        self.btn_add_visitor.clicked.connect(self.add_visitor_group)
        layout.addWidget(self.btn_add_visitor, 0, 1)

        # 保存到CSV按钮
        self.btn_save_to_csv = QPushButton("Save to CSV", self)
        self.btn_save_to_csv.clicked.connect(self.save_to_csv)
        layout.addWidget(self.btn_save_to_csv, 1, 0)

        # 清除CSV按钮
        self.btn_clear_csv = QPushButton("Clear CSV", self)
        self.btn_clear_csv.clicked.connect(self.clear_csv)
        layout.addWidget(self.btn_clear_csv, 1, 1)

        # 显示游客顺序按钮
        self.btn_show_visitor_order = QPushButton("Show Visitor Order", self)
        self.btn_show_visitor_order.clicked.connect(self.show_visitor_order)
        layout.addWidget(self.btn_show_visitor_order, 2, 0, 1, 2)

        # 搜索文物按钮
        self.btn_search_artifacts = QPushButton("Search Artifacts", self)
        self.btn_search_artifacts.clicked.connect(self.search_artifacts)
        layout.addWidget(self.btn_search_artifacts, 3, 0, 1, 2)

    # 获取文物信息并且添加文物
    def ask_for_artifact_info(self):
        artifact_id, ok = QInputDialog.getInt(self, "Add Artifact", "Enter artifact ID:")
        if ok:
            name, ok = QInputDialog.getText(self, "Add Artifact", "Enter artifact name:")
            if ok:
                era, ok = QInputDialog.getText(self, "Add Artifact", "Enter artifact era:")
                if ok:
                    significance, ok = QInputDialog.getText(self, "Add Artifact", "Enter artifact significance (HIGH, MEDIUM, LOW):")
                    if ok:
                        artifact_type, ok = QInputDialog.getText(self, "Add Artifact", "Enter artifact type (SCULPTURE, PAINTING, DOCUMENT):")
                        if ok:
                            try:
                                new_artifact = Artifact(artifact_id, name, era, Significance[significance.upper()], ArtifactType[artifact_type.upper()])
                                self.manager.add_artifact(new_artifact)
                                self.status_label.setText(f"Artifact {new_artifact} added.")
                            except KeyError as e:
                                self.status_label.setText(f"Invalid input for artifact: {e}")

    # 获取游客组信息并且添加游客组
    def ask_for_visitor_group_info(self):
        group_id, ok = QInputDialog.getInt(self, "Add Visitor Group", "Enter visitor group ID:")
        if ok:
            arrival_time, ok = QInputDialog.getText(self, "Add Visitor Group", "Enter arrival time (YYYY-MM-DD HH:MM:SS or HH:MM):")
            if ok:
                reservation_priority, ok = QInputDialog.getText(self, "Add Visitor Group", "Enter reservation priority (HIGH, MEDIUM, LOW):")
                if ok:
                    preference, ok = QInputDialog.getText(self, "Add Visitor Group", "Enter artifact era preference (optional):")
                    if ok:
                        preference = preference if preference else None
                        try:
                            new_visitor_group = VisitorGroup(group_id, arrival_time, Significance[reservation_priority.upper()], preference)
                            self.manager.add_visitor_group(new_visitor_group)
                            self.status_label.setText(f"Visitor group {new_visitor_group} added.")
                        except ValueError as e:
                            self.status_label.setText(f"Invalid arrival time format: {e}")
                        except KeyError as e:
                            self.status_label.setText(f"Invalid input for visitor group: {e}")

    # 添加文物
    def add_artifact(self):
        self.ask_for_artifact_info()

    # 添加游客组
    def add_visitor_group(self):
        self.ask_for_visitor_group_info()

    # 保存数据到CSV文件
    def save_to_csv(self):
        output_dir = 'output'  # 创建output文件夹保存数据到文件夹
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        artifacts_df = pd.DataFrame([vars(a) for a in self.manager.artifacts])
        visitors_df = pd.DataFrame([vars(v) for v in self.manager.visitor_queue])
        artifacts_df.to_csv(os.path.join(output_dir, 'artifacts.csv'), index=False)
        visitors_df.to_csv(os.path.join(output_dir, 'visitors.csv'), index=False)
        self.status_label.setText("Data saved to CSV.")

    # 清除CSV文件数据
    def clear_csv(self):
        artifact_id, ok = QInputDialog.getInt(self, "Clear CSV", "Enter artifact ID to remove:")
        if ok:
            self.manager.remove_artifact(artifact_id)
            self.save_to_csv()

    # 显示游客组顺序
    def show_visitor_order(self):
        visitor_order = "\n".join([f"{index + 1}. {group}" for index, group in enumerate(self.manager.visitor_queue)])
        QMessageBox.information(self, "Visitor Order", visitor_order)

    # 根据游客对文物的年代喜好来搜索文物，并将搜索结果保存到search_result文件夹下
    def search_artifacts(self):
        era, ok = QInputDialog.getText(self, "Search Artifacts", "Enter artifact era to search:")
        if ok:
            matching_artifacts = self.manager.search_artifacts_by_era(era)
            result = "\n".join([str(artifact) for artifact in matching_artifacts])
            QMessageBox.information(self, "Search Results", result)
            if matching_artifacts:
                search_result_dir = 'search_result'
                if not os.path.exists(search_result_dir):
                    os.makedirs(search_result_dir)
                result_df = pd.DataFrame([vars(a) for a in matching_artifacts])
                result_df.to_csv(os.path.join(search_result_dir, f'{era}_artifacts.csv'), index=False)
                self.status_label.setText(f"Search results saved to {search_result_dir}/{era}_artifacts.csv")
            else:
                self.status_label.setText("No matching artifacts found.")

    # 关闭窗口
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', "Do you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
