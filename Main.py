import tkinter as tk
from tkinter import *
from tkinter import ttk
import ctypes

main_window = tk.Tk()
main_window.tk.call('tk', 'scaling', 1.5) 
main_window.geometry("1920x1080")
main_window.title("Booru Sort Lite")
main_window.config(background='#242323')
##ctypes.windll.shcore.SetProcessDpiAwareness(1)


#top left sidebar
sidebar_area = tk.Frame(main_window, width = 320, height = 540, borderwidth = 1, relief = tk.GROOVE)
sidebar_area.pack_propagate(False)
sidebar_area.pack(anchor = 'w', side = 'top')

sidebar_frame = Canvas(sidebar_area)
sidebar_frame.pack(side=LEFT, fill=BOTH, expand=1)

#scrollbar
sidebar_scrollbar = ttk.Scrollbar(sidebar_frame, orient=VERTICAL, command=sidebar_frame.yview)
sidebar_scrollbar.pack(side=RIGHT, fill=Y)

sidebar_frame.configure(yscrollcommand=sidebar_scrollbar.set, background='#171717', highlightthickness=0)

second_frame = Frame(sidebar_frame, background='#171717')
sidebar_frame.create_window((0, 0), window=second_frame, anchor="nw")

sidebar_frame.create_window((0,0), window=second_frame, anchor="nw")
second_frame.bind("<Configure>", lambda e: sidebar_frame.configure(scrollregion=sidebar_frame.bbox("all")))

def _on_mousewheel(event):
    sidebar_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")

sidebar_frame.bind_all("<MouseWheel>", _on_mousewheel)



#top half search
tag_area_bottom2 = tk.Frame(main_window, width = 320, height = 245, borderwidth = 2, relief = tk.RIDGE)
tag_area_bottom2.pack_propagate(False)
tag_area_bottom2.pack(anchor = 'w', side = 'bottom')
tag_area_bottom2.config(background='#171717')
##tag_area_bottom2.config(background='cyan')


#top half
tag_area_bottom = tk.Frame(main_window, width = 320, height = 25, borderwidth = 2, relief = tk.RIDGE)
tag_area_bottom.pack_propagate(False)
tag_area_bottom.pack(anchor = 'w', side = 'bottom')
tag_area_bottom.config(background='#242323')
##tag_area_bottom.config(background='purple')




label = tk.Label(tag_area_bottom, text='Recent tags', bg='#242323', fg='white')
label.pack(side='left', padx=5)


#bottom half search
tag_area_top2 = tk.Frame(main_window, width = 320, height = 245, borderwidth = 2, relief = tk.RIDGE)
tag_area_top2.pack_propagate(False)
tag_area_top2.pack(anchor = 'w', side = 'bottom')
tag_area_top2.config(background='#171717')
##tag_area_top2.config(background='red')

#bottom half
tag_area_top = tk.Frame(main_window, width = 320, height = 25, borderwidth = 2, relief = tk.RIDGE)
tag_area_top.pack_propagate(False)
tag_area_top.pack(anchor = 'w', side = 'bottom')
tag_area_top.config(background='#242323')
##tag_area_top.config(background='green')

label = tk.Label(tag_area_top, text = 'Pinned tags')
label.pack(anchor = 'w', side='top')
label.config(bg='#242323', fg="white")


#add tag
def enter_key(event):
    global tag_frame
    global tag_name

    tag_value = tag_name.get()
    if not tag_name.get().strip():
        tag_frame.destroy()
    else:
        
        tag = Button(tag_area_bottom2, text=tag_value, padx=10, pady=5)
        tag.pack(pady=2, padx=2, anchor='nw')

        tag_frame.destroy()

def create_tag_window():
    global tag_frame
    global tag_name

    x = main_window.winfo_pointerx() - main_window.winfo_rootx()
    y = main_window.winfo_pointery() - main_window.winfo_rooty()

    tag_frame = tk.Frame(main_window, width=320, height=60, borderwidth=2, relief=tk.RIDGE, bg='#171717')
    tag_frame.place(x=x, y=y)  

    label = tk.Label(tag_frame, text="Tag name:", fg="white", bg='#171717')
    label.pack(pady=(5, 0), anchor='c', padx=5)

    tag_name = tk.Entry(tag_frame, bg="#242323", fg="white", insertbackground="white")
    tag_name.pack(padx=15, pady=15, fill='x')
    tag_name.focus_set()

    tag_name.bind("<Return>", enter_key)

##button next to recent tags
button = tk.Button(tag_area_bottom, text='＋', bg='#242323', fg='white', command=create_tag_window)
button.pack(side='right')

    

def showContextMenu(event):
    right_click_menu.tk_popup(event.x_root, event.y_root)

right_click_menu = tk.Menu(main_window, tearoff=0)
right_click_menu.add_command(label = "View", command=create_tag_window)
right_click_menu.add_separator()
right_click_menu.add_command(label = "New", command=create_tag_window)
right_click_menu.add_separator()
right_click_menu.add_command(label = "New tag", command=create_tag_window)

main_window.bind("<Button-3>", showContextMenu)







main_window.mainloop()
