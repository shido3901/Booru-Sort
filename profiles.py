from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QDialog,
    QLabel, QLineEdit, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
import json
import os
import shutil
import sys


class DeleteProfileDialog(QDialog):
    def __init__(self, profile_name):
        super().__init__()
        self.setWindowTitle("Delete Profile")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        label = QLabel(f"delete '{profile_name}'?")
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete")
        cancel_btn = QPushButton("Cancel")
        delete_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

class ProfileManager(QDialog):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("users")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #112233;")
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.show()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.profiles_json = "profiles.json"

        self.profile_count = 0

        self.selected_data = {} 
        self.profile_buttons = []
        self.selected_user = None
        

        self.create_profile = False
        self.no_profile = True

        self.load_profile_buttons()

        self.col_cnt = 0
        self.row = 0

        

    
    def load_profile_buttons(self):

        with open('profiles.json', 'r') as f:
            profiles_names_data = json.load(f)

        self.profile_buttons = profiles_names_data["profiles"]
        self.profile_count = len(self.profile_buttons)
       
        self.row = 0
        self.col_cnt = 0
        i = 0

        for i in range(self.profile_count):

            self.row = i // 4
            self.col_cnt = i % 4

            self.add_profile_widget = QWidget()
            self.add_profile_widget.setFixedSize(150, 200)

            self.add_profile_widget_layout = QVBoxLayout(self.add_profile_widget)
            self.add_profile_widget_layout.setSpacing(0)
            self.add_profile_widget_layout.setContentsMargins(0, 0, 0, 0)

            profile_button = QPushButton(QIcon(r"C:\Users\Jon\Desktop\New folder\2bda51ca60cc3b5daaa8e062eb880430.jpg"), "")
            profile_button.setIconSize(QSize(150,150))
            profile_button.setFixedSize(150,150)

            self.profile_label = QLabel()
            name = self.profile_buttons[i] 
            self.profile_label.setText(name)
            self.profile_label.setAlignment(Qt.AlignCenter)

            self.profile_label.setStyleSheet("color: white;" "border: none;" "font-size: 18px;")
            self.profile_label.setFixedSize(150, 50)

            profile_button.clicked.connect(lambda checked, n=name: self.load_profile(n))

            profile_button.setContextMenuPolicy(Qt.CustomContextMenu)
            profile_button.customContextMenuRequested.connect(lambda _, n=name: self.on_profile_right_click(n))

            self.add_profile_widget_layout.addWidget(profile_button)
            self.add_profile_widget_layout.addWidget(self.profile_label)


            self.layout.addWidget(self.add_profile_widget, self.row, self.col_cnt)


        if self.profile_count == 0 and self.no_profile == True or i == self.profile_count - 1 and self.create_profile == False:
              

                if self.profile_count == 0:
                    last_row = 0
                    last_col = 0
                else:

                    last_row = self.profile_count // 4
                    last_col = self.profile_count % 4

                self.add_profile_button_widget = QWidget()
                self.add_profile_button_widget.setFixedSize(150, 200)
                
                self.add_profile_button_widget_layout = QVBoxLayout(self.add_profile_button_widget)
                self.add_profile_button_widget_layout.setSpacing(0) 
                self.add_profile_button_widget_layout.setContentsMargins(0, 0, 0, 0)  


                add_profile_button = QPushButton("+")
                add_profile_button.setFixedSize(150,150)
                add_profile_button.setStyleSheet("QPushButton { font-size: 40px; background-color: #444; color: white; border: 2px solid #888; border-radius: 8px; } QPushButton:hover { background-color: #666; }")

                self.add_label = QLabel("add profile")
                self.add_label.setAlignment(Qt.AlignCenter)
                self.add_label.setStyleSheet("color: white;"
                                            "border: none;"
                                            "font-size: 18px;")
                self.add_label.setFixedSize(150, 50)        
                
                self.add_profile_button_widget_layout.addWidget(add_profile_button, alignment=Qt.AlignTop)
                self.add_profile_button_widget_layout.addWidget(self.add_label, alignment=Qt.AlignBottom)
            
                add_profile_button.clicked.connect(self.create_new_profile)
                self.layout.addWidget(self.add_profile_button_widget, last_row, last_col)


        elif self.create_profile == True or self.profile_count == 0:
                
                last_row = self.profile_count // 4
                last_col = self.profile_count % 4
                
                self.add_profile_name = QWidget()
                self.add_profile_name.setFixedSize(150, 200)

                self.add_profile_name_layout = QVBoxLayout(self.add_profile_name)
                self.add_profile_name_layout.setSpacing(0)
                self.add_profile_name_layout.setContentsMargins(0, 0, 0, 0)

                profile_button = QPushButton(QIcon(r"C:\Users\Jon\Desktop\New folder\2bda51ca60cc3b5daaa8e062eb880430.jpg"), "")
                profile_button.setIconSize(QSize(150,150))
                profile_button.setFixedSize(150,150)

                self.input_box = QLineEdit()
                self.input_box.setPlaceholderText("profile name eg., miku")
                font = QFont()
                font.setPointSize(12)
                self.input_box.setFont(font)
                
                self.input_box.setFixedSize(150, 50)
                self.input_box.returnPressed.connect(lambda: self.profile_input(self.input_box))

                self.input_box.setStyleSheet("color: white;" "border: none;")
                self.input_box.setFixedSize(150, 50)
                self.input_box.setFocus()

                self.add_profile_name_layout.addWidget(profile_button, alignment=Qt.AlignTop)
                self.add_profile_name_layout.addWidget(self.input_box, alignment=Qt.AlignBottom)

                self.layout.addWidget(self.add_profile_name, last_row, last_col)

    def on_profile_right_click(self, name):
        delete_dialog = DeleteProfileDialog(name)
        if delete_dialog.exec_() == QDialog.Accepted:
            
            self.profile_buttons.remove(name)

            profile_name = name
            self.no_profile = True

            profile_data = {
                "profiles": self.profile_buttons,
                "selected user": self.selected_user
            }

            with open('profiles.json', 'w') as f:
                json.dump(profile_data, f, indent=4)

            try:
                shutil.rmtree(f"profiles/{profile_name}")
            except FileNotFoundError:
                 print('No folder font for user')

            self.refresh_profiles()
            
    def create_new_profile(self):
       
        if len(self.profile_buttons) == 0:
             self.no_profile = False


        self.create_profile = True
        self.refresh_profiles()


    def profile_input(self, input_box):

        profile_name = self.input_box.text()
        self.profile_buttons.append(profile_name)

        #directory_name =profile_name

        try:
            os.mkdir("profiles")
        except FileExistsError:
            print('File already exists')

        nested_directory = f"profiles/{profile_name}"

        try:
            os.makedirs(nested_directory)
        except FileExistsError:
            print('Directory already exists')

        self.create_profile = False

        profile_data = {
                "profiles": self.profile_buttons,
                "selected user": self.selected_user
            }

        with open('profiles.json', 'w') as f:
                json.dump(profile_data, f, indent=4)
        
        self.refresh_profiles()


    def refresh_profiles(self):
         
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
        self.load_profile_buttons()

    def load_profile(self, name):

        self.selected_user = name

        profile_data = {
                "profiles": self.profile_buttons,
                "selected user": self.selected_user
            }

        with open('profiles.json', 'w') as f:
                json.dump(profile_data, f, indent=4)

        print(name)
        self.refresh_profiles()

        self.close()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)


    



        


   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileManager()
    window.show()
    sys.exit(app.exec_())


#"""for i in range(3):
    #        profile_button = QPushButton(QIcon(r"C:\Users\Jon\Desktop\Coding\Booru Sort Lite\2bda51ca60cc3b5daaa8e062eb880430.jpg"), "")
  #          profile_button.setIconSize(QSize(100, 100))
  #          profile_button.setFixedSize(100,100)
            
  #          self.layout.addWidget(profile_button, 0, i)
  #          profile_button.clicked.connect(self.open_profile)"""