from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QPushButton,
    QLabel, QLineEdit, QApplication, QSizePolicy, QTextEdit
)
from PyQt5.QtGui import QFont, QIcon, QMouseEvent, QTextCursor, QCursor, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPoint
import json
import os
import sys


class TagList():
    def __init__(self, new_tag_list=None, recent_tag_list=None):

        self.new_tag_list = new_tag_list
        self.recent_tag_list = recent_tag_list

        self.font = QFont('Roboto')

        self.tag_list = {
    "cats": 345,
    "nature": 12823,
    "dogs": 10560,
    "holidays": 2457,
    "beach": 42334,
    "mountains": 9876,
    "cityscape": 12345,
    "food": 987,
    "sports": 14312,
    "landscape": 6795,
    "architecture": 8754,
    "animals": 45678,
    "people": 87654,
    "cars": 123456,
    "flowers": 34567,
    "wildlife": 43210,
    "travel": 23456,
    "street": 3456,
    "sunset": 7654,
    "portrait": 876,
    "art": 5432,
    "snow": 6789,
    "winter": 1234,
    "summer": 2345,
    "spring": 67890,
    "fall": 12345,
    "vacation": 89012,
    "adventure": 4321,
    "fashion": 23456,
    "music": 12345,
    "photography": 6789,
    "urban": 23456,
    "history": 9876,
    "culture": 1234,
    "technology": 45678,
    "design": 2345,
    "night": 8765,
    "festival": 23456,
    "nightlife": 12345,
    "events": 56789,
    "fitness": 23456,
    "shopping": 6789,
    "wedding": 123456,
    "family": 34567,
    "friends": 12345,
    "mountain": 8765,
    "landscapes": 3456,
    "sky": 9876,
    "ocean": 56789,
    "desert": 12345
}

        self.recent_list = {}

        self.recent_tag = False

    def load_new_tag_buttons(self):

    
         
        for tag_name in list(self.tag_list)[:50][::-1]:
            entity_count = self.tag_list[tag_name]
            self.create_new_tag_buttons(tag_name, entity_count)

    def add_tags(self, tags):
        for tag_name in tags:
            if tag_name not in self.tag_list:
                self.tag_list = {tag_name: 0, **self.tag_list}
                self.create_new_tag_buttons(tag_name, 0)
                print(self.tag_list)
                

    def create_new_tag_buttons(self, tag_name, entity_count):
                
                tag_button_widget = QWidget()
                tag_button_widget.setFixedHeight(38)
                tag_button_widget.setStyleSheet(
                                        "background-color: #112233")
                
                if self.recent_tag == False:
                    self.new_tag_list.insertWidget(0, tag_button_widget)
                else:
                    self.recent_tag_list.insertWidget(0, tag_button_widget)

                tag_button_layout = QHBoxLayout()
                tag_button_layout.setContentsMargins(0,0,0,5)
                tag_button_widget.setLayout(tag_button_layout)

                tag_button = RightClickButton(tag_name)
                tag_button.setFont(self.font)
                tag_button.setFixedHeight(34)
                tag_button.setStyleSheet("QPushButton { color: white; background-color: #112233; border: none; font-size: 25px; } QPushButton:hover { color: #00FFFF; }")
                tag_button_layout.addWidget(tag_button, alignment=Qt.AlignLeft)
                tag_button_layout.addStretch()

                tag_button.clicked.connect(lambda checked=False, t=tag_name: self.add_to_recent(t, entity_count))
                tag_button.rightClicked.connect(lambda t=tag_name: self.delete_tag(t, entity_count))

               
                if entity_count >= 1000:
                    entity_display = f"{entity_count / 1000:.1f}k"
                else: 
                    entity_display = entity_count

                tag_entity_count = QLabel(str(entity_display))
                tag_entity_count.setFont(self.font)
                tag_entity_count.setMinimumWidth(15)
                tag_entity_count.setFixedHeight(40)
                tag_entity_count.setStyleSheet("color: #B0B0B0; background-color: #112233; border: none; font-size: 23px; }")
                tag_button_layout.addWidget(tag_entity_count, alignment=Qt.AlignRight)

                import_pics = QPushButton("+")
                import_pics.setFont(self.font)
                import_pics.setMinimumWidth(20)
                import_pics.setStyleSheet("QPushButton { color: white; background-color: #112233; border: none; font-size: 29px; } QPushButton:hover { color: #00FFFF; }")
                tag_button_layout.addWidget(import_pics, alignment=Qt.AlignRight)

                self.recent_tag = False

        

    def add_to_recent(self, recent_tag_name, entity_count):
       
            if recent_tag_name in self.recent_list:
                tag_name_list = list(self.recent_list.keys())
                    
                widget_position = tag_name_list.index(recent_tag_name)
                print(widget_position)
             
                widget = self.recent_tag_list.itemAt(widget_position).widget()
                widget.deleteLater()
                del self.recent_list[recent_tag_name]

            self.recent_tag = True

            if recent_tag_name not in self.recent_list:
                self.create_new_tag_buttons(recent_tag_name, entity_count)

            self.recent_list = {recent_tag_name: entity_count, **self.recent_list}

            print(self.recent_list)


    def delete_tag(self, tag_name, entity_count):
        dialog = ConfirmDeleteDialog(tag_name, entity_count)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            print('dfs')
    
class TagWindow(QDialog):
    def __init__(self, new_tag_list):
        super().__init__()

        self.new_tag_list = new_tag_list

       
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
        # Get the input text from the text box, remove leading/trailing whitespace
        tag_name_list = self.text_box.toPlainText().strip()

        tag_names = tag_name_list.split()

      
        self.new_tag_list.add_tags(tag_names)

      
        self.accept()  



class ConfirmDeleteDialog(QDialog):
    def __init__(self, tag_name, entity_count, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Tag?")
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.setStyleSheet("background-color: black; color: white;")
        self.setFixedSize(500, 250)  

        layout = QVBoxLayout()
      
        label = QLabel(f"Delete '{tag_name}'?\n {entity_count} items will be deleted!")
        label.setStyleSheet("font-size: 25px;")
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



class RightClickButton(QPushButton):
        rightClicked = pyqtSignal()

        def __init__(self, text, parent=None):
            super().__init__(text, parent)

        def mousePressEvent(self, event):
            if event.button() == Qt.RightButton:
                self.rightClicked.emit()
                    
            else:
                super().mousePressEvent(event)
