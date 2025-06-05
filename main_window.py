import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget,
                            QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from tag import add_tag_to_grid
from view_elements import  add_image_to_area, refresh_image_area, set_image_size

image_cell_width = 250
image_cell_height = 420
image_size = 2


class MainWindow(QMainWindow):
    global image_cell_width, image_cell_height

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Booru Sort Lite")
        self.setGeometry(700,300,1920,1080)
        self.setStyleSheet("background-color: black;") 
        self.initUI()
        self.num_cols = self.image_area.width() // image_cell_width
        self.num_rows = self.image_area.height() // image_cell_height


    def initUI(self):
        main_window = QWidget()
        self.setCentralWidget(main_window)

        self.tag_list_panel = QWidget(main_window)
        self.tag_list_panel.setMinimumWidth(270) 
        self.tag_list_panel.setMaximumWidth(450)
        self.tag_list_panel.setStyleSheet("background-color: #454545;")


        

        self.tag_list_layout = QGridLayout()
    
        self.tag_list_panel.setLayout(self.tag_list_layout)

        self.image_area = QWidget(main_window)
        self.image_area.setMinimumWidth(300)
        self.image_area.setMinimumHeight(500)
        self.image_area.setStyleSheet("background-color: #454545;")

        self.search_bar = QWidget(main_window)
        self.search_bar.setMinimumWidth(200)
        self.search_bar.setMinimumHeight(50)
        self.search_bar.setMaximumHeight(50)
        self.search_bar.setStyleSheet("background-color: #454545;")
        
        self.options_bar = QWidget(main_window)
        self.options_bar.setMinimumWidth(180)
        self.options_bar.setMinimumHeight(50)
        self.options_bar.setMaximumHeight(50)
        self.options_bar.setStyleSheet("background-color: #454545;")

        options_layout = QVBoxLayout(self.options_bar)
        options_layout.setContentsMargins(0, 0, 0, 0)

        tag_button = QPushButton("change size", self.options_bar)
        tag_button.setStyleSheet("color: white; background-color: #606060; border: none;")
        tag_button.clicked.connect(self.change_size)
        options_layout.addWidget(tag_button, alignment=Qt.AlignCenter)
        tag_button.setFixedSize(120, 40)

        
    
        self.bottom_bar = QWidget(main_window)
        self.bottom_bar.setMinimumWidth(100)
        self.bottom_bar.setMinimumHeight(50)
        self.bottom_bar.setMaximumHeight(50)
        self.bottom_bar.setStyleSheet("background-color: #454545;")

        self.image_area_layout = QGridLayout()
        self.image_area.setLayout(self.image_area_layout)

      
        grid = QGridLayout()

        grid.addWidget(self.tag_list_panel, 0, 0, 5, 1)
   
        grid.addWidget(self.image_area, 1, 1, 2, 2)
        grid.addWidget(self.search_bar, 0, 1)
        grid.addWidget(self.options_bar, 0, 2)
        grid.addWidget(self.bottom_bar, 3, 1, 2, 2)

        grid.setColumnStretch(0, 0)  
        grid.setColumnStretch(1, 1)  

        grid.setRowStretch(0, 1)  
        grid.setRowStretch(1, 1)    
        grid.setSpacing(5)   
        grid.setContentsMargins(6, 6, 6, 6)
       
        main_window.setLayout(grid)

        add_tag_to_grid(self.tag_list_layout)
        add_image_to_area(self.image_area_layout)

       

    def resizeEvent(self, event):
        global latest_num_cols, latest_num_rows
        latest_num_cols = self.image_area.width() // image_cell_width
        latest_num_rows = self.image_area.height() // image_cell_height

        if latest_num_cols != self.num_cols or latest_num_rows != self.num_rows:
            self.num_cols = latest_num_cols
            self.num_rows = latest_num_rows
     
            
            refresh_image_area(self.image_area_layout, latest_num_cols, latest_num_rows)

        event.accept()

    def change_size(self):
        global image_size,  image_cell_height, image_cell_width, latest_num_cols, latest_num_rows

        if image_size == 1:
            image_cell_width = 250
            image_cell_height = 360
           
            image_size = 2

        elif image_size == 2:
            image_cell_width = 360
            image_cell_height = 430
            image_size = 3
            

        elif image_size == 3:
            image_cell_width = 130
            image_cell_height = 180
            image_size = 1
            

        latest_num_cols = self.image_area.width() // image_cell_width
        latest_num_rows = self.image_area.height() // image_cell_height

        if latest_num_cols != self.num_cols or latest_num_rows != self.num_rows:
            self.num_cols = latest_num_cols
            self.num_rows = latest_num_rows



        set_image_size(self.image_area_layout, self.num_cols, self.num_rows)


  







def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()