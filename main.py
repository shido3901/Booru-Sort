import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget, QLineEdit, QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtCore import Qt


debug_mode = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Booru Sort Lite")
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #010c1c;")

        self.initUI()

    def initUI(self):
        main_window = QWidget()
        self.setCentralWidget(main_window)

        if debug_mode == 0:
            self.ui = "color: black; background-color: white; border: 2px dashed red;"
            self.left_panel_ui = "color: black; background-color: white; border: 2px dashed red;"
            self.widgets = "color: black; background-color: yellow; border: 2px dashed red;"
            self.widgets_next = "color: black; background-color: green; border: 2px dashed red;"
            
        else:
            self.ui = "color: white; background-color: #112233; border: 2px solid #1f618d; border-radius: 10px;"
            self.left_panel_ui = "color: white; background-color;"
            self.widgets = "color: white; background-color: #112233; border: 2px solid #1f618d; border-radius: 10px;"
            self.widgets_next = "color: white; background-color: #010c1c; border: 2px solid #1f618d; border-radius: 10px;"

#============LEFT PANEL=====================================================================================================================

        grid_layout = QGridLayout(main_window)
        main_window.setLayout(grid_layout)

        self.left_panel = QWidget(main_window)
        self.left_panel.setMinimumWidth(300)
        self.left_panel.setMaximumWidth(475)
        self.left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_panel.setStyleSheet(self.left_panel_ui)
        grid_layout.addWidget(self.left_panel, 0, 0, 3, 1)

        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.left_panel_layout.setSpacing(5)

        #============ profile panel=======================
 
        self.profile_panel = QWidget(self.left_panel)
        self.profile_panel.setMinimumWidth(250)
        self.profile_panel.setMinimumHeight(70)
        self.profile_panel.setMaximumHeight(70)
        self.profile_panel.setStyleSheet(self.widgets)
        self.left_panel_layout.addWidget(self.profile_panel)

        profile_panel_layout = QVBoxLayout(self.profile_panel)

        profile_select_button = QPushButton("profile :",  self.profile_panel)
        profile_select_button.setCursor(Qt.PointingHandCursor)
        profile_select_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)       
        profile_panel_layout.addWidget(profile_select_button, alignment=Qt.AlignLeft)
    
        #======= add tag and hide new tag list =====================================
        self.add_tag_panel = QWidget(self.left_panel)
        self.add_tag_panel.setMinimumWidth(250)
        self.add_tag_panel.setMinimumHeight(50)
        self.add_tag_panel.setMaximumHeight(70)
        self.add_tag_panel.setStyleSheet(self.widgets_next)
        self.left_panel_layout.addWidget(self.add_tag_panel, stretch=1)

        self.add_tag_panel_layout = QHBoxLayout(self.add_tag_panel)

        self.tag_label = QLabel("new tags")
        self.tag_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        self.tag_label.setMinimumHeight(30)
        self.add_tag_panel_layout.addWidget(self.tag_label, alignment=Qt.AlignLeft)

        hide_new_tags = QPushButton("◯", self.add_tag_panel)
        hide_new_tags.setCursor(Qt.PointingHandCursor)
        hide_new_tags.setMinimumHeight(30)
        hide_new_tags.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)
        self.add_tag_panel_layout.addWidget(hide_new_tags, alignment=Qt.AlignLeft)

        self.list_hidden = False
        def hide_new_tag_list():
            self.list_hidden = not self.list_hidden
            self.tag_list.setVisible(not self.list_hidden)

        hide_new_tags.clicked.connect(hide_new_tag_list)
        
        add_tag_button = QPushButton("add +", self.add_tag_panel)
        add_tag_button.setCursor(Qt.PointingHandCursor)
        add_tag_button.setMinimumHeight(30)
        add_tag_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)
        self.add_tag_panel_layout.addWidget(add_tag_button, alignment=Qt.AlignRight)
        
        self.tag_list = QWidget(self.left_panel)
        self.tag_list.setMinimumWidth(250)
        self.tag_list.setMinimumHeight(200)
        self.tag_list.setStyleSheet(self.widgets)
        self.left_panel_layout.addWidget(self.tag_list, stretch=7)

        #==========recent tags panel ==================

        self.recent_tag_panel = QWidget(self.left_panel)
        self.recent_tag_panel.setMinimumWidth(250)
        self.recent_tag_panel.setMinimumHeight(50)
        self.recent_tag_panel.setMaximumHeight(70)
        self.recent_tag_panel.setStyleSheet(self.widgets_next)
        self.left_panel_layout.addWidget(self.recent_tag_panel, stretch=1)

        self.recent_tag_panel_layout = QHBoxLayout(self.recent_tag_panel)

        recent_tag_label = QLabel("recent tags")
        recent_tag_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        self.recent_tag_panel_layout.addWidget(recent_tag_label, alignment=Qt.AlignLeft)

    
        
        self.recent_list = QWidget(self.left_panel)
        self.recent_list.setMinimumWidth(250)
        self.recent_list.setMinimumHeight(30)
        self.recent_list.setStyleSheet(self.widgets)
        self.left_panel_layout.addWidget(self.recent_list, stretch=13)

      
      
