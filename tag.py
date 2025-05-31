import tkinter as tk
from tkinter import *

#tag create process(Window)

tag_in_progress = False


def create_tag_window(parent):
    global tag_name, tag_frame, tag_entry, tag_in_progress
   
    if tag_in_progress is True:
        tag_frame.destroy()
        tag_in_progress = False

    x = parent.winfo_pointerx() - parent.winfo_rootx()
    y = parent.winfo_pointery() - parent.winfo_rooty()

    tag_frame = tk.Frame(parent, width=320, height=60, borderwidth=2, relief=tk.RIDGE, bg='#171717')
    tag_frame.place(x=x, y=y)  

    label = tk.Label(tag_frame, text="Tag name:", fg="white", bg='#171717')
    label.pack(pady=(5, 0), anchor='c', padx=5)

    tag_entry = tk.Entry(tag_frame, bg="#242323", fg="white", insertbackground="white")
    tag_entry.pack(padx=15, pady=15, fill='x')
    tag_entry.focus_set()

    tag_in_progress = True

    tag_frame.bind("<Enter>", inside_frame)
    tag_frame.bind("<Leave>", outside_frame)

    tag_entry.bind("<Return>", enter_key)
    tag_entry.bind("<Escape>", exit_tag_frame)

global tag_name
tag_name = None

def register_callback(cb):
    global callback
    callback = cb

def enter_key(event):
    global tag_frame, tag_name, tag_entry

    tag_name = tag_entry.get()
    if not tag_entry.get().strip():
        tag_frame.destroy()
    else:
        tag_frame.destroy()
        print(tag_name + ' confirmed in tag.py')
 
    if callback:
        callback()

def get_tag_name():
    return tag_name

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