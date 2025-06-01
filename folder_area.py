import tkinter as tk
import time
from tag import add_tag

def create_folder_area(parent):
    folder_area = tk.Frame(parent, bg="#242323", width=1600, height=1080)
    folder_area.grid(row=0, column=1, rowspan=6, sticky="nsew")

    folder_area.grid_rowconfigure(0, weight=1)
    folder_area.grid_columnconfigure(0, weight=1)

    return folder_area

def folder_area_right_click(event):
    right_click_menu = tk.Menu(event.widget, tearoff=0, bg="#333333", fg="white", activebackground="#555555", activeforeground="cyan", font=("Arial", 10))
    right_click_menu.config(bg="#171717", bd=0, relief="flat")

    right_click_menu.add_command(label="View", command=lambda: print("yo"))
    right_click_menu.add_separator()
    right_click_menu.add_command(label="New Folder", command=lambda: print("yo"))
    right_click_menu.add_separator()
    right_click_menu.add_command(label="New tag", command=lambda: create_tag_window(event))

    right_click_menu.tk_popup(event.x_root, event.y_root)

tag_in_progress = False

def create_tag_window(event):
    global tag_frame, tag_entry, tag_in_progress
   
    if tag_in_progress is True:
        tag_frame.destroy()
        tag_in_progress = False

    x = event.widget.winfo_pointerx() - event.widget.winfo_rootx()
    y = event.widget.winfo_pointery() - event.widget.winfo_rooty()

    tag_frame = tk.Frame(event.widget, width=320, height=60, borderwidth=2, relief=tk.RIDGE, bg='#171717')
    tag_frame.place(x=x, y=y)  

    label = tk.Label(tag_frame, text="Tag name:", fg="white", bg='#171717')
    label.pack(pady=(5, 0), anchor='c', padx=5)

    tag_entry = tk.Entry(tag_frame, bg="#242323", fg="white", insertbackground="white")
    tag_entry.pack(padx=15, pady=15, fill='x')
    tag_entry.focus_set()

    tag_in_progress = True

    tag_frame.bind("<Enter>", inside_frame)
    tag_frame.bind("<Leave>", outside_frame)

    tag_entry.bind("<Return>", confirm_tag)
    tag_entry.bind("<Escape>", exit_tag_frame)

def confirm_tag(event):
    global tag_frame, tag_name, tag_entry
    tag_name = tag_entry.get()
    if not tag_entry.get().strip():
        tag_frame.destroy()
    else:
        
        add_tag(tag_name, "")
        tag_frame.destroy()
        print(f"tag '{tag_name}' created")

in_frame = False
    
def tag_window_left_click(event):
    global tag_frame, in_frame, tag_in_progress
    if not in_frame and tag_in_progress is True:
        tag_frame.destroy()

def tag_window_right_click(event):
    global tag_frame, in_frame, tag_in_progress
    if not in_frame and tag_in_progress is True:
        tag_frame.destroy()

def exit_tag_frame(event):
    global tag_frame
    tag_frame.destroy()
   
def inside_frame(event):
    global in_frame
    in_frame = True

def outside_frame(event):
    global in_frame
    in_frame = False

class SelectBox:
    def __init__(self, canvas):
        self.canvas = canvas
        self.left_click_hold = False
        self.rect = None
        self.x_start = None
        self.y_start = None
        self.last_motion_time = 0
        self.throttle_delay = 0.016

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<ButtonRelease-1>", self.left_click_release)
        self.canvas.bind("<Motion>", self.mouse_move)

    def left_click(self, event):
        self.on_left_click_press(event)
    
    def left_click_release(self, event):
        self.on_left_click_release(event)

    def on_left_click_press(self, event):
        self.left_click_hold = True
        self.x_start = event.x
        self.y_start = event.y

        if self.rect is None:
            self.rect = self.canvas.create_rectangle(self.x_start, self.y_start, self.x_start, self.y_start, outline="#27bde7", width=1.5)

    def on_left_click_release(self, event):
        self.left_click_hold = False
        if self.rect:
            self.canvas.coords(self.rect, 0, 0, 0, 0)

    def mouse_move(self, event):
        now = time.time()
        if now - self.last_motion_time < self.throttle_delay:
            return
        self.last_motion_time = now

        if self.left_click_hold and self.rect:
            self.canvas.coords(self.rect, self.x_start, self.y_start, event.x, event.y)
