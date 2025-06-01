import tkinter as tk

def side_panel(parent):
    side_panel = tk.Frame(parent, bg="#171717", width=320, height=540, borderwidth = 2, relief = tk.RIDGE)
    side_panel.grid(row=1, column=0, sticky="nsew")

    return side_panel