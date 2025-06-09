from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTextEdit, 
                             QPushButton, QHBoxLayout)

from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import QObject, QEvent, Qt
#from tag import TagManager

import json

class TagWindow(QDialog):
    def __init__(self, tag_list_manager, parent=None):
        super().__init__(parent)

        self.tag_list_manager = tag_list_manager

       
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: #171717;")
        self.setWindowTitle(" ")
        self.setGeometry(100, 300, 500, 400)

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
    def __init__(self, tag_list_area, tag_list_area_layout, 
                 tag_list_recent_panel, tag_list_recent_panel_layout, parent=None):
        super().__init__()
        
        self.tag_list_area = tag_list_area
        self.tag_list_area_layout = tag_list_area_layout 
        self.parent = parent
        self.tag_list = []

        self.add_tag_recent = RecentTags(tag_list_recent_panel, tag_list_recent_panel_layout, self)

    def create_tag_window(self):
       dialog = TagWindow(self)
       dialog.exec_()

    def add_tag_to_list(self, tag_name_list):
        self.tag_list = tag_name_list + self.tag_list
        print("new tag list:", self.tag_list)

    def tag_load_images(self, tag_name):  #tag.py module
 
        #self.tag_manager = TagManager(tag_name)

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
 
        for i, tag_name in enumerate(self.tag_list):
            tag_button = QPushButton(tag_name)
            tag_button.setStyleSheet("""
                background-color: #333333;
                color: white;
                padding: 10px;
                border-radius: 5px;
            """)
            tag_button.setFont(QFont("Arial", 10))
            tag_button.clicked.connect(lambda checked=False, name=tag_name: self.add_tag_recent.recent_tag_add(name))
            tag_button.installEventFilter(self)

            self.tag_list_area_layout.addWidget(tag_button, i, 0, alignment=Qt.AlignTop)


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
            
                self.tag_list.remove(tag_name)

                print(self.tag_list)
                self.refresh_list()


class RecentTags(QObject):
    def __init__(self, tag_list_recent_panel, tag_list_recent_panel_layout, tag_list_manager):
        super().__init__()

        self.tag_list_recent_panel = tag_list_recent_panel_layout
        self.recent_tag_list = []

        self.tag_list_manager = tag_list_manager
        
    
    def recent_tag_add(self, name):
        self.tag_name = name
        if self.tag_name in self.recent_tag_list:

            self.recent_tag_list.remove(self.tag_name)
        self.recent_tag_list.insert(0, self.tag_name)

        self.refresh_recent_list()
        
     
    def load_recent_buttons(self):

        for i, self.tag_name in enumerate(self.recent_tag_list):
            recent_tag_button = QPushButton(self.tag_name)
            recent_tag_button.setStyleSheet("""
                background-color: #333333;
                color: white;
                padding: 10px;
                border-radius: 5px;
            """)
            recent_tag_button.setFont(QFont("Arial", 10))
            recent_tag_button.clicked.connect(lambda checked=False, name=self.tag_name: self.recent_tag_add(name))
            recent_tag_button.installEventFilter(self)
            
            self.tag_list_recent_panel.addWidget(recent_tag_button, i, 0, alignment=Qt.AlignLeft)


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
            
                self.recent_tag_list.remove(tag_name)

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

        # Connect buttons
        yes_button.clicked.connect(self.accept)
        no_button.clicked.connect(self.reject)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)