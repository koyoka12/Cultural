import sys
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QLineEdit, QInputDialog, QMessageBox
from artifact_management.artifact import Artifact, Significance, ArtifactType
from artifact_management.visitors import VisitorGroup
from artifact_management.manager import CulturalHeritageSiteManager
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.manager = CulturalHeritageSiteManager()
        self.manager.load_artifacts()
        self.manager.load_visitors()

        self.setWindowTitle("Cultural Heritage Site Management")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        btn_frame = QHBoxLayout()
        main_layout.addLayout(btn_frame)

        self.btn_add_artifact = QPushButton("Add Artifact", self)
        self.btn_add_artifact.clicked.connect(self.add_artifact)
        btn_frame.addWidget(self.btn_add_artifact)

        self.btn_add_visitor = QPushButton("Add Visitor Group", self)
        self.btn_add_visitor.clicked.connect(self.add_visitor_group)
        btn_frame.addWidget(self.btn_add_visitor)

        self.btn_save_to_csv = QPushButton("Save to CSV", self)
        self.btn_save_to_csv.clicked.connect(self.save_to_csv)
        btn_frame.addWidget(self.btn_save_to_csv)

        self.btn_clear_csv = QPushButton("Clear CSV", self)
        self.btn_clear_csv.clicked.connect(self.clear_csv)
        btn_frame.addWidget(self.btn_clear_csv)

        self.btn_show_visitor_order = QPushButton("Show Visitor Order", self)
        self.btn_show_visitor_order.clicked.connect(self.show_visitor_order)
        btn_frame.addWidget(self.btn_show_visitor_order)

        self.status_label = QLabel("", self)
        main_layout.addWidget(self.status_label)

        self.show()

    def ask_for_artifact_info(self):
        artifact_id, ok = QInputDialog.getInt(self, "Add Artifact", "Enter artifact ID:")
        if ok:
            name, ok = QInputDialog.getText(self, "Add Artifact", "Enter artifact name:")
            if ok:
                era, ok = QInputDialog.getText(self, "Add Artifact", "Enter artifact era:")
                if ok:
                    significance, ok = QInputDialog.getText(self, "Add Artifact",
                                                            "Enter artifact significance (HIGH, MEDIUM, LOW):")
                    if ok:
                        artifact_type, ok = QInputDialog.getText(self, "Add Artifact",
                                                                 "Enter artifact type (SCULPTURE, PAINTING, DOCUMENT):")
                        if ok:
                            try:
                                new_artifact = Artifact(artifact_id, name, era, Significance[significance.upper()],
                                                        ArtifactType[artifact_type.upper()])
                                self.manager.add_artifact(new_artifact)
                                self.status_label.setText(f"Artifact {new_artifact} added.")
                            except KeyError as e:
                                self.status_label.setText(f"Invalid input for artifact: {e}")

    def ask_for_visitor_group_info(self):
        group_id, ok = QInputDialog.getInt(self, "Add Visitor Group", "Enter visitor group ID:")
        if ok:
            arrival_time, ok = QInputDialog.getText(self, "Add Visitor Group",
                                                    "Enter arrival time (YYYY-MM-DD HH:MM:SS):")
            if ok:
                reservation_priority, ok = QInputDialog.getText(self, "Add Visitor Group",
                                                                "Enter reservation priority (HIGH, MEDIUM, LOW):")
                if ok:
                    try:
                        new_visitor_group = VisitorGroup(group_id, arrival_time,
                                                         Significance[reservation_priority.upper()])
                        self.manager.add_visitor_group(new_visitor_group)
                        self.status_label.setText(f"Visitor group {new_visitor_group} added.")
                    except ValueError as e:
                        self.status_label.setText("Invalid arrival time format.")
                    except KeyError as e:
                        self.status_label.setText(f"Invalid input for visitor group: {e}")

    def add_artifact(self):
        self.ask_for_artifact_info()

    def add_visitor_group(self):
        self.ask_for_visitor_group_info()

    def save_to_csv(self):
        artifacts_df = pd.DataFrame([vars(a) for a in self.manager.artifacts])
        visitors_df = pd.DataFrame([vars(v) for v in self.manager.visitor_queue])
        artifacts_df.to_csv('artifacts.csv', index=False)
        visitors_df.to_csv('visitors.csv', index=False)
        self.status_label.setText("Data saved to CSV.")

    def clear_csv(self):
        artifact_id, ok = QInputDialog.getInt(self, "Clear CSV", "Enter artifact ID to remove:")
        if ok:
            self.manager.remove_artifact(artifact_id)
            self.save_to_csv()

    def show_visitor_order(self):
        visitor_order = "\n".join([f"{index + 1}. {group}" for index, group in enumerate(self.manager.visitor_queue)])
        QMessageBox.information(self, "Visitor Order", visitor_order)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', "Do you want to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
