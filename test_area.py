import tkinter as tk
from tkinter import filedialog

def open_file_explorer():
   
    file_paths = filedialog.askopenfilenames(title="Add to:", filetypes=[
        ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
        ("Video Files", "*.mp4;*.mov;*.avi")
    ])
    
    
    if file_paths:
        result = "\n".join(file_paths)
        print(f"Selected files:\n{result}")
        entry_box.delete(0, tk.END)  
        entry_box.insert(0, result.split("\n")[0])  
    else:
        print("No file selected")


root = tk.Tk()
root.title("File Explorer Example")
root.geometry("400x250")

tag_list = {}

open_button = tk.Button(root, text="Click to Open File Explorer", command=open_file_explorer)
open_button.pack(pady=20)

def add_tag(event=None):
    tag_name = entry_box.get() 
    tag_list[tag_name] = []
    print(f"Tag '{tag_name}' added!")

entry_box = tk.Entry(root, width=50)
entry_box.pack(pady=10)
entry_box.bind("<Return>", add_tag)



root.mainloop()