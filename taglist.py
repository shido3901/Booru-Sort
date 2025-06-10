from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTextEdit,  QGridLayout, QRadioButton, QWidget,
                             QPushButton, QHBoxLayout, QSizePolicy)

from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import QObject, QEvent, Qt, pyqtSignal
from tag import TagManager
from collections import OrderedDict
from user_profiles import ProfileManager
from view_elements import ImageManager

import json

class TagWindow(QDialog):
    def __init__(self, tag_list_manager, parent=None):
        super().__init__(parent)

        self.tag_list_manager = tag_list_manager

       
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: #171717;")
        self.setWindowTitle(" ")
        self.setGeometry(100, 300, 500, 400)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel("enter tags, separated by space:")
        label.setStyleSheet("color: white;")
        label.setFont(QFont("Arial", 11))
        layout.addWidget(label, alignment=Qt.AlignCenter)

        self.text_box = QTextEdit()
        self.text_box.setStyleSheet("""
            background-color: #242323;
            color: white;
            border: none;
        """)
        self.text_box.setFont(QFont("Arial", 14))
        layout.addWidget(self.text_box)

   
        create_tag_button = QPushButton("create tag")
        create_tag_button.setStyleSheet("""
            background-color: #333333;
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)

        create_tag_button.setFont(QFont("Arial", 12))
        create_tag_button.clicked.connect(self.on_submit_clicked)
        layout.addWidget(create_tag_button, alignment=Qt.AlignCenter)

        self.text_box.setFocus()
        self.text_box.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.text_box and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Space:
                cursor = self.text_box.textCursor()
                pos = cursor.position()

                cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
                if cursor.selectedText() == " ":
                    cursor.removeSelectedText()
                    cursor.insertText("_")
                    return True
        return super().eventFilter(source, event)

    def on_submit_clicked(self):
     
        tag_name_list = self.text_box.toPlainText().strip()
        if tag_name_list:
       
            tag_name = [tag.lower() for tag in tag_name_list.split()]
            #print("created tag names:", tag_name)
            self.accept()  
            
            self.tag_list_manager.add_tag_to_list(tag_name)
            self.tag_list_manager.refresh_list()
        else:
          
            self.reject()  


class TagListManager(QObject):
    custom_signal = pyqtSignal(str)

    def __init__(self, tag_list_area, tag_list_area_layout, 
                 tag_list_recent_panel, tag_list_recent_panel_layout, parent=None):
        super().__init__()
        
        self.tag_list_area = tag_list_area
        self.tag_list_area_layout = tag_list_area_layout 
        self.parent = parent
        self.tag_list = {}

        self.add_tag_recent = RecentTags(tag_list_recent_panel, tag_list_recent_panel_layout, self)

        #json area
        self.list_data = "tag_list.json"
        self.profile_manager = ProfileManager()

        self.load_tag_startup()

    def get_tag_list(self):
        return self.tag_list

    def load_tag_startup(self):
        try:
            with open(self.profile_manager.data_file, "r") as f:
                user_data = json.load(f)
                name = user_data.get("selected_user")
                print(name, 'Maybe grabbed json"?')
        except (FileNotFoundError, json.JSONDecodeError):
            print("Could not read selected user.")
            return

        try:
            with open(self.list_data, "r") as f:
                all_user_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_user_data = {}
        
        if name in all_user_data:
            self.tag_list = all_user_data[name].get("new tag list", {}).copy()
            print("Loaded tag list:", self.tag_list)
        else:
            print(f"No data found for user: {name}")
            self.tag_list = {}

        self.refresh_list()
    


    def create_tag_window(self):
       dialog = TagWindow(self)
       dialog.exec_()

    def add_tag_to_list(self, tag_name_list):

        try:
            with open(self.profile_manager.data_file,"r") as f:
                user_data = json.load(f)
                self.name = user_data.get("selected_user")
               

                print(self.name, 'Maybe grabbed json"?')
        except (FileNotFoundError, json.JSONDecodeError):
            pass 

        for tag in tag_name_list:
            tag = tag.strip().lower()
            if tag and tag not in self.tag_list:
                self.tag_list[tag] = []

        try:
            with open(self.list_data, "r") as f:
                all_user_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_user_data = {}
                
        all_user_data[self.name] = {
            "new tag list": self.tag_list
        }

        with open(self.list_data, "w") as f:
            json.dump(all_user_data, f, indent=2)


    def tag_load_images(self, tag_name):  #tag.py module
 
        

        if tag_name in self.tag_list:
        
            self.tag_list.remove(tag_name)
            self.tag_list.insert(0, tag_name)
      
            self.refresh_list()


    def refresh_list(self):

        self.clear_layout()
        self.load_buttons()


    def clear_layout(self):
     
        while self.tag_list_area_layout.count():
            item = self.tag_list_area_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def load_buttons(self):

 
        for tag_name in self.tag_list:
            tag_button = QPushButton(tag_name)
            
            tag_button.setFont(QFont("Arial"))
            tag_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        background-color: #112233;
                        font-size: 22px;
                        text-align: left; 
                        border: none;  
                    }

                    QPushButton:hover {
                        color: #00FFFF; 
                    }
                """)


            tag_button.clicked.connect(lambda checked=False, name=tag_name: self.add_tag_recent.recent_tag_add(name))
           
            
            tag_button.installEventFilter(self)


            #====import photo button=====

            import_button = QPushButton(" +")
            import_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        background-color: #112233;
                        font-size: 23px;
                        text-align: left; 
                        border: none;  
                    }

                    QPushButton:hover {
                        color: #00FFFF; 
                    }
                """)
            
     
            manager = TagManager(tag_name)
            import_button.clicked.connect(lambda checked=False, mgr=manager: mgr.print_tag_name())
            import_button.clicked.connect(lambda checked=False, name=tag_name: self.custom_signal.emit(name))



            #==get entity count======

            tag_count = len(self.tag_list[tag_name])
            if tag_count >= 1000:
                tag_count_display_num = f"{tag_count / 1000:.1f}k"
            else:
                tag_count_display_num = str(tag_count)

            tag_count_display = QLabel(tag_count_display_num)
            tag_count_display.setStyleSheet("""
                color: white;
                font-size: 22px;
                background-color: #112233;
                border: none                            
            """)

            #=== UI stuff==========

            tag_button.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Fixed)
            

            row = QWidget()
            row.setStyleSheet("background-color: #112233;")
            row_layout = QHBoxLayout()
            row_layout.setSpacing(1)
            row_layout.setContentsMargins(0, 0, 0, 0)

            row_layout.addWidget(tag_button, alignment=Qt.AlignLeft)
  
            row_layout.addStretch(1)
            

            row_layout.addWidget(tag_count_display)
            row_layout.addWidget(import_button)

            row.setLayout(row_layout)
            self.tag_list_area_layout.addWidget(row)

        self.tag_list_area_layout.addStretch()


    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                tag_name = obj.text()
                self.handle_right_click(tag_name)
                return True  
        return False 
    
    
    def handle_right_click(self, tag_name):
        self.show_delete_box(tag_name)



    def show_delete_box(self, tag_name):
        dialog = ConfirmDeleteDialog(tag_name)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.delete_tag(tag_name)
            
            self.add_tag_recent.delete_recent_tag(tag_name)
        else:
            print("Cancelled.")



    def delete_tag(self, tag_name):
      
        if tag_name in self.tag_list:
            
            del self.tag_list[tag_name]

            print(self.tag_list)

            try:
                with open(self.profile_manager.data_file,"r") as f:
                    user_data = json.load(f)
                    self.name = user_data.get("selected_user")
                

                    print(self.name, 'Maybe grabbed json"?')
            except (FileNotFoundError, json.JSONDecodeError):
                pass 


            try:
                with open(self.list_data, "r") as f:
                    all_user_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_user_data = {}
                    
            all_user_data[self.name] = {
                "new tag list": self.tag_list
            }

            with open(self.list_data, "w") as f:
                json.dump(all_user_data, f, indent=2)

            self.refresh_list()  


        


class RecentTags(QObject):
    def __init__(self, tag_list_recent_panel, tag_list_recent_panel_layout, tag_list_manager):
        super().__init__()

        self.tag_list_recent_panel = tag_list_recent_panel_layout
        self.recent_tag_list = {}

        self.tag_list_manager = tag_list_manager
        
    
    def recent_tag_add(self, name):
        if not hasattr(self, 'recent_tag_list') or not isinstance(self.recent_tag_list, OrderedDict):
            self.recent_tag_list = OrderedDict()

        if name in self.recent_tag_list:
            del self.recent_tag_list[name]

        self.recent_tag_list[name] = {} 
        self.recent_tag_list.move_to_end(name, last=False)

        print(self.recent_tag_list)

        self.refresh_recent_list()


        
     
    def load_recent_buttons(self):

        for self.tag_name in self.recent_tag_list:
            recent_tag_button = QPushButton(self.tag_name)
            recent_tag_button.setFont(QFont("Arial"))

            recent_tag_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        background-color: #112233;
                        font-size: 22px;
                        text-align: left; 
                        border: none;  
                    }

                    QPushButton:hover {
                        color: #00FFFF; 
                    }
                """)
            
            recent_tag_button.clicked.connect(lambda checked=False, name=self.tag_name: self.recent_tag_add(name))
            recent_tag_button.installEventFilter(self)

            import_button = QPushButton("+")
            import_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        background-color: transparent;
                        font-size: 23px;
                        text-align: left; 
                        border: none;  
                    }

                    QPushButton:hover {
                        color: #00FFFF; 
                    }
                """)
            

            #==get entity count======

            tag_count = len(self.recent_tag_list[self.tag_name])
            if tag_count >= 1000:
                tag_count_display_num = f"{tag_count / 1000:.1f}k"
            else:
                tag_count_display_num = str(tag_count)

            tag_count_display = QLabel(tag_count_display_num)
            tag_count_display.setStyleSheet("""
                color: white;
                font-size: 22px;
                background-color: transparent;
            """)

            #=== UI stuff==========

            recent_tag_button.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Fixed)
            

            row = QWidget()
            row_layout = QHBoxLayout()
            row_layout.setSpacing(1)
            row_layout.setContentsMargins(0, 0, 0, 0)

            row_layout.addWidget(recent_tag_button, alignment=Qt.AlignLeft)
  
            row_layout.addStretch(1)
            

            row_layout.addWidget(tag_count_display)
            row_layout.addWidget(import_button)

            row.setLayout(row_layout)
            self.tag_list_recent_panel.addWidget(row)
        
        self.tag_list_recent_panel.addStretch()



        


    def clear_recent_tags(self):
     
        while self.tag_list_recent_panel.count():
            item = self.tag_list_recent_panel.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

 
    def refresh_recent_list(self):

        self.clear_recent_tags()
        self.load_recent_buttons()


    def delete_recent_tag(self, tag_name):
      
        if tag_name in self.recent_tag_list:
            
                del self.recent_tag_list[tag_name]

                print(self.recent_tag_list)
                self.refresh_recent_list()



    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                tag_name = obj.text()
                
                self.handle_right_click(tag_name)
                return True  
        return False 
    

    def handle_right_click(self, tag_name):
        self.show_delete_dialog(tag_name)

    def show_delete_dialog(self, tag_name):
        dialog = ConfirmDeleteDialog(tag_name)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            
            self.delete_recent_tag(tag_name)

            self.tag_list_manager.delete_tag(tag_name)


class ConfirmDeleteDialog(QDialog):
    def __init__(self, tag_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Tag?")
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.setStyleSheet("background-color: black; color: white;")
        self.setFixedSize(300, 200)  

        layout = QVBoxLayout()

      
        label = QLabel(f"Delete tag '{tag_name}'?")
        label.setStyleSheet("font-size: 19px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        for btn in (yes_button, no_button):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: white;
                    border: 1px solid white;
                    border-radius: 4px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #222;
                }
            """)
            btn.setFixedWidth(80)

      
        yes_button.clicked.connect(self.accept)
        no_button.clicked.connect(self.reject)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)