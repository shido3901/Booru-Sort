from PyQt5.QtWidgets import QLabel

def add_tag_to_grid(tag_list_layout):
    row = 0  # Start at column 0
    
    for i in range(10):
        add_tag_to_list = QLabel(f"test")  
        add_tag_to_list.setStyleSheet("color: white; font-size: 18px;")
        tag_list_layout.addWidget(add_tag_to_list, row, 0)
        
        row += 1  


