from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication, QHBoxLayout

import json
import os

class ImportEntities():
    def __init__(self, main_area_layout=None):
   

        self.main_area_layout = main_area_layout



    def import_entity_box(self, tag_name):

        self.tag_name = tag_name
        

        print(tag_name)
        
        import_area_widget = QWidget()
        import_area_widget.setStyleSheet("background-color: white;")
        import_area_widget.setMinimumWidth(200)
      

        import_area_widget_layout = QHBoxLayout(import_area_widget)

        import_area_box = QWidget()
        import_area_box.setFixedHeight(500)
        import_area_box.setFixedWidth(700)
        import_area_box.setStyleSheet("background-color: red;")
        import_area_box.setAcceptDrops(True)  
        import_area_widget_layout.addWidget(import_area_box)

        import_area_box_layout = QHBoxLayout(import_area_box)

        tag_label = QLabel(f'add to {tag_name}')
        tag_label.setFixedWidth(200)
        tag_label.setFixedHeight(50)
        tag_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

        import_area_box_layout.addWidget(tag_label)

        import_area_box.dragEnterEvent = self.dragEnterEvent
        import_area_box.dropEvent = self.dropEvent

        self.main_area_layout.addWidget(import_area_widget)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
           
            valid_files = [url for url in urls if self.is_image_or_video(url)]
            if valid_files: 
                event.acceptProposedAction()
            else:
                event.ignore()  
        else:
            event.ignore() 
  

    def is_image_or_video(self, url: QUrl) -> bool:
      
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
        
        file_path = url.toLocalFile()
        if file_path:
        
            file_extension = file_path.split('.')[-1].lower()
            if f'.{file_extension}' in image_extensions or f'.{file_extension}' in video_extensions:
                return True
        return False
    
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
      
            valid_files = [url for url in urls if self.is_image_or_video(url)]
            if valid_files:


                with open('profiles.json', 'r') as f:
                    selected_user = json.load(f)
                    self.current_user = selected_user["selected user"]

                    self.nested_directory = f"profiles/{self.current_user}"

                    os.makedirs(self.nested_directory, exist_ok=True)
                    print(f'current user: {self.current_user}')

                try:
                    self.new_tag_path = os.path.join(self.nested_directory, f'{self.tag_name}.json')

                    with open(self.new_tag_path, 'r') as f:
                        tag_data = json.load(f)

                        self.tag_list = tag_data


                        print(self.tag_list)
                except FileNotFoundError:
                    print('no json yet')
       

                for url in valid_files:
                    file_path = url.toLocalFile()
                    
                    file_name = os.path.basename(file_path)  # Extract the file name from the path
                    self.tag_list[file_name] = file_path 

                with open(self.new_tag_path, 'w') as f:
                    json.dump(self.tag_list, f, indent=4)


                event.acceptProposedAction()
            else:
                event.ignore() 
        else:
            event.ignore()

    
