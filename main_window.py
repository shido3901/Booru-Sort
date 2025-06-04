import tkinter as tk
from folder_area import create_folder_area, folder_area_right_click, SelectBox
from side_panel import side_panel
from tag_panel import tag_panel, tag_search
from tag import TagProperties
from PIL import Image, ImageTk
from load_images import load_images_area, show_pictures_function

main_window = tk.Tk()
main_window.geometry("2560x1440")
main_window.title("Booru Sort Lite")
main_window.config(bg='cyan')

main_window.grid_rowconfigure(0, weight=0)  
main_window.grid_columnconfigure(1, weight=1)

main_window.grid_rowconfigure(1, weight=1)
main_window.grid_rowconfigure(3, weight=1)
main_window.grid_rowconfigure(5, weight=20) 

folder_area = create_folder_area(main_window)
folder_area, canvas = create_folder_area(main_window)

side_panel_area = side_panel(main_window)

tag_panel_area, pinned_panel, tag_panel_recent_label, tag_panel_recent_content, add_tag, tag_entry = tag_panel(main_window)
tag_entry.bind("<KeyRelease>", lambda event: tag_search(event, tag_panel_recent_content))

garbageaf = load_images_area(main_window)

folder_area_box = canvas
folder_area_box.bind("<Button-3>", lambda event: folder_area_right_click(event, canvas)) 

select_box = SelectBox(folder_area_box)

canvas = load_images_area(main_window)
image_path = None
show_pictures_function(image_path, canvas)

tag_properties = TagProperties(tag_panel_recent_content, canvas=canvas)
tag_properties.refresh()



main_window.mainloop()