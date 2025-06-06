import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QEvent

from tag import add_tag_to_grid
from view_elements import ImageManager  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Booru Sort Lite")
        self.setGeometry(700, 300, 1920, 1200)
        self.setStyleSheet("background-color: black;")

        self.image_manager = ImageManager()

        self.initUI()

        self.num_cols = self.image_area.width() // self.image_manager.image_cell_width
        self.num_rows = self.image_area.height() // self.image_manager.image_cell_height

        self.image_manager.refresh_image_area(self.image_area_layout, self.num_cols, self.num_rows)

    def initUI(self):
        main_window = QWidget()
        self.setCentralWidget(main_window)

        self.tag_list_panel = QWidget(main_window)
        self.tag_list_panel.setMinimumWidth(320)
        self.tag_list_panel.setMaximumWidth(520)
        self.tag_list_panel.setStyleSheet("background-color: #454545;")
        self.tag_list_layout = QGridLayout()
        self.tag_list_panel.setLayout(self.tag_list_layout)

        self.image_area = QWidget(main_window)
        self.image_area.setMinimumWidth(300)
        self.image_area.setMinimumHeight(500)
        self.image_area.setStyleSheet("background-color: #454545;")

        self.search_bar = QWidget(main_window)
        self.search_bar.setMinimumWidth(200)
        self.search_bar.setMinimumHeight(80)
        self.search_bar.setMaximumHeight(80)
        self.search_bar.setStyleSheet("background-color: #454545;")

        text_box = QLineEdit(self.search_bar)
        text_box.setPlaceholderText("Search Example: black_cat")
        text_box.setFixedHeight(70)
        text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        text_box.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                border: 3px;
                padding: 5px;
            }
        """)

        self.options_bar = QWidget(main_window)
        self.options_bar.setMinimumWidth(180)
        self.options_bar.setMinimumHeight(50)
        self.options_bar.setMaximumHeight(50)
        self.options_bar.setStyleSheet("background-color: #454545;")
        options_layout = QVBoxLayout(self.options_bar)
        options_layout.setContentsMargins(0, 0, 0, 0)

        search_layout = QHBoxLayout(self.search_bar)
        search_layout.setContentsMargins(5, 0, 0, 0)
        search_layout.setSpacing(5)
        search_layout.addWidget(text_box)

        tag_button = QPushButton("change size", self.options_bar)
        tag_button.setStyleSheet("color: white; background-color: #606060; border: none;")
        tag_button.clicked.connect(self.change_size)
        tag_button.setFixedSize(120, 40)
        options_layout.addWidget(tag_button, alignment=Qt.AlignCenter)

        self.bottom_bar = QWidget(main_window)
        self.bottom_bar.setMinimumHeight(50)
        self.bottom_bar.setMaximumHeight(50)
        self.bottom_bar.setStyleSheet("background-color: #454545;")
        self.bottom_bar.setContentsMargins(0, 0, 0, 0)

        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.setContentsMargins(10, 0, 10, 0)
        bottom_bar_layout.setSpacing(20)
        self.bottom_bar.setLayout(bottom_bar_layout)

        previous_page_click = QPushButton("Previous Page", self.bottom_bar)
        previous_page_click.setStyleSheet("color: white; background-color: #606060; border: none;")
        previous_page_click.setFixedSize(120, 40)
        previous_page_click.clicked.connect(self.previous_page_click)

        self.page_count = QLabel("", self.bottom_bar)
        self.page_count.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.page_count.setAlignment(Qt.AlignCenter)

        next_page_click = QPushButton("Next Page", self.bottom_bar)
        next_page_click.setStyleSheet("color: white; background-color: #606060; border: none;")
        next_page_click.setFixedSize(120, 40)
        next_page_click.clicked.connect(self.next_page_click)

        bottom_bar_layout.addWidget(previous_page_click, alignment=Qt.AlignLeft)
        bottom_bar_layout.addWidget(self.page_count, alignment=Qt.AlignCenter)
        bottom_bar_layout.addWidget(next_page_click, alignment=Qt.AlignRight)

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

        self.image_area.installEventFilter(self)
        add_tag_to_grid(self.tag_list_layout)

    def resizeEvent(self, event):
        latest_num_cols = self.image_area.width() // self.image_manager.image_cell_width
        latest_num_rows = self.image_area.height() // self.image_manager.image_cell_height

        if latest_num_cols != self.num_cols or latest_num_rows != self.num_rows:
            self.num_cols = latest_num_cols
            self.num_rows = latest_num_rows
            self.image_manager.refresh_image_area(self.image_area_layout, self.num_cols, self.num_rows)

        event.accept()

    def change_size(self):
        latest_num_cols = self.image_area.width() // self.image_manager.image_cell_width
        latest_num_rows = self.image_area.height() // self.image_manager.image_cell_height
        self.image_manager.set_image_size(self.image_area_layout, latest_num_cols, latest_num_rows)

    def next_page_click(self):
        latest_num_cols = self.image_area.width() // self.image_manager.image_cell_width
        latest_num_rows = self.image_area.height() // self.image_manager.image_cell_height
        self.image_manager.next_page(self.image_area_layout, latest_num_cols, latest_num_rows)

    def previous_page_click(self):
        latest_num_cols = self.image_area.width() // self.image_manager.image_cell_width
        latest_num_rows = self.image_area.height() // self.image_manager.image_cell_height
        self.image_manager.previous_page(self.image_area_layout, latest_num_cols, latest_num_rows)

    def eventFilter(self, source, event):
        if source == self.image_area and event.type() == QEvent.Wheel:
            delta = event.angleDelta().y()
            if delta > 0:
                self.previous_page_click()
            else:
                self.next_page_click()
            return True
        return super().eventFilter(source, event)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
