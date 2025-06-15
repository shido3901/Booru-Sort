import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget, QLineEdit, QSizePolicy, QScrollArea,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtCore import Qt, QTimer, QPoint
from profiles import ProfileManager
from taglist import TagList, TagWindow
from PyQt5.QtGui import QCursor
from theme import Theme
from import_entities import ImportEntities

import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Booru Sort Lite")
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #010c1c;")

        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        self.theme = Theme(theme=1)
     
        self.initUI()
    
    def initUI(self):
        self.main_window = QWidget()
        self.setCentralWidget(self.main_window)


#============LEFT PANEL=====================================================================================================================

        grid_layout = QGridLayout(self.main_window)
        self.main_window.setLayout(grid_layout)

        self.left_panel = QWidget(self.main_window)
        self.left_panel.setMinimumWidth(300)
        self.left_panel.setMaximumWidth(475)
        self.left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_panel.setStyleSheet(self.theme.left_panel_ui)
        grid_layout.addWidget(self.left_panel, 0, 0, 3, 1)

        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.left_panel_layout.setSpacing(5)

        #============ profile panel=======================
 
        self.profile_panel = QWidget(self.left_panel)
        self.profile_panel.setMinimumWidth(250)
        self.profile_panel.setMinimumHeight(70)
        self.profile_panel.setMaximumHeight(70)
        self.profile_panel.setStyleSheet(self.theme.widgets)
        self.left_panel_layout.addWidget(self.profile_panel)

        profile_panel_layout = QVBoxLayout(self.profile_panel)
        try:

            with open('profiles.json', 'r') as f:
                profiles_names_data = json.load(f)
        except FileNotFoundError:
            print('asd')

        self.selected_user = profiles_names_data["selected user"]

        profile_select_button = QPushButton(f"profile",  self.profile_panel)
        profile_select_button.setCursor(Qt.PointingHandCursor)
        profile_select_button.setStyleSheet(self.theme.buttons)       
        profile_panel_layout.addWidget(profile_select_button, alignment=Qt.AlignLeft)



        profile_select_button.clicked.connect(self.open_profile)
     
        #======= add tag and hide new tag list =====================================
        self.add_tag_panel = QWidget(self.left_panel)
        self.add_tag_panel.setMinimumWidth(250)
        self.add_tag_panel.setMinimumHeight(50)
        self.add_tag_panel.setMaximumHeight(70)
        self.add_tag_panel.setStyleSheet(self.theme.widgets_next)
        self.left_panel_layout.addWidget(self.add_tag_panel, stretch=1)

        self.add_tag_panel_layout = QHBoxLayout(self.add_tag_panel)

        self.tag_label = QLabel("new tags")
        self.tag_label.setStyleSheet(self.theme.qlabel)
        self.tag_label.setMinimumHeight(30)
        self.add_tag_panel_layout.addWidget(self.tag_label, alignment=Qt.AlignLeft)

        hide_new_tags = QPushButton("◯", self.add_tag_panel)
        hide_new_tags.setCursor(Qt.PointingHandCursor)
        hide_new_tags.setMinimumHeight(30)
        hide_new_tags.setStyleSheet(self.theme.buttons)
        self.add_tag_panel_layout.addWidget(hide_new_tags, alignment=Qt.AlignLeft)

        self.list_hidden = False
        def hide_new_tag_list():
            self.list_hidden = not self.list_hidden
            self.tag_list.setVisible(not self.list_hidden)

        hide_new_tags.clicked.connect(hide_new_tag_list)
        
        add_tag_button = QPushButton("add +", self.add_tag_panel)
        add_tag_button.setCursor(Qt.PointingHandCursor)
        add_tag_button.setMinimumHeight(30)
        add_tag_button.setStyleSheet(self.theme.buttons)
        self.add_tag_panel_layout.addWidget(add_tag_button, alignment=Qt.AlignRight)

       
        add_tag_button.clicked.connect(self.open_tag_window)

   
        
        self.tag_list = QWidget(self.left_panel)
        self.tag_list.setMinimumWidth(250)
        self.tag_list.setMinimumHeight(200)
        self.tag_list.setStyleSheet(self.theme.widgets)

        self.tag_list_layout = QVBoxLayout()
        self.tag_list_layout.setSpacing(0)
        self.tag_list_layout.setContentsMargins(0,0,0,0)
        self.tag_list.setLayout(self.tag_list_layout)

        new_tag_scroll_area = QScrollArea()
        new_tag_scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0,0,0,0)
        scroll_layout.setSpacing(2)
        scroll_layout.addStretch()
        scroll_content.setLayout(scroll_layout)
        
     
        new_tag_scroll_area.setWidget(scroll_content)
        new_tag_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }

            QScrollBar:vertical {
                background: #2c2c2c;
                width: 10px;
                margin: 2px 0 2px 0;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: #888;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar:horizontal {
                height: 8px;
                background: #2c2c2c;
            }

            QScrollBar::handle:horizontal {
                background: #555;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #888;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0;
                background: none;
                border: none;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

        
        self.tag_list_layout.addWidget(new_tag_scroll_area)
        

        self.left_panel_layout.addWidget(self.tag_list, stretch=7)


        #==========recent tags panel ==================

        self.recent_tag_panel = QWidget(self.left_panel)
        self.recent_tag_panel.setMinimumWidth(250)
        self.recent_tag_panel.setMinimumHeight(50)
        self.recent_tag_panel.setMaximumHeight(70)
        self.recent_tag_panel.setStyleSheet(self.theme.widgets_next)
        self.left_panel_layout.addWidget(self.recent_tag_panel, stretch=1)

        self.recent_tag_panel_layout = QHBoxLayout(self.recent_tag_panel)

        recent_tag_label = QLabel("recent tags")
        recent_tag_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        self.recent_tag_panel_layout.addWidget(recent_tag_label, alignment=Qt.AlignLeft)

        self.recent_list = QWidget(self.left_panel)
        self.recent_list.setMinimumWidth(250)
        self.recent_list.setMinimumHeight(200)
        self.recent_list.setStyleSheet(self.theme.widgets)

        self.recent_list_layout = QVBoxLayout()
        self.recent_list_layout.setSpacing(0)
        self.recent_list_layout.setContentsMargins(0,0,0,0)
        self.recent_list.setLayout(self.recent_list_layout)

        recent_scroll_area = QScrollArea()
        recent_scroll_area.setWidgetResizable(True)

        recent_scroll_content = QWidget()
        recent_scroll_layout = QVBoxLayout()
        recent_scroll_layout.setContentsMargins(0,0,0,0)
        recent_scroll_layout.setSpacing(0)
        recent_scroll_layout.addStretch()
        recent_scroll_content.setLayout(recent_scroll_layout)

        recent_scroll_area.setWidget(recent_scroll_content)
        recent_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }

            QScrollBar:vertical {
                background: #2c2c2c;
                width: 10px;
                margin: 2px 0 2px 0;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: #888;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar:horizontal {
                height: 8px;
                background: #2c2c2c;
            }

            QScrollBar::handle:horizontal {
                background: #555;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #888;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0;
                background: none;
                border: none;
            }

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

        
        self.recent_list_layout.addWidget(recent_scroll_area)
   
        
        self.left_panel_layout.addWidget(self.recent_list, stretch=13)


        self.new_tag_list = TagList(scroll_layout, recent_scroll_layout)
        self.new_tag_list.load_new_tag_buttons()

       

    
      

        
      
       
        


      
      
