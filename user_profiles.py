from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QDialog,
    QLabel, QLineEdit, QApplication, QMenu, QAction, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import json

class CreateProfileDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("users")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        label = QLabel("new user:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("e.g., miku")
        self.input.setFont(QFont("Arial", 12))
        layout.addWidget(label)
        layout.addWidget(self.input)

        button_layout = QHBoxLayout()
        create_btn = QPushButton("create")
        cancel_btn = QPushButton("cancel")
        create_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_name(self):
        return self.input.text().strip()

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

    def get_confirmation(self):
        return self.result() == QDialog.Accepted

class ProfileManager(QWidget):
    def __init__(self):
        super().__init__()

        self.data_file = "users.json"
        self.selected_data = {"selected_user": None}

        self.setWindowTitle("users")
        self.setFixedSize(600, 400)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.profile_buttons = []
        self.load_profiles()

    def load_profiles(self):
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                names = data.get("users", [])
                self.selected_data["selected_user"] = data.get("selected_user")

                for name in names:
                    self.add_profile_button(name, save=False)

                if self.selected_data["selected_user"] is None and names:
                    self.selected_data["selected_user"] = names[0]
                    print("No selected user found. Defaulting to first profile:", self.selected_data["selected_user"])

                if self.selected_data["selected_user"]:
                    print("Loaded selected user:", self.selected_data["selected_user"])
        except (FileNotFoundError, json.JSONDecodeError):
            pass 

        self.add_create_button()
        
    def save_profiles(self):
        names = [btn.text() for btn in self.profile_buttons if btn.text() != "+"]
        data = {
            "users": names,
            "selected_user": self.selected_data.get("selected_user")
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_create_button(self):
        if any(btn.text() == "+" for btn in self.profile_buttons):
            return

        add_btn = QPushButton("+")
        add_btn.setFixedSize(100, 100)
        add_btn.setStyleSheet("""
            QPushButton {
                font-size: 36px;
                background-color: #444;
                color: white;
                border: 2px solid #888;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        
        add_btn.clicked.connect(self.show_create_dialog)
        self.layout.addWidget(add_btn, len(self.profile_buttons) // 4, len(self.profile_buttons) % 4)
        self.profile_buttons.append(add_btn)

    def show_create_dialog(self):
        dialog = CreateProfileDialog()
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.get_name()
            if name:
                self.add_profile_button(name)

    def on_profile_clicked(self, name):
        self.selected_data["selected_user"] = name
        print("Selected user:", name)
        self.save_profiles()

    def on_profile_right_click(self, name):
       
        delete_dialog = DeleteProfileDialog(name)
        if delete_dialog.exec_() == QDialog.Accepted:
            self.delete_profile(name)

    def delete_profile(self, name):
       
        names = [btn.text() for btn in self.profile_buttons if btn.text() not in [name, "+"]]
   
        if self.selected_data["selected_user"] == name:
            self.selected_data["selected_user"] = names[0] if names else None

     
        data = {
            "users": names,
            "selected_user": self.selected_data["selected_user"]
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

        for btn in self.profile_buttons:
            self.layout.removeWidget(btn)
            btn.setParent(None)
        self.profile_buttons.clear()

      
        for name in names:
            self.add_profile_button(name, save=False)

        self.add_create_button()


    def add_profile_button(self, name, save=True):
        
        if self.profile_buttons and self.profile_buttons[-1].text() == "+":
            plus_button = self.profile_buttons.pop()
            self.layout.removeWidget(plus_button)
            plus_button.setParent(None)

        row = len(self.profile_buttons) // 4
        col = len(self.profile_buttons) % 4

        profile_btn = QPushButton(name)
        profile_btn.setFixedSize(100, 150)
        profile_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #222;
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        profile_btn.clicked.connect(lambda _, n=name: self.on_profile_clicked(n))
        
        profile_btn.setContextMenuPolicy(Qt.CustomContextMenu)
        profile_btn.customContextMenuRequested.connect(lambda _, n=name: self.on_profile_right_click(n))

        self.layout.addWidget(profile_btn, row, col)
        self.profile_buttons.append(profile_btn)

        if save:
            self.save_profiles()

        self.add_create_button()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfileManager()
    window.show()
    sys.exit(app.exec_())
