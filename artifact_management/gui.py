import sys  
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
import tkinter as tk
from tkinter import ttk
from artifact_management.manager import CulturalHeritageSiteManager
from artifact_management.artifact import Artifact
def main():
    manager = CulturalHeritageSiteManager()
    manager.load_artifacts()
    manager.load_visitors()

    root = tk.Tk()
    root.title("Cultural Heritage Site Management")

    frame_artifacts = ttk.Frame(root)
    frame_artifacts.pack(side=tk.LEFT, padx=10, pady=10)

    tk.Label(frame_artifacts, text="Artifacts Tree").pack()
    button_add_artifact = tk.Button(frame_artifacts, text="Add Artifact", command=lambda: print("Add Artifact clicked"))
    button_add_artifact.pack()
    button_remove_artifact = tk.Button(frame_artifacts, text="Remove Artifact", command=lambda: print("Remove Artifact clicked"))
    button_remove_artifact.pack()

    frame_visitors = ttk.Frame(root)
    frame_visitors.pack(side=tk.LEFT, padx=10, pady=10)

    tk.Label(frame_visitors, text="Visitor Queue").pack()
    button_add_visitor = tk.Button(frame_visitors, text="Add Visitor Group", command=lambda: print("Add Visitor Group clicked"))
    button_add_visitor.pack()
    button_remove_visitor = tk.Button(frame_visitors, text="Remove Visitor Group", command=lambda: print("Remove Visitor Group clicked"))
    button_remove_visitor.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