#============TOP PANEL====================================================================================================================

        #======== search bar =========
        self.top_bar = QWidget(self.main_window)
        self.top_bar.setMinimumWidth(600)
        self.top_bar.setMinimumHeight(30)
        self.top_bar.setMaximumHeight(70)
        self.top_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.top_bar.setStyleSheet(self.theme.ui)
        grid_layout.addWidget(self.top_bar, 0, 1)

        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.setSpacing(0)

        self.search_bar_widget = QWidget(self.top_bar)
        self.search_bar_widget.setMinimumWidth(300)
        self.search_bar_widget.setStyleSheet(self.theme.widgets_next)
        self.top_bar_layout.addWidget(self.search_bar_widget)

        self.search_bar_widget_layout = QHBoxLayout(self.search_bar_widget)
        self.search_bar_widget_layout.setContentsMargins(10,1,1,10)
        self.search_bar_widget_layout.setSpacing(7)

        self.save_search = QPushButton("save search", self.search_bar_widget)
        self.save_search.setCursor(Qt.PointingHandCursor)
        self.save_search.setMinimumHeight(30)
        self.save_search.setMaximumWidth(170)
        self.save_search.setStyleSheet(self.theme.buttons)
        self.search_bar_widget_layout.addWidget(self.save_search)

        text_box = QLineEdit(self.search_bar_widget)
        text_box.setPlaceholderText("Search Example: black_cat")
        text_box.setMinimumHeight(30)
        text_box.setMinimumWidth(700)
        text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        text_box.setStyleSheet("""
            QLineEdit {
                background-color: #2f2f2f;
                color: white;
                border: 3px;
                padding: 5px;
                font-size: 21px;
            }
        """)

        self.search_bar_widget_layout.addWidget(text_box)

        self.set_size = QPushButton("size", self.search_bar_widget)
        self.set_size.setCursor(Qt.PointingHandCursor)
        self.set_size.setMinimumHeight(30)
        self.set_size.setMinimumWidth(70)
        self.set_size.setMaximumWidth(170)
        self.set_size.setStyleSheet(self.theme.buttons)
        self.search_bar_widget_layout.addWidget(self.set_size)

        self.main_area = QWidget(self.main_window)
        self.main_area.setMinimumWidth(300)
        self.main_area.setMinimumHeight(600)
        self.main_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_area.setStyleSheet(self.theme.ui)
        grid_layout.addWidget(self.main_area, 1, 1)

        self.main_area_layout = QVBoxLayout(self.main_area)

      

        self.import_entities = ImportEntities(self.main_area_layout)
        self.new_tag_list.import_entities.connect(self.import_entities.import_entity_box)
        
