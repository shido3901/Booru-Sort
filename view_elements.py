# view_elements.py
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QPushButton
from PyQt5.QtCore import Qt

class ImageManager:
    def __init__(self, image_area):
        self.image_size = 2
        self.image_area = image_area

        self.image_cell_width = 0
        self.image_cell_height = 0

        self.cell_size_width = 180
        self.cell_size_height = 220
     


        self.num_cols = self.image_area.width() // self.cell_size_width
        self.num_rows = self.image_area.height() // self.cell_size_height

        self.max_column = 6
        self.row = 2

        self.starting_count = 0
        
        self.current_page = 1
        self.page_count = 0
        
        self.amount_on_current_page = 0
        self.total_on_screen = 0 #images + blank frames

        self.entity_count = 456

        self.image_size_selection = 2


        
    def set_image_size(self, image_area_layout):

        if self.image_size_selection == 1:
            
            self.image_cell_width = 300
            self.image_cell_height = 375

            self.cell_size_width = 315
            self.cell_size_height = 390


            self.image_size_selection = 2
        elif self.image_size_selection == 2:


            self.image_cell_width = 375
            self.image_cell_height = 500

            self.cell_size_width = 390
            self.cell_size_height = 515


            self.image_size_selection = 3
        elif self.image_size_selection == 3:
            


            self.image_cell_width = 225
            self.image_cell_height = 300

            self.cell_size_width = 240
            self.cell_size_height = 315

            self.image_size_selection = 1

        print(self.image_size_selection)
        
        self.num_cols = self.image_area.width() // self.cell_size_width
        self.num_rows = self.image_area.height() // self.cell_size_height

        self.refresh_image_area(image_area_layout)


    def refresh_image_area(self, image_area_layout):
        self.max_column = self.num_cols
        max_row = self.num_rows
        self.total_on_screen = self.max_column * max_row

        # clear layout
        while image_area_layout.count():
            child = image_area_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.current_page = (self.starting_count // self.total_on_screen) + 1 if self.total_on_screen > 0 else 1
        self.page_count = (self.entity_count + self.total_on_screen - 1) // self.total_on_screen if self.total_on_screen else 1  

        self.page_count_text.setText(f"Page {self.current_page} of {self.page_count}, {self.entity_count} items")

        self.add_image_to_area(image_area_layout)
    
    def set_page_count_text(self, text):
        self.page_count_text = text



    def add_image_to_area(self, layout):
        row = 0
        col = 0
        self.amount_on_current_page = 0

        for i in range(self.starting_count, self.starting_count + self.total_on_screen):
            if i < self.entity_count:
                label = QLabel(f"{i + 1}")
                label.setStyleSheet("color: white; font-size: 50px; background-color: black;")
                self.amount_on_current_page += 1
            else:
                label = QLabel()
                label.setStyleSheet("background-color: #454545;")

    
            label.setMaximumHeight(self.image_cell_height)
            label.setMaximumWidth(self.image_cell_width)
            label.setAlignment(Qt.AlignCenter)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            layout.addWidget(label, row, col)
            col += 1
            if col == self.max_column:
                col = 0
                row += 1





    def next_page(self):
        if self.starting_count + self.amount_on_current_page != self.entity_count:
            self.starting_count = self.amount_on_current_page + self.starting_count
            #print(self.starting_count)
            self.refresh_image_area(self.image_area.layout())

    def previous_page(self):
            self.starting_count -= self.total_on_screen
            if self.starting_count < 0:
                self.starting_count = 0 
              
            #print(self.total_on_screen)
            self.refresh_image_area(self.image_area.layout())
            


    def resizeEvent(self, event):
  
        latest_num_cols = self.image_area.width() // self.cell_size_width
        if latest_num_cols != self.num_cols:
            self.num_cols = latest_num_cols

        latest_num_rows = self.image_area.height() // self.cell_size_height 
        if latest_num_rows != self.num_rows:
            self.num_rows = latest_num_rows

        self.refresh_image_area(self.image_area.layout())



     



    




def change_size(self):
        latest_num_cols = self.image_area.width() // self.image_manager.image_cell_width
        latest_num_rows = self.image_area.height() // self.image_manager.image_cell_height
        self.image_manager.set_image_size(self.image_area_layout, latest_num_cols, latest_num_rows)

"""def eventFilter(self, source, event):
        if source == self.image_area and event.type() == QEvent.Wheel:
            delta = event.angleDelta().y()
            if delta > 0:
                self.previous_page_click()
            else:
                self.next_page_click()
            return True
        return super().eventFilter(source, event)"""
