import tkinter as tk
from PIL import Image, ImageTk 


def load_images_area(parent):
    folder_area = tk.Frame(parent, bg="#242323", width=2200, height=1500)
    folder_area.grid(row=0, column=1, rowspan=6, sticky="nsew")

    canvas = tk.Canvas(folder_area, bg="#242323", width=2200, height=1500)
    canvas.grid(row=0, column=1, sticky="nsew")

    return canvas


column_count_image = 0
row_count_image = 0


def show_pictures_function(file_path_name, canvas):
    image_load_name = file_path_name

    print(f'{image_load_name}')

    load_image_on_canvas(image_load_name, canvas)

    return image_load_name 

def load_image_on_canvas(image_load_name, canvas):
    global column_count_image, row_count_image 

    try:

        pil_image = Image.open(image_load_name)
        thumbnail_size = (300, 300)
        pil_image.thumbnail(thumbnail_size, Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(pil_image)

        # Calculate pixel position
        x = column_count_image * 310  # Add some spacing
        y = row_count_image * 310

        canvas.create_image(x, y, image=tk_image, anchor="nw")
        if not hasattr(canvas, "images"):
            canvas.images = []
        canvas.images.append(tk_image)  # Keep reference

        column_count_image += 1
        if column_count_image > 9:
            column_count_image = 0
            row_count_image += 1

    except Exception as e:
        print(f"Error loading image: {e}")
