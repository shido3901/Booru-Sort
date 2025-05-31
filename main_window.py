import tkinter as tk
import tag
from folder_area import SelectBox, create_folder_area, folder_area_right_click
from side_panel import create_sidepanel_area
from tag_panel import create_tag_panel
from tag import tag_window_left_click, tag_window_right_click
import tag

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

side_panel = create_sidepanel_area(main_window)

tag_panel_pinned, pinned_panel, tag_panel_recent_label, tag_panel_recent_content = create_tag_panel(main_window)

#select box
folder_area = tk.Canvas(folder_area, bg=folder_area['bg'], highlightthickness=0.5)
folder_area.grid(row=0, column=0, sticky="nsew")
select_box = SelectBox(folder_area)

#left click
main_window.bind("<Button-1>", tag_window_left_click)

#right click
folder_area.bind("<Button-3>", folder_area_right_click)
main_window.bind("<Button-3>", tag_window_right_click)

current_column = 0
current_row = 0  
max_columns = 4  

def my_main_function():
    global tag_name
    tag_name = tag.get_tag_name()

    if tag_name.strip():
        add_tag()
        print(tag_name + ' successfully created in main_window')


def add_tag():
    global current_column, current_row, add_tag, tag_name

    if current_column >= max_columns:
        current_column = 0
        current_row += 1  

    tag = tk.Button(tag_panel_recent_content, text=tag_name, padx=5, pady=5)
    
    tag.grid(row=current_row, column=current_column, pady=5, padx=5)

    current_column += 1  

tag.register_callback(my_main_function)

main_window.mainloop()


   
        