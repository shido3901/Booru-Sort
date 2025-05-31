import tkinter as tk

def create_tag_panel(parent):
    tag_panel_pinned = tk.Frame(parent, bg="#242323", width=320, height=25, borderwidth=2, relief=tk.RIDGE)
    tag_panel_pinned.grid(row=2, column=0, sticky="nsew")

    pinned_panel = tk.Frame(parent, bg="#171717", width=320, height=245, borderwidth=2, relief=tk.RIDGE)
    pinned_panel.grid(row=3, column=0, sticky="nsew")

    tag_panel_recent_label = tk.Frame(parent, bg="#242323", width=320, height=25, borderwidth=2, relief=tk.RIDGE)
    tag_panel_recent_label.grid(row=4, column=0, sticky="nsew")  

    tag_panel_recent_content = tk.Frame(parent, bg="#171717", width=320, height=245, borderwidth=2, relief=tk.RIDGE)
    tag_panel_recent_content.grid(row=5, column=0, sticky="nsew")

    


    return tag_panel_pinned, pinned_panel, tag_panel_recent_label, tag_panel_recent_content




    

