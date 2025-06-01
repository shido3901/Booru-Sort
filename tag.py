import tkinter as tk
import json
import os


json_file_path = "saved_tags.json"

tag_list = {}

def load_tags():
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save to JSON
def add_tag(tag_name, value):
    data = load_tags()
    data[tag_name] = value
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Saved: {tag_name} → {value}")

# Optional: create button for GUI
def create_tag_button(tag_panel_recent_content, tag_name):
    button = tk.Button(tag_panel_recent_content, text=tag_name)
    button.pack()