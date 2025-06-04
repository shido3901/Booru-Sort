import tkinter as tk
import json
import os
import sys
from tkinter import filedialog
from shared_state import column_count, row_count
from load_images import show_pictures_function

if sys.platform == "win32":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

global file_path_name
file_path_name = None

json_file_path = "saved_tags.json"
tag_list = {}

def load_tag_info():
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_tag_info(data):
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

key_search_press = False

class TagProperties:
    def __init__(self, tag_panel_recent_content, tag_name="", file_path_name="", canvas=None):
        self.tag_panel_recent_content = tag_panel_recent_content
        self.tag_name = tag_name
        self.file_path_name = file_path_name
        self.canvas = canvas
    

    def add_tag(self):

        data = load_tag_info()
        if self.tag_name not in data:
            data[self.tag_name] = []

        if self.file_path_name and self.file_path_name.strip():
            if self.file_path_name not in data[self.tag_name]:
                data[self.tag_name].append(self.file_path_name)
        save_tag_info(data)

        self.create_tag_button()


    def create_tag_button(self):
        tag_name_copy = self.tag_name
        data = load_tag_info()
        import shared_state
        global column_count, row_count
        count = len(data[self.tag_name])
        grab_tag_length = len(self.tag_name)
       
        if grab_tag_length < 15:

            tag_button = tk.Button(self.tag_panel_recent_content, 
                                text=self.tag_name,
                                width=15,
                                padx=2,
                                pady=5,  
                                bg="#333333",
                                anchor=("w"),        
                                fg="white",           
                                font=("Arial", 9)
                                
                                )
        else:

            tag_button = tk.Button(self.tag_panel_recent_content, 
                                text=self.tag_name,
                                width=15,
                                padx=2,  
                                pady=5,  
                                bg="#333333",  
                                anchor=("e"),       
                                fg="white",           
                                font=("Arial", 9) 
                              
                                )
            

        tag_button_count = tk.Label(self.tag_panel_recent_content, 
                            text=count - 1,
                            width=13,
                            padx=2,  
                            pady=5,  
                            bg="#171717",  
                            fg="white", 
                            anchor=("e"),       
                        
                                )

        tag_button.tag_name = self.tag_name
        tag_button.tag_instance = self  

        tag_button.grid(row=shared_state.row_count, column=shared_state.column_count, padx=4, pady=4)
        tag_button_count.grid(row=shared_state.row_count, column=1, padx=4, pady=4)

        shared_state.row_count += 1
       
        tag_button.bind("<Button-1>", lambda event, tag_name=tag_name_copy, canvas=self.canvas: show_pictures(tag_name, canvas))


        tag_button.bind("<Button-3>", lambda event: right_click_menu(event, tag_button, self))


    def delete_tag(self, tag_button):
       
        tag_name = tag_button.tag_name

        data = load_tag_info()
        print(f"{len(data[tag_name])} entities deleted from {tag_name}")
        if tag_name in data:
                del data[tag_name]
                save_tag_info(data)
                print(f"deleted tag '{tag_name}'")
        for widget in self.tag_panel_recent_content.winfo_children():
            widget.destroy()

        import shared_state
        shared_state.column_count = 0
        shared_state.row_count = 0

        self.refresh()

    def refresh(self):
        tags = load_tag_info()
        for tag_name in tags:  
            self.tag_name = tag_name 
            self.create_tag_button()

    

#===============================================================================Show pictures in folder area=================================================================
def show_pictures(tag_name, canvas):
    file_load_count = 0
    print(f"You are showing path files of the tag {tag_name}")
    data = load_tag_info()
    if tag_name in data:
        for file_path_name in data[tag_name]:
            if file_path_name.strip():
                show_pictures_function(file_path_name, canvas)
            




#=============================================================================================================================================================

def right_click_menu(event, tag_button, tag_properties):
    tag_menu = tk.Menu(tag_button, tearoff=0, bg="#333", fg="white",
                        activebackground="#555", activeforeground="cyan", font=("Arial", 10))

    tag_menu.add_command(label="Add", command=lambda: show_drag_drop_box(tag_button))
    tag_menu.add_command(label="Delete", command=lambda: delete_tag_box(tag_button, tag_properties))
    
    tag_menu.tk_popup(event.x_root, event.y_root)




def delete_tag_box(tag_button, tag_properties):
    tag_name = tag_button.tag_name

    confirm_box = tk.Toplevel(tag_button)
    confirm_box.configure(bg="#1e1e1e")
    confirm_box.resizable(False, False)

    width, height = 300, 120
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
    tk.Button(button_frame, text="Yes", command=lambda: tag_properties.delete_tag(tag_button)).pack(side="left", padx=10)

    tk.Button(button_frame, text="No", command=confirm_box.destroy).pack(side="right", padx=10)


def show_drag_drop_box(tag_button):
    global drop_box

    tag_name = tag_button.tag_name

    drop_box = tk.Toplevel(tag_button)
    drop_box.title("Add to tag")
    drop_box.configure(bg="#1e1e1e")
    drop_box.resizable(False, False)

    width, height = 450, 230
    x = tag_button.winfo_rootx()
    y = tag_button.winfo_rooty() - height - 50
    if y < 0:
        y = tag_button.winfo_rooty() + 40

    drop_box.geometry(f"{width}x{height}+{x}+{y}")
    drop_box.focus_set()
    drop_box.grab_set()
    drop_box.transient(tag_button)
    drop_box.bind("<Button-1>", lambda event: get_image_path(tag_button))

    drop_frame = tk.Frame(drop_box, width=300, height=170, bg="#2e2e2e",
                          highlightbackground="gray", highlightthickness=2, bd=0)
    drop_frame.pack(pady=20)
    drop_frame.pack_propagate(False)

    label = tk.Label(drop_frame, text=f"Add to '{tag_name}'", fg="gray",
                     bg="#2e2e2e", font=("Arial", 12))
    label.pack(expand=True)

def get_image_path(tag_button):
    tag_name = tag_button.tag_name
    tag_properties_instance = TagProperties(tag_panel_recent_content=tag_button.master, tag_name=tag_name)
    
    select_photos = filedialog.askopenfilenames(title=f"Add to {tag_name}:", filetypes=[
        ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
        ("Video Files", "*.mp4;*.mov;*.avi")
    ])

    if select_photos:
        entity_count_added = 0
        duplicate_count = 0
        data = load_tag_info()

        for path in select_photos:
            file_path_name = os.path.abspath(path)
            tag_properties_instance.file_path_name = file_path_name
          
            
            if tag_name in data:
                if file_path_name not in data[tag_name]:
                    data[tag_name].append(file_path_name)
                    entity_count_added = entity_count_added + 1
                    save_tag_info(data)
                    try:
                        print(f"[{file_path_name}] added to tag '{tag_name}'")
                    except UnicodeEncodeError:
                        print(f"[{file_path_name.encode('utf-8')}] added to tag '{tag_name.encode('utf-8')}'")
                else:
                    try:
                        print(f"[{file_path_name}] already exists in tag {tag_name}")
                    except UnicodeEncodeError:
                        print(f"[{file_path_name.encode('utf-8')}] already exists in tag '{tag_name.encode('utf-8')}'")
                    duplicate_count = duplicate_count + 1

        save_tag_info(data)
        print(f"added {entity_count_added} entities to {tag_name}")
        print(f"{duplicate_count} duplicates")
    drop_box.destroy()
