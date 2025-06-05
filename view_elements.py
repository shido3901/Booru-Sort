from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import Qt

max_column = 6
row = 2
entity_count = 26
total_on_screen = 32
image_size = 2

def set_image_size(image_area_layout, latest_num_cols, latest_num_rows):
     
        global max_column, total_on_screen, image_size

        max_column = latest_num_cols
        max_row = latest_num_rows

        if image_size == 1:
            #print('2')
            image_size = 2

        elif image_size == 2:
            image_size = 3
            #print('3')

        elif image_size == 3:
            image_size = 1
            #print('1')

        
        
        refresh_image_area(image_area_layout, latest_num_cols, latest_num_rows)

def refresh_image_area(image_area_layout, latest_num_cols, latest_num_rows):
    global max_column, total_on_screen, image_size

    max_column = latest_num_cols
    max_row = latest_num_rows

    while image_area_layout.count():
            child = image_area_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    total_on_screen = max_row * max_column
    

    add_image_to_area(image_area_layout)


def add_image_to_area(elements_area):
    global row, current_column, entity_count, total_on_screen, max_column
    row = 0
    current_column = 0

    for i in range(total_on_screen):
 
        
        if i <= entity_count - 1:
            add_element_to_area = QLabel(f"{i + 1} ") 
            add_element_to_area.setStyleSheet("color: white; font-size: 50px;"
                                            "background-color: black;")

        else:
            add_element_to_area = QLabel()
            add_element_to_area.setStyleSheet("background-color: #454545;")
                
        

        if image_size == 1:
            add_element_to_area.setMaximumHeight(180)
            add_element_to_area.setMaximumWidth(100)

        elif image_size == 2:
            add_element_to_area.setMaximumHeight(360)
            add_element_to_area.setMaximumWidth(200)

        elif image_size == 3:
            add_element_to_area.setMaximumHeight(500)
            add_element_to_area.setMaximumWidth(275)




        add_element_to_area.setAlignment(Qt.AlignCenter)
        add_element_to_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        elements_area.addWidget(add_element_to_area, row, current_column)

        current_column += 1
        
        if current_column == max_column:
            row += 1
            current_column = 0




