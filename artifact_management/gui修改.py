import sys  
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
import pandas as pd

import tkinter as tk
from tkinter import ttk, simpledialog
from artifact_management.artifact import Artifact, Significance, ArtifactType
from artifact_management.visitors import VisitorGroup
from artifact_management.manager import CulturalHeritageSiteManager

# 假设 CulturalHeritageSiteManager 类已经定义，并具有相应的方法
def main():
    # 创建文化遗产遗址管理器实例
    manager = CulturalHeritageSiteManager()
    # 加载数据（如果需要）
    manager.load_artifacts()
    manager.load_visitors()
    root = tk.Tk()
    root.title("Cultural Heritage Site Management")
    # 创建操作按钮
    btn_frame = ttk.Frame(root)
    btn_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
    btn_add_artifact = ttk.Button(btn_frame, text="Add Artifact", command=lambda: add_artifact(manager))
    btn_add_artifact.pack(side=tk.LEFT, padx=5, pady=5)
    btn_add_visitor = ttk.Button(btn_frame, text="Add Visitor Group", command=lambda: add_visitor_group(manager))
    btn_add_visitor.pack(side=tk.LEFT, padx=5, pady=5)
    btn_save_to_csv = ttk.Button(btn_frame, text="Save to CSV", command=lambda: save_to_csv(manager))
    btn_save_to_csv.pack(side=tk.LEFT, padx=5, pady=5)
    btn_clear_csv = ttk.Button(btn_frame, text="Clear CSV", command=lambda: clear_csv(manager))
    btn_clear_csv.pack(side=tk.LEFT, padx=5, pady=5)
    btn_show_visitor_order = ttk.Button(btn_frame, text="Show Visitor Order", command=lambda: show_visitor_order(manager))
    btn_show_visitor_order.pack(side=tk.LEFT, padx=5, pady=5)
    # 运行 GUI 事件循环
    root.mainloop()
def ask_for_artifact_info(root, manager):
    artifact_id = simpledialog.askinteger("Add Artifact", "Enter artifact ID:", parent=root)
    if artifact_id is not None:
        name = simpledialog.askstring("Add Artifact", "Enter artifact name:", parent=root)
        era = simpledialog.askstring("Add Artifact", "Enter artifact era:", parent=root)
        significance = simpledialog.askstring("Add Artifact", "Enter artifact significance (HIGH, MEDIUM, LOW):", parent=root)
        artifact_type = simpledialog.askstring("Add Artifact", "Enter artifact type (SCULPTURE, PAINTING, DOCUMENT):", parent=root)
        try:
            new_artifact = Artifact(artifact_id, name, era, Significance[significance], ArtifactType[artifact_type])
            manager.add_artifact(new_artifact)
            print(f"Artifact {new_artifact} added.")
        except KeyError as e:
            print(f"Invalid input for artifact: {e}")
def ask_for_visitor_group_info(root, manager):
    group_id = simpledialog.askinteger("Add Visitor Group", "Enter visitor group ID:", parent=root)
    if group_id is not None:
        arrival_time = simpledialog.askstring("Add Visitor Group", "Enter arrival time (YYYY-MM-DD HH:MM:SS):", parent=root)
        reservation_priority = simpledialog.askstring("Add Visitor Group", "Enter reservation priority (HIGH, MEDIUM, LOW):", parent=root)
        try:
            new_visitor_group = VisitorGroup(group_id, arrival_time, Significance[reservation_priority])
            manager.add_visitor_group(new_visitor_group)
            print(f"Visitor group {new_visitor_group} added.")
        except ValueError as e:
            print(f"Invalid arrival time format.")
        except KeyError as e:
            print(f"Invalid input for visitor group: {e}")
def add_artifact_button_clicked(root, manager):
    ask_for_artifact_info(root, manager)
def remove_artifact_button_clicked(root, manager):
    artifact_id = simpledialog.askinteger("Remove Artifact", "Enter artifact ID to remove:", parent=root)
    if artifact_id is not None:
        if manager.remove_artifact(artifact_id):
            print(f"Artifact with ID {artifact_id} has been removed.")
        else:
            print(f"No artifact found with ID {artifact_id}.")
def add_visitor_group_button_clicked(root, manager):
    ask_for_visitor_group_info(root, manager)
def remove_visitor_group_button_clicked(root, manager):
    group_id = simpledialog.askinteger("Remove Visitor Group", "Enter visitor group ID to remove:", parent=root)
    if group_id is not None:
        if manager.remove_visitor_group(group_id):
            print(f"Visitor group with ID {group_id} has been removed.")
        else:
            print(f"No visitor group found with ID {group_id}.")
def save_to_csv(manager):
    # 将文物和游客组数据保存到 CSV 文件
    artifacts_df = pd.DataFrame([(vars(a) for a in manager.artifacts.values())])
    visitors_df = pd.DataFrame([(vars(v) for v in manager.tour_queue.queue)])
    artifacts_df.to_csv('artifacts.csv', index=False)
    visitors_df.to_csv('visitors.csv', index=False)
    print("Data saved to CSV.")
def clear_csv(manager, filename):
    # 从 CSV 文件中删除指定 ID 的记录
    # 这里以删除文物为例，实际代码可能需要调整以适应不同情况
    artifact_id = simpledialog.askinteger("Clear CSV", "Enter artifact ID to remove:", parent=root)
    if artifact_id is not None:
        manager.remove_artifact(artifact_id)
        manager.save_to_csv()  # 假设管理器有此方法来保存更新后的数据到 CSV
def show_visitor_order(manager):
    # 显示游客进场顺序
    for index, group in enumerate(manager.tour_queue.queue, start=1):
        print(f"{index}. {group}")
if __name__ == "__main__":
    main()