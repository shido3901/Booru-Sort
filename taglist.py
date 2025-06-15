from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QPushButton,
    QLabel, QLineEdit, QApplication, QSizePolicy, QTextEdit
)
from PyQt5.QtGui import QFont, QIcon, QMouseEvent, QTextCursor, QCursor, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPoint, QObject

from import_entities import ImportEntities
import json
import os
import sys


class TagList(QObject):
    import_entities = pyqtSignal(str)
    def __init__(self, new_tag_list=None, recent_tag_list=None):
        super().__init__()

        self.new_tag_list = new_tag_list
        self.recent_tag_list = recent_tag_list

        self.font = QFont('Roboto')

        self.tag_list = {}
        self.recent_list = {}

        self.recent_tag = False
        self.load_recent_tags = False
   
    

    def load_new_tag_buttons(self):

        for i in reversed(range(self.recent_tag_list.count())):
            widget = self.recent_tag_list.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                #print(f'cleared {widget}')
                self.tag_list.clear()

        for i in reversed(range(self.new_tag_list.count())):
            widget = self.new_tag_list.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                #print(f'cleared {widget}')
                self.tag_list.clear()


        with open('profiles.json', 'r') as f:
            selected_user = json.load(f)
            self.current_user = selected_user["selected user"]

        self.nested_directory = f"profiles/{self.current_user}"

        os.makedirs(self.nested_directory, exist_ok=True)
        print(f'current user: {self.current_user}')
       
        try:
            self.new_tag_path = os.path.join(self.nested_directory, f'new tags.json')

            with open(self.new_tag_path, 'r') as f:
                tag_data = json.load(f)

                self.tag_list = tag_data
        except FileNotFoundError:
             self.tag_list = {}
             print('no json yet')


        try:
            self.recent_tag_path = os.path.join(self.nested_directory, f'recent tags.json')

            with open(self.recent_tag_path, 'r') as f:
                recent_tag_data = json.load(f)

                self.recent_list = recent_tag_data
        except FileNotFoundError:
             print('no json yet')
             self.recent_list = {}

        
        for tag_name in list(self.tag_list)[:50][::-1]:
              entity_count = self.tag_list[tag_name]
              self.create_new_tag_buttons(tag_name, entity_count)
              
    
        self.load_recent_tags = True

        for tag_name in list(self.recent_list)[:100][::-1]:
            entity_count = self.recent_list[tag_name]
            self.create_new_tag_buttons(tag_name, entity_count)


        self.load_recent_tags = False


    def add_tags(self, tags):

        for tag_name in tags:
            if tag_name not in self.tag_list:
                self.tag_list = {tag_name: 0, **self.tag_list}
                self.create_new_tag_buttons(tag_name, 0)

                data = {
                    f"{tag_name}": "",
                }

                tag_path_file = os.path.join(self.nested_directory, f'{tag_name}.json')
                with open(tag_path_file, 'w') as f:
                    json.dump(data, f, indent=4)


        with open(self.new_tag_path, 'w') as f:
                json.dump(self.tag_list, f, indent=4)


        print(f'addted {tag_name} to {self.current_user}')
                

    def create_new_tag_buttons(self, tag_name, entity_count):
                
                tag_button_widget = QWidget()
                tag_button_widget.setFixedHeight(38)
                tag_button_widget.setStyleSheet(
                                        "background-color: #112233")
                
                if self.recent_tag == False and self.load_recent_tags == False:
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
                import_pics.clicked.connect(lambda: self.import_entities.emit(tag_name))
                import_pics.setMinimumWidth(20)
                import_pics.setStyleSheet("QPushButton { color: white; background-color: #112233; border: none; font-size: 29px; } QPushButton:hover { color: #00FFFF; }")
                tag_button_layout.addWidget(import_pics, alignment=Qt.AlignRight)

                self.recent_tag = False

        

    def add_to_recent(self, recent_tag_name, entity_count):
       
            if recent_tag_name in self.recent_list:
                tag_name_list = list(self.recent_list.keys())
                    
                widget_position = tag_name_list.index(recent_tag_name)
             
                widget = self.recent_tag_list.itemAt(widget_position).widget()
                widget.deleteLater()
                del self.recent_list[recent_tag_name]

            self.recent_tag = True

            if recent_tag_name not in self.recent_list:
                self.create_new_tag_buttons(recent_tag_name, entity_count)

            self.recent_list = {recent_tag_name: entity_count, **self.recent_list}
            
        
            with open( self.recent_tag_path, 'w') as f:
                json.dump(self.recent_list, f, indent=4)      
                 

            print(self.recent_list)
            print(f'the tag list should be {self.tag_list}')




    def delete_tag(self, tag_name, entity_count):
        dialog = ConfirmDeleteDialog(tag_name, entity_count)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            
            if tag_name in self.tag_list:
                tag_name_list = list(self.tag_list.keys())
                    
                widget_position = tag_name_list.index(tag_name)
             
                widget = self.new_tag_list.itemAt(widget_position).widget()
                widget.deleteLater()
                del self.tag_list[tag_name]

                with open(self.new_tag_path, 'w') as f:
                    json.dump(self.tag_list, f, indent=4) 

                file_path = os.path.join(self.nested_directory, f'{tag_name}.json')

                if os.path.exists(file_path):
                    os.remove(file_path)

            if tag_name in self.recent_list:
                tag_name_list = list(self.recent_list.keys())
                    
                widget_position = tag_name_list.index(tag_name)
             
                widget = self.recent_tag_list.itemAt(widget_position).widget()
                widget.deleteLater()
                del self.recent_list[tag_name]

                with open(self.recent_tag_path, 'w') as f:
                    json.dump(self.recent_list, f, indent=4)

            print(self.tag_list)
            print(self.recent_list)
        
    
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

        label = QLabel(f"Delete '{tag_name}'?\n{entity_count} item{'s' if entity_count != 1 else ''} will be deleted!" if entity_count else f"Delete '{tag_name}'?")

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
