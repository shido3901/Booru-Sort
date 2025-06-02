import tkinter as tk
from folder_area import create_folder_area, folder_area_right_click, SelectBox
from side_panel import side_panel
from tag_panel import tag_panel
from tag import load_tag_buttons

main_window = tk.Tk()
main_window.geometry("1920x1080")
main_window.title("Booru Sort Lite")
main_window.config(bg='cyan')

main_window.grid_rowconfigure(0, weight=0)  
main_window.grid_columnconfigure(1, weight=1)

main_window.grid_rowconfigure(1, weight=1)
main_window.grid_rowconfigure(3, weight=1)
main_window.grid_rowconfigure(5, weight=20) 

folder_area = create_folder_area(main_window)

side_panel_area = side_panel(main_window)

tag_panel_area, pinned_panel, tag_panel_recent_label, tag_panel_recent_content, add_tag = tag_panel(main_window)

folder_area.bind("<Button-3>", folder_area_right_click)

folder_area_box = tk.Canvas(folder_area, bg=folder_area['bg'], highlightthickness=0.5)
folder_area_box.grid(row=0, column=0, sticky="nsew")
folder_area_box.bind("<Button-3>", folder_area_right_click)

select_box = SelectBox(folder_area_box)

load_tag_buttons(tag_panel_recent_content)

main_window.mainloop()