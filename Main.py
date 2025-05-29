import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import time

main_window = tk.Tk()
main_window.tk.call('tk', 'scaling', 1.5) 
main_window.geometry("1920x1080")
main_window.title("Booru Sort Lite")
main_window.config(background='#242323')
##ctypes.windll.shcore.SetProcessDpiAwareness(1)



#folder area (main)
folder_area = tk.Frame(main_window, width = 1600, height = 1080, borderwidth = 1, relief = tk.GROOVE)
folder_area.config(background='#242323')
folder_area.pack(side='right')


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

def on_mousewheel(event):
    sidebar_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")

sidebar_frame.bind_all("<MouseWheel>", on_mousewheel)


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
    tag_name.bind("<Escape>", enter_key)



folder_count = 0
folder_labels = []
isFolder = False

def folderSelect(event):
    global isFolder
    isFolder = True
    print("select folder")

def folder_unselect(event):
    global isFolder
    isFolder = False
    print("unselect")

folder_in_progress = False

#add folder
def create_folder():
    
    global folder_count
    global folder_label
    
    global folder_in_progress

    folder_in_progress = True

    x = 20 + (folder_count % 10) * 150  
    y = 40 + (folder_count // 10) * 150

    folder_image = Image.open("folder.png").convert("RGBA")
    folder_photo = ImageTk.PhotoImage(folder_image)

    folder_wrapper = tk.Frame(folder_area, bg='#242323')
    folder_wrapper.place(x=x, y=y)

    folder_label = tk.Label(folder_wrapper, image=folder_photo, bg='#242323')   
    folder_label.image = folder_photo  
    folder_label.pack()

    folder_label.bind("<Enter>", folderSelect) 
    folder_label.bind("<Leave>", folder_unselect)
    folder_labels.append(folder_label)

    folder_count += 1


    ##name area for folder
    folder_rename = tk.Entry(folder_wrapper, bg="#242323", fg="white", width=10, insertbackground="white")
    folder_rename.insert(0, 'New Folder')
    folder_rename.pack()
    folder_rename.focus_set()

    global folder_rename_enter
    def folder_rename_enter(event):
        global folder_in_progress
        folder_name_final = folder_rename.get()

        ##check if folder name is empty
        if not folder_rename.get():
            folder_name_final = 'New Folder'
        folder_new_name = tk.Label(folder_wrapper, text=folder_name_final, fg="white", bg='#242323')
        folder_new_name.pack()
        folder_rename.bind("<Key>", folder_key_press)

        folder_rename.destroy()
        folder_in_progress = False

        print('folder created')
        

    folder_rename.bind("<Return>", folder_rename_enter)
    folder_rename.bind("<Escape>", folder_rename_enter)
    
    
    def folder_key_press(event):
        current_text = folder_rename.get()
        new_text = current_text.replace("New Folder", "")
        folder_rename.delete(0, END)
        folder_rename.insert(0, new_text)

    folder_rename.bind("<Key>", folder_key_press)
    


##button next to recent tags
button = tk.Button(tag_area_bottom, text='＋', bg='#242323', fg='white', command=create_tag_window)
button.pack(side='right')


def show_context_menu(event):

    if isFolder == False:
        right_click_menu.tk_popup(event.x_root, event.y_root)
    else:
        folder_right_click.tk_popup(event.x_root, event.y_root)
    right_click_menu.grab_release()
    folder_right_click.grab_release()

#right click when folder select
right_click_menu = tk.Menu(main_window, tearoff=0)
right_click_menu.add_command(label="View", command=create_tag_window)
right_click_menu.add_separator()
right_click_menu.add_command(label="New Folder", command=create_folder)
right_click_menu.add_separator()
right_click_menu.add_command(label="New tag", command=create_tag_window)

folder_right_click = tk.Menu(main_window, tearoff=0)
folder_right_click.add_command(label="View", command=create_tag_window)
folder_right_click.add_separator()
folder_right_click.add_command(label="Delete Folder", command=create_tag_window)
folder_right_click.add_separator()
folder_right_click.add_command(label="New tag", command=create_tag_window)

def on_right_click(event):
    if folder_in_progress:
        folder_rename_enter(event)
    else:
        show_context_menu(event)


def on_left_click(event):
    if folder_in_progress:
        folder_rename_enter(event)
    else:
        on_left_button_press(event)


##cursor hold click functionality
x_start = None  
y_start = None  
rect = None

canvas = tk.Canvas(folder_area, width=1600, height=1080, bg=folder_area['bg'], highlightthickness=0)
canvas.place(x=0, y=0)

left_click_hold = False  

def on_left_button_press(event):
    global left_click_hold
    global x_start
    global y_start
    global rect
    left_click_hold = True  
    print("left click", left_click_hold)
    ##print(f"Starting coords: ({event.x}, {event.y})") 
    x_start = event.x
    y_start = event.y

    if rect is None:
        rect = canvas.create_rectangle(x_start, y_start, x_start, y_start, outline="#4287f5", width=2.5)


def on_left_button_release(event):
    global left_click_hold
    left_click_hold = False 
    print("release True")
    canvas.coords(rect, 0,0,0,0)


last_motion_time = 0
throttle_delay = 0.033


def on_mouse_move(event):

    global last_motion_time
    now = time.time()
    if now - last_motion_time < throttle_delay:
        return 
    last_motion_time = now

    global x_start
    global y_start
    global rect
    if left_click_hold and rect:
        ##print(f"Dragging at: ({event.x}, {event.y})")
        canvas.coords(rect, x_start, y_start, event.x, event.y)

        

main_window.bind("<Button-1>", on_left_click)  
main_window.bind("<ButtonRelease-1>", on_left_button_release)
main_window.bind("<Motion>", on_mouse_move)


main_window.bind("<Button-3>", on_right_click)
main_window.bind("<Button-1>", on_left_click)


main_window.mainloop()
