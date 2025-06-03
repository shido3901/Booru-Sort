import tkinter as tk
from tag import TagProperties, load_tag_info
from shared_state import column_count, row_count


def tag_panel(parent):
    global tag_panel_recent_content
    global tag_search_key

    tag_panel_pinned = tk.Frame(parent, bg="#242323", width=380, height=25, borderwidth=2, relief=tk.RIDGE)
    tag_panel_pinned.grid(row=2, column=0, sticky="nsew")

    pinned_panel = tk.Frame(parent, bg="#171717", width=80, height=245, borderwidth=2, relief=tk.RIDGE)
    pinned_panel.grid(row=3, column=0, sticky="nsew")

    tag_panel_recent_label = tk.Frame(parent, bg="#242323", width=380, height=25, borderwidth=2, relief=tk.RIDGE)
    tag_panel_recent_label.grid(row=4, column=0, sticky="nsew")  

    tag_search_key = tk.Entry(tag_panel_recent_label, bg="#242323", fg="white", insertbackground="white")
    tag_search_key.pack(fill='x', side="left")

    add_tag = tk.Button(tag_panel_recent_label, text="＋", bg="#444", fg="white", font=("Arial", 13), width=2, command=lambda: open_window())
    add_tag.pack(side="right")

    tag_panel_recent_content = tk.Frame(parent, bg="#171717", width=380, height=245, borderwidth=2, relief=tk.RIDGE)
    tag_panel_recent_content.grid(row=5, column=0, sticky="nsew")

    return tag_panel_pinned, pinned_panel, tag_panel_recent_label, tag_panel_recent_content, add_tag, tag_search_key

def open_window():
    tag_box = tk.Toplevel()
    tag_box.title("Booru Sort Lite")
    tag_box.configure(bg='#171717')
    width = 600
    height = 410
    x = 300
    y = 600

    tag_box.geometry(f"{width}x{height}+{x}+{y}")
    tag_box.focus_set()

    label = tk.Label(tag_box, text="enter tags, separated by space:", fg="white", bg='#171717', font=("Arial", 11))
    label.pack(pady=(10, 0), padx=10, anchor='c')
    
    text_box = tk.Text(tag_box, bg="#242323", fg="white", insertbackground="white", wrap='word', height=3, font=("Arial", 14))
    text_box.pack(padx=15, pady=10, fill='both', expand=True)
    text_box.focus_set()

    def insert_underscore(event):
        current_text = text_box.get("1.0", "end-1c")  

        if current_text and current_text[-1] == " ":
           
            text_box.delete("1.0", "end-1c")  
            text_box.insert("1.0", current_text[:-1] + "_")  
            return "break"  

        return None

    text_box.bind("<space>", insert_underscore)
    text_box.bind("<Return>", lambda: submit_text)
   
    def submit_text():

        tag_list_add = text_box.get("1.0", tk.END).strip()

        if not tag_list_add:
            return

        tag_name_split = tag_list_add.split(' ')
    
        for tag_name in tag_name_split:
    
            tag_instance = TagProperties(tag_panel_recent_content, tag_name)
            tag_instance.add_tag()
            
            print(f"tag '{tag_name}' added.")
 
        tag_box.destroy()

    create_button = tk.Button(tag_box, text="create", command=submit_text, bg="#444", fg="white")
    create_button.pack(pady=10)

    text_box.bind("<Return>", submit_text)


def tag_search(event, tag_panel_recent_content):
    

    search_text = tag_search_key.get()
    data = load_tag_info()

    for widget in tag_panel_recent_content.winfo_children():
        widget.destroy()

    import shared_state
    shared_state.column_count = 0
    shared_state.row_count = 0

    for tag_name in data:
        if search_text in tag_name:
            tag_instance = TagProperties(
                tag_panel_recent_content=tag_panel_recent_content,
                tag_name=tag_name
            )
            tag_instance.create_tag_button()
