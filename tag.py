import tkinter as tk
from tkinter import *
from tkinter import messagebox


def tag_properties(tag):
   tag.bind("<Button-3>", right_click_menu)
   print('test')

def right_click_menu(event):
    tag_name = event.widget.cget("text") #confirmation incase something breaks lol
    print("Right-clicked on tag: " + tag_name)
    
    tag_menu = tk.Menu(event.widget, tearoff=0, bg="#333333", fg="white", activebackground="#555555", activeforeground="cyan", font=("Arial", 10))
   
    #aAdd commands as needed
    tag_menu.add_command(label="Rename", command=lambda: print('ok'))
    tag_menu.add_command(label="Delete", command=lambda: confirm_delete_box(event.widget, f"Delete tag: '{tag_name}'?", lambda: print(f"{tag_name} deleted")))



    tag_menu.config(bg="#171717", bd=0, relief="flat")
    tag_menu.tk_popup(event.x_root, event.y_root)

def confirm_delete_box(parent, message, on_confirm):
    confirm_box = tk.Toplevel(parent)
    confirm_box.configure(bg="#1e1e1e")
    confirm_box.resizable(False, False)

    width = 250
    height = 120

    widget_x = parent.winfo_rootx()
    widget_y = parent.winfo_rooty()

    x = widget_x
    offset = 50  
    y = widget_y - height - offset if widget_y - height - offset > 0 else widget_y + 40 

    confirm_box.geometry(f"{width}x{height}+{x}+{y}")
    confirm_box.focus_set()
    confirm_box.grab_set()
    confirm_box.transient(parent)

    tk.Label(confirm_box, text=message, bg="#1e1e1e", fg="white", font=("Arial", 10)).pack(pady=20)

    button_frame = tk.Frame(confirm_box, bg="#1e1e1e")
    button_frame.pack(pady=10)

    def confirm():
        on_confirm()
        confirm_box.destroy()

    def cancel():
        confirm_box.destroy()

    tk.Button(button_frame, text="Yes", command=confirm, bg="#444", fg="white", width=10).pack(side="left", padx=10)
    tk.Button(button_frame, text="No", command=cancel, bg="#444", fg="white", width=10).pack(side="right", padx=10)

"""def rename(parent):
    global tag_name, tag_frame, tag_entry, tag_in_progress

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
    tag_entry.bind("<Escape>", exit_tag_frame)"""
    
    
    
  

  


#tag create process(Window popup)
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

#tag properties

