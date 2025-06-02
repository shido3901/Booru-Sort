import tkinter as tk
import json
import os
from tkinter import filedialog

json_file_path = "saved_tags.json"
tag_list = {}

def load_tags():
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_tags(data):
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_tag(tag_name, value):
    data = load_tags()
    if tag_name not in data:
        data[tag_name] = []
    if value not in data[tag_name]:
        data[tag_name].append(value)
    save_tags(data)

def delete_tag(tag_button):
    tag_name = tag_button.tag_name

    data = load_tags()
    if tag_name in data:
        del data[tag_name]
        save_tags(data)
        tag_button.destroy()
        print(f"deleted tag '{tag_name}'")



def load_tag_buttons(tag_panel_recent_content):
    tags = load_tags()
    for tag_name, values in tags.items():
            create_tag_button(tag_panel_recent_content, tag_name, values)
        



def print_test():
    print('testingr')

def delete_tag_box(event, tag_button):
    tag_name = tag_button.tag_name

    confirm_box = tk.Toplevel(tag_button)
    confirm_box.configure(bg="#1e1e1e")
    confirm_box.resizable(False, False)

    width, height = 250, 120
    x = tag_button.winfo_rootx()
    y = tag_button.winfo_rooty() - height - 50
    if y < 0:
        y = tag_button.winfo_rooty() + 40

    confirm_box.geometry(f"{width}x{height}+{x}+{y}")
    confirm_box.focus_set()
    confirm_box.grab_set()

    tk.Label(confirm_box, text=f"Delete '{tag_name}'?", bg="#1e1e1e", fg="white", font=("Arial", 10)).pack(pady=20)

    button_frame = tk.Frame(confirm_box, bg="#1e1e1e")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Yes", command=lambda: (delete_tag(tag_button), confirm_box.destroy()),
              bg="#444", fg="white", width=10).pack(side="left", padx=10)
    tk.Button(button_frame, text="No", command=confirm_box.destroy,
              bg="#444", fg="white", width=10).pack(side="right", padx=10)

def right_click_menu(event):
    tag_button = event.widget
    tag_menu = tk.Menu(tag_button, tearoff=0, bg="#333", fg="white",
                       activebackground="#555", activeforeground="cyan", font=("Arial", 10))

    tag_menu.add_command(label="Rename", command=print_test)
    tag_menu.add_command(label="Delete", command=lambda: delete_tag_box(event, tag_button))
    tag_menu.tk_popup(event.x_root, event.y_root)

column_count = 0
row_count = 0

def create_tag_button(parent, tag_name, value):

    tag = tk.Button(parent, text=tag_name)
    tag.tag_name = tag_name
    tag.value = value

    global column_count, row_count

    tag.grid(row=row_count, column=column_count, padx=4, pady=4)
    column_count = column_count + 1

    if column_count == 6:
        row_count = row_count + 1
        column_count = 0

    tag.bind("<Button-1>", lambda event: show_drag_drop_box(tag))
    tag.bind("<Button-3>", right_click_menu)

def show_drag_drop_box(tag, event=None):
    global drop_box
    tag_name = tag.tag_name

    drop_box = tk.Toplevel(tag)
    drop_box.title("Add to tag")
    drop_box.configure(bg="#1e1e1e")
    drop_box.resizable(False, False)

    width, height = 250, 120
    x = tag.winfo_rootx()
    y = tag.winfo_rooty() - height - 50
    if y < 0:
        y = tag.winfo_rooty() + 40

    drop_box.geometry(f"{width}x{height}+{x}+{y}")
    drop_box.focus_set()
    drop_box.grab_set()
    drop_box.transient(tag)
    drop_box.bind("<Button-1>", lambda event: get_image_path(tag))

    drop_frame = tk.Frame(drop_box, width=200, height=80, bg="#2e2e2e",
                          highlightbackground="gray", highlightthickness=2, bd=0)
    drop_frame.pack(pady=20)
    drop_frame.pack_propagate(False)

    label = tk.Label(drop_frame, text=f"Add to '{tag_name}'", fg="gray",
                     bg="#2e2e2e", font=("Arial", 12))
    label.pack(expand=True)

def get_image_path(tag):
    global drop_box
    tag_name = tag.tag_name

    select_photos = filedialog.askopenfilenames(title=f"Add to {tag_name}:", filetypes=[
        ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
        ("Video Files", "*.mp4;*.mov;*.avi")
    ])

    if select_photos:
        for path in select_photos:
            file_name = os.path.basename(path)
            add_tag(tag_name, file_name)
            try:
                print(f"Added: {file_name} to tag {tag_name}")
            except UnicodeEncodeError:
                print(f"Added: {file_name.encode('utf-8')} to tag {tag_name.encode('utf-8')}")
    drop_box.destroy()
