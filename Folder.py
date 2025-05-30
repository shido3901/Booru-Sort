def get_folder_position(folder_count):
    x = 20 + (folder_count % 10) * 150
    y = 40 + (folder_count // 10) * 150
    return x, y