#============TOP PANEL====================================================================================================================

        #======== search bar =========
        self.top_bar = QWidget(main_window)
        self.top_bar.setMinimumWidth(600)
        self.top_bar.setMinimumHeight(30)
        self.top_bar.setMaximumHeight(70)
        self.top_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.top_bar.setStyleSheet(self.ui)
        grid_layout.addWidget(self.top_bar, 0, 1)

        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_layout.setSpacing(5)


        self.search_bar_widget = QWidget(self.top_bar)
        self.search_bar_widget.setMinimumWidth(300)
        self.search_bar_widget.setStyleSheet(self.widgets_next)
        self.top_bar_layout.addWidget(self.search_bar_widget)

        self.search_bar_widget_layout = QHBoxLayout(self.search_bar_widget)
        self.search_bar_widget_layout.setContentsMargins(10,5,5,10)
        self.search_bar_widget_layout.setSpacing(10)


        self.save_search = QPushButton("save search", self.search_bar_widget)
        self.save_search.setCursor(Qt.PointingHandCursor)
        self.save_search.setMinimumHeight(30)
        self.save_search.setMaximumWidth(170)
        self.save_search.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)
        self.search_bar_widget_layout.addWidget(self.save_search)


        text_box = QLineEdit(self.search_bar_widget)
        text_box.setPlaceholderText("Search Example: black_cat")
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
        self.set_size.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)
        self.search_bar_widget_layout.addWidget(self.set_size)





      
        self.main_area = QWidget(main_window)
        self.main_area.setMinimumWidth(300)
        self.main_area.setMinimumHeight(600)
        self.main_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_area.setStyleSheet(self.ui)
        grid_layout.addWidget(self.main_area, 1, 1)
     
#============== bottom bar ====================

        self.bottom_bar = QWidget(main_window)
        self.bottom_bar.setMinimumHeight(30)
        self.bottom_bar.setMaximumHeight(50)
        self.bottom_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bottom_bar.setObjectName("bottomBar")
        self.bottom_bar.setStyleSheet(self.widgets_next)
        grid_layout.addWidget(self.bottom_bar, 2, 1)

        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_bar_layout.setSpacing(0)

        self.bottom_bar_area = QWidget(self.bottom_bar)
        self.bottom_bar_area.setStyleSheet(self.widgets_next)

        self.bottom_bar_area_layout = QHBoxLayout(self.bottom_bar_area)
        self.bottom_bar_area_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_bar_area_layout.setSpacing(0)
        self.bottom_bar_layout.addWidget(self.bottom_bar_area, alignment=Qt.AlignCenter)

        self.page_count_area = QWidget(self.bottom_bar_area)
        self.page_count_area.setStyleSheet(self.ui)  
        self.page_count_area.setMaximumWidth(600)
        self.page_count_area.setMinimumHeight(20)
        self.bottom_bar_area_layout.addWidget(self.page_count_area, alignment=Qt.AlignCenter)

        self.page_count_area_layout = QHBoxLayout(self.page_count_area)
        self.page_count_area_layout.setContentsMargins(0, 0, 0, 0)
        self.page_count_area_layout.setSpacing(25) 


        self.first_page = QPushButton("<<", self.page_count_area)
        self.first_page.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)       
        self.page_count_area_layout.addWidget(self.first_page, alignment=Qt.AlignLeft)


        self.previous_page =  QPushButton("<", self.page_count_area)
        self.previous_page.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)       
        self.previous_page.setCursor(Qt.PointingHandCursor)
        self.page_count_area_layout.addWidget(self.previous_page, alignment=Qt.AlignLeft)

        self.page_count =  QLabel("Page 3 of 14, 377 items", self.page_count_area)
        self.page_count.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)       
        self.page_count.setMinimumWidth(100)
        self.page_count_area_layout.addWidget(self.page_count, alignment=Qt.AlignCenter)

        self.next_page =  QPushButton(">", self.page_count_area)
        self.next_page.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)       
        self.next_page.setCursor(Qt.PointingHandCursor)
        self.page_count_area_layout.addWidget(self.next_page, alignment=Qt.AlignRight)

        self.last_page =  QPushButton(">>", self.page_count_area)
        self.last_page.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #112233;
                border: none;
                font-size: 25px;
            }

            QPushButton:hover {
                color: #00FFFF;  
            }
        """)       
        self.last_page.setCursor(Qt.PointingHandCursor)
        self.page_count_area_layout.addWidget(self.last_page, alignment=Qt.AlignRight)




        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 20)
        grid_layout.setRowStretch(2, 1)

        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 3)
       
        
        
    
        








def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
