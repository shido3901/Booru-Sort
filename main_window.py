import tkinter as tk
from folder_area import create_folder_area, show_context_menu, SelectBox
from side_panel import create_sidepanel_area
from tag_panel import create_tag_panel

main_window = tk.Tk()
main_window.geometry("1920x1080")
main_window.title("Booru Sort Lite")
main_window.config(bg='cyan')

main_window.grid_rowconfigure(0, weight=1)  
main_window.grid_columnconfigure(1, weight=1)

main_window.grid_rowconfigure(1, weight=25)
main_window.grid_rowconfigure(3, weight=15)
main_window.grid_rowconfigure(5, weight=15)  

folder_area = create_folder_area(main_window)

side_panel = create_sidepanel_area(main_window)

tag_panel = create_tag_panel(main_window)

#select box
canvas = tk.Canvas(folder_area, bg=folder_area['bg'], highlightthickness=0.5)
canvas.grid(row=0, column=0, sticky="nsew")

select_box = SelectBox(canvas)

canvas.bind("<Button-3>", show_context_menu)



main_window.mainloop()