#============== bottom bar ====================

        self.bottom_bar = QWidget(self.main_window)
        self.bottom_bar.setMinimumHeight(30)
        self.bottom_bar.setMaximumHeight(50)
        self.bottom_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_bar.setObjectName("bottomBar")
        self.bottom_bar.setStyleSheet(self.theme.widgets_next)
        grid_layout.addWidget(self.bottom_bar, 2, 1)

        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_bar_layout.setSpacing(0)

        self.bottom_bar_area = QWidget(self.bottom_bar)
        self.bottom_bar_area.setStyleSheet(self.theme.widgets_next)

        self.bottom_bar_area_layout = QHBoxLayout(self.bottom_bar_area)
        self.bottom_bar_area_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_bar_area_layout.setSpacing(0)
        self.bottom_bar_layout.addWidget(self.bottom_bar_area, alignment=Qt.AlignCenter)

        self.page_count_area = QWidget(self.bottom_bar_area)
        self.page_count_area.setStyleSheet(self.theme.ui)  
        self.page_count_area.setMaximumWidth(600)
        self.page_count_area.setMinimumHeight(20)
        self.bottom_bar_area_layout.addWidget(self.page_count_area, alignment=Qt.AlignCenter)

        self.page_count_area_layout = QHBoxLayout(self.page_count_area)
        self.page_count_area_layout.setContentsMargins(0, 0, 0, 0)
        self.page_count_area_layout.setSpacing(25) 

        self.first_page = QPushButton("<<", self.page_count_area)
        self.first_page.setStyleSheet(self.theme.buttons)       
        self.page_count_area_layout.addWidget(self.first_page, alignment=Qt.AlignLeft)

        self.previous_page =  QPushButton("<", self.page_count_area)
        self.previous_page.setStyleSheet(self.theme.buttons)       
        self.previous_page.setCursor(Qt.PointingHandCursor)
        self.page_count_area_layout.addWidget(self.previous_page, alignment=Qt.AlignLeft)

        self.page_count =  QLabel("Page 3 of 14, 377 items", self.page_count_area)
        self.page_count.setStyleSheet(self.theme.buttons)       
        self.page_count.setMinimumWidth(100)
        self.page_count_area_layout.addWidget(self.page_count, alignment=Qt.AlignCenter)

        self.next_page =  QPushButton(">", self.page_count_area)
        self.next_page.setStyleSheet(self.theme.buttons)       
        self.next_page.setCursor(Qt.PointingHandCursor)
        self.page_count_area_layout.addWidget(self.next_page, alignment=Qt.AlignRight)

        self.last_page =  QPushButton(">>", self.page_count_area)
        self.last_page.setStyleSheet(self.theme.buttons)       
        self.last_page.setCursor(Qt.PointingHandCursor)
        self.page_count_area_layout.addWidget(self.last_page, alignment=Qt.AlignRight)

        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 20)
        grid_layout.setRowStretch(2, 1)

        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 3)

        self.close()

        try:
            with open('profiles.json', 'r') as f:
                profiles_names_data = json.load(f)
        except FileNotFoundError:
    
            print("json not found")

        self.selected_user = profiles_names_data["selected user"]

        if self.selected_user == None:
            self.profiles = ProfileManager(self)
            
            QTimer.singleShot(0, lambda: self.profiles.raise_())

            self.profiles.closed.connect(self.on_profile_closed)
               
    def open_profile(self):
            self.profiles = ProfileManager(self)
            self.profiles.refresh_buttons.connect(self.new_tag_list.load_new_tag_buttons)
            
    def on_profile_closed(self):

        try:
            with open('profiles.json', 'r') as f:
                profiles_names_data = json.load(f)
        except FileNotFoundError:
            print("json not found")

            
        self.selected_user = profiles_names_data["selected user"]
        

        if self.selected_user == None:
            self.close()

    def open_tag_window(self):
            self.tag_window = TagWindow(self.new_tag_list)
            mouse_pos = QCursor.pos()

         
            self.tag_window.move(mouse_pos)

            self.tag_window.show()


            
  

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
