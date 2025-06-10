import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QLineEdit, QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton)
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, QEvent

from view_elements import ImageManager
from taglist import TagListManager, RecentTags
from user_profiles import ProfileManager
from tag import TagManager


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

        #=======left panel===========

        self.settings_panel = QWidget(main_window)
        self.settings_panel.setMinimumWidth(350)
        self.settings_panel.setMaximumWidth(520)
        self.settings_panel.setMaximumHeight(70)
        self.settings_panel.setMinimumHeight(70)
        self.settings_panel.setStyleSheet("background-color: #112233;"
                                          "border-radius: 10px;" 
                                          "border: 2px solid #1f618d")
        
        self.settings_panel_layout = QHBoxLayout(self.settings_panel)
        self.user_profile = ProfileManager()
        self.profile_button = QPushButton("profile test", self.settings_panel)
        self.profile_button.setStyleSheet("color: white; background-color: black; border: none;")
        self.settings_panel_layout.addWidget(self.profile_button, alignment=Qt.AlignLeft)

        

        self.profile_button.clicked.connect(self.user_profile.show) 

        self.tag_list_panel = QWidget(main_window)
        self.tag_list_panel.setMinimumWidth(320)
        self.tag_list_panel.setMaximumWidth(520)
  
        self.tag_list_panel.setObjectName("tagPanel")
        self.tag_list_panel.setStyleSheet("#tagPanel {background-color: #112233;"
                                          "border-radius: 10px;" 
                                          "border: 2px solid #1f618d }")
        
        #112233
        
        self.tag_top_bar = QWidget(self.tag_list_panel)
        self.tag_top_bar.setMinimumWidth(140)
        self.tag_top_bar.setMaximumWidth(520)
        self.tag_top_bar.setMinimumHeight(50)
        self.tag_top_bar.setMaximumHeight(50)
     
        self.tag_top_bar.setStyleSheet("background-color: #112233;")
        
        self.tag_top_bar_layout = QHBoxLayout(self.tag_top_bar)
        self.tag_top_bar_layout.setContentsMargins(0,0,0,0)
        self.tag_top_bar_layout.setSpacing(0)
        self.tag_top_bar.setLayout(self.tag_top_bar_layout)

        self.tag_label = QLabel("new tags", self.tag_top_bar)
        self.tag_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        self.tag_label.setMinimumHeight(50)
        self.tag_label.setMinimumWidth(20)
     

        create_tag_button = QPushButton("add +", self.tag_top_bar)
        create_tag_button.setStyleSheet("""
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

       
        create_tag_button.setMinimumHeight(50)
        create_tag_button.setMinimumWidth(20)
        create_tag_button.setMaximumWidth(80)
       
        self.tag_top_bar_layout.addWidget(self.tag_label)
        self.tag_top_bar_layout.addWidget(create_tag_button, alignment=Qt.AlignRight)

        
        self.tag_list_panel_layout = QVBoxLayout(self.tag_list_panel)
        self.tag_list_panel.setLayout(self.tag_list_panel_layout)


        self.tag_list_area = QWidget(self.tag_list_panel)
        self.tag_list_area.setMinimumWidth(310)
        self.tag_list_area.setMinimumHeight(300)
        self.tag_list_area.setObjectName("tagList")
        self.tag_list_area.setStyleSheet("#tagList {background-color: #112233;"
                                        "border-radius: 15px;" 
                                          "border: 3px solid #444444;} ") ##112233
        
        #elf.tag_number


        self.tag_list_area_layout = QVBoxLayout()
        self.tag_list_area.setLayout(self.tag_list_area_layout)
       

        self.tag_list_recent_panel = QWidget(self.tag_list_panel)
        self.tag_list_recent_panel.setMinimumWidth(310)
        self.tag_list_recent_panel.setMaximumWidth(520)
        self.tag_list_recent_panel.setMinimumHeight(600)
        self.tag_list_recent_panel.setStyleSheet("background-color: #112233;"
                                        "border-radius: 15px;" 
                                          "border: 3px solid #444444; ") ##112233

    

        self.tag_list_recent_panel_layout = QVBoxLayout()
        self.tag_list_recent_panel.setLayout(self.tag_list_recent_panel_layout)

        #idfk how this got so convoluted lmao fix later
        self.tag_list_manager = TagListManager(self.tag_list_area, self.tag_list_area_layout,
                                               self.tag_list_recent_panel, 
                                               self.tag_list_recent_panel_layout,
                                                )


        self.recent_tag_list = RecentTags(self.tag_list_recent_panel, 
                                          self.tag_list_recent_panel_layout,
                                          self.tag_list_manager)

       
        self.tag_list_panel_layout.addWidget(self.tag_top_bar)

        self.tag_list_panel_layout.addWidget(self.tag_list_area, stretch=2)
        self.tag_list_panel_layout.addWidget(self.tag_list_recent_panel, stretch=4)
        
        self.tag_list_panel_layout.setSpacing(0)
      

        

        
        create_tag_button.clicked.connect(self.tag_list_manager.create_tag_window)  

        
        #========middle area========

        self.image_area = QWidget(main_window)
        self.image_area.setMinimumWidth(300)
        self.image_area.setMinimumHeight(500)
        self.image_area.setObjectName("imageArea")
        self.image_area.setStyleSheet("#imageArea { border: 2px solid #1f618d;"
                                      "border-radius: 10px;"
                                      "background-color: #112233; }")
        
        self.search_bar = QWidget(main_window)
        self.search_bar.setMinimumWidth(200)
        self.search_bar.setMinimumHeight(70)
        self.search_bar.setMaximumHeight(70)
        self.search_bar.setObjectName("searchBar")
        self.search_bar.setStyleSheet("#searchBar { border: 2px solid #1f618d;"
                                      "border-radius: 10px;"
                                      "background-color: #112233; }")

        text_box = QLineEdit(self.search_bar)
        text_box.setPlaceholderText("Search Example: black_cat")
        text_box.setFixedHeight(50)
        text_box.setMinimumWidth(1200)
        text_box.setMaximumWidth(1200)
        text_box.setStyleSheet("""
            QLineEdit {
                background-color: #2f2f2f;
                color: white;
                border: 3px;
                padding: 5px;
                font-size: 20px;
            }
        """)

        self.options_bar = QWidget(main_window)
        self.options_bar.setFixedWidth(180)
        self.options_bar.setFixedHeight(70)
        self.options_bar.setObjectName("optionsBar")
        self.options_bar.setStyleSheet("#optionsBar { border: 2px solid #1f618d;"
                                      "border-radius: 10px;"
                                      "background-color: #112233; }")

        options_layout = QHBoxLayout(self.options_bar)
        options_layout.setContentsMargins(0, 0, 0, 0)

        search_layout = QHBoxLayout(self.search_bar)
        search_layout.setContentsMargins(5, 0, 0, 0)
        search_layout.setSpacing(5)
        
        #==============top bar=================

        search = QPushButton("Testing", self.search_bar)
        search.setStyleSheet("color: white; background-color; black border: none;")
        search.setFixedSize(70, 40)
        search_layout.addWidget(search, alignment=Qt.AlignRight)

        search_layout.addWidget(text_box, alignment=Qt.AlignCenter)

        tag_button = QPushButton("size", self.options_bar)
        tag_button.setStyleSheet("color: white; background-color: #606060; border: none;")
        tag_button.clicked.connect(lambda: self.image_manager.set_image_size(self.image_area_layout))
        tag_button.setFixedSize(120, 40)
        options_layout.addWidget(tag_button, alignment=Qt.AlignCenter)

        save_search = QPushButton("save", self.search_bar)
        search.setStyleSheet("color: white; background-color; black border: none;")
        search_layout.addWidget(save_search, alignment=Qt.AlignLeft)
        
        #==========bottom bar=============

        self.bottom_bar = QWidget(main_window)
        self.bottom_bar.setMinimumHeight(50)
        self.bottom_bar.setMaximumHeight(50)
        self.bottom_bar.setObjectName("bottomBar")
        self.bottom_bar.setStyleSheet("#bottomBar { border: 2px solid #1f618d;"
                                      "border-radius: 10px;"
                                      "background-color: #112233; }")
        self.bottom_bar.setContentsMargins(0, 0, 0, 0)

        bottom_bar_layout = QGridLayout()
        bottom_bar_layout.setContentsMargins(10, 0, 10, 0)
        bottom_bar_layout.setHorizontalSpacing(20)
        self.bottom_bar.setLayout(bottom_bar_layout)


        previous_page_click = QPushButton("Previous Page", self.bottom_bar)
        previous_page_click.setStyleSheet("color: white; background-color: #606060; border: none;")
        previous_page_click.setFixedSize(120, 40)

        skip_to_previous = QPushButton("Beg", self.bottom_bar)
        skip_to_previous.setStyleSheet("color: white; background-color: #606060; border: none;")
        skip_to_previous.setFixedSize(80, 40)

        self.page_count = QLabel("", self.bottom_bar)
        self.page_count.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.page_count.setAlignment(Qt.AlignCenter)

        skip_to_last = QPushButton("Last", self.bottom_bar)
        skip_to_last.setStyleSheet("color: white; background-color: #606060; border: none;")
        skip_to_last.setFixedSize(80, 40)

        next_page_click = QPushButton("Next Page", self.bottom_bar)
        next_page_click.setStyleSheet("color: white; background-color: #606060; border: none;")
        next_page_click.setFixedSize(120, 40)

      
        bottom_bar_layout.addWidget(previous_page_click, 0, 0)
        bottom_bar_layout.addWidget(skip_to_previous, 0, 1)
        bottom_bar_layout.addWidget(self.page_count, 0, 2, alignment=Qt.AlignCenter)
        bottom_bar_layout.addWidget(skip_to_last, 0, 3)
        bottom_bar_layout.addWidget(next_page_click, 0, 4)

        
        self.image_area_layout = QGridLayout()
        self.image_area.setLayout(self.image_area_layout)

        grid = QGridLayout()
        grid.addWidget(self.settings_panel, 0, 0, 1, 1) 
        grid.addWidget(self.tag_list_panel, 1, 0, 5, 1)
        grid.addWidget(self.search_bar, 0, 1)
        grid.addWidget(self.options_bar, 0, 2)
        grid.addWidget(self.image_area, 1, 1, 2, 2)
        
        
        grid.addWidget(self.bottom_bar, 4, 1, 2, 2)

        grid.setColumnStretch(0, 0)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setSpacing(5)
        grid.setContentsMargins(6, 6, 6, 6)

        main_window.setLayout(grid)

        self.image_area.installEventFilter(self)
    

        self.image_manager = ImageManager(self.image_area)
        self.image_manager.set_page_count_text(self.page_count)
        self.image_area.installEventFilter(self.image_manager)

        next_page_click.clicked.connect(self.image_manager.next_page)
        previous_page_click.clicked.connect(self.image_manager.previous_page)
        skip_to_last.clicked.connect(self.image_manager.skip_to_last)
        skip_to_previous.clicked.connect(self.image_manager.skip_to_previous)

      
        self.user_profile.profile_selected.connect(self.tag_list_manager.load_tag_startup)
        self.tag_list_manager.custom_signal.connect(self.import_entities)


        self.importing_files = True

    def import_entities(self, tag_name):
 
        for i in reversed(range(self.image_area_layout.count())):
            widget = self.image_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        drop_box = DropBox(tag_name=tag_name, tag_list=self.tag_list_manager.get_tag_list())
        drop_box.setMinimumSize(500, 500)
        drop_box.setStyleSheet("""
        background-color: white;
        border: 1px solid black;
    """)

        self.image_area_layout.addWidget(drop_box, 0, 0)

        self.importing_files = False

        
    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.importing_files == True:
            self.image_manager.resizeEvent(event)



class DropBox(QWidget):
    def __init__(self, tag_name, tag_list, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 150)
        self.setAcceptDrops(True)

        self.tag_name = tag_name
        self.tag_list = tag_list 

        self.setStyleSheet("""
            background-color: white;
            border: 2px dashed gray;
        """)

        self.label = QLabel(f"drag and drop to \n'{tag_name}'\nor", self)
        self.label.setStyleSheet("font-size: 30px;")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle the drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()  
        else:
            event.ignore()  

    def dropEvent(self, event: QDropEvent):
        """Handle the drop event when files are dropped"""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile() 

            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm')):
                print(f"Dropped file: {file_path}")
                self.label.setText(f"Loaded: {file_path.split('/')[-1]}") 

                if self.tag_name not in self.tag_list:
                    self.tag_list[self.tag_name] = []  

          
                self.tag_list[self.tag_name].append(file_path)

                print(f"Files under '{self.tag_name}': {self.tag_list[self.tag_name]}")
            else:
                print("Unsupported file type")



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
