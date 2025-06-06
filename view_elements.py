# view_elements.py
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import Qt

class ImageManager:
    def __init__(self):
        self.image_size = 2
        self.image_cell_width = 250
        self.image_cell_height = 420

        self.max_column = 6
        self.row = 2
        self.entity_count = 2345
        self.starting_count = 0
        self.total_on_screen = 0
        self.page_count = 0
        self.current_page = 0
        self.amount_on_current_page = 0
        self.temporary_page_count_save = 0
        self.fit_all = True

    def update_cell_size(self):
        size_map = {
            1: (130, 180),
            2: (250, 360),
            3: (360, 430)
        }
        self.image_cell_width, self.image_cell_height = size_map[self.image_size]

    def set_image_size(self, image_area_layout, latest_num_cols, latest_num_rows):
        self.image_size = {1: 2, 2: 3, 3: 1}[self.image_size]
        self.update_cell_size()
        self.refresh_image_area(image_area_layout, latest_num_cols, latest_num_rows)


    def refresh_image_area(self, image_area_layout, latest_num_cols, latest_num_rows):
        self.max_column = latest_num_cols
        max_row = latest_num_rows
        self.total_on_screen = self.max_column * max_row

        # Clear layout
        while image_area_layout.count():
            child = image_area_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.total_on_screen >= self.entity_count and self.fit_all:
            self.temporary_page_count_save = self.starting_count
            self.fit_all = False
            self.starting_count = 0
        elif not self.fit_all:
            self.starting_count = self.temporary_page_count_save
            self.fit_all = True

        self._add_image_to_area(image_area_layout)

    def _add_image_to_area(self, layout):
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

            size_map = {
                1: (180, 100),
                2: (360, 200),
                3: (500, 275)
            }

            height, width = size_map[self.image_size]
            label.setMaximumHeight(height)
            label.setMaximumWidth(width)
            label.setAlignment(Qt.AlignCenter)
            label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

            layout.addWidget(label, row, col)
            col += 1
            if col == self.max_column:
                col = 0
                row += 1

        self.current_page = (self.starting_count // self.total_on_screen) + 1 if self.total_on_screen > 0 else 1
        self.page_count = (self.entity_count + self.total_on_screen - 1) // self.total_on_screen if self.total_on_screen else 1

    def next_page(self, layout, latest_num_cols, latest_num_rows):
        if self.starting_count < self.entity_count - self.total_on_screen:
            self.starting_count += self.total_on_screen
            self.refresh_image_area(layout, latest_num_cols, latest_num_rows)

    def previous_page(self, layout, latest_num_cols, latest_num_rows):
        self.starting_count -= self.total_on_screen
        if self.starting_count < 0:
            self.starting_count = 0
        self.refresh_image_area(layout, latest_num_cols, latest_num_rows)
