from PyQt5.QtWidgets import QLabel

class TagListManager():
    def __init__(self, tag_list_area):

        self.tag_list_area = tag_list_area
        self.add_image_to_area()
        
    def add_image_to_area(self):

        for i in range(6):
                    print('workin?')
                    label = QLabel("Hey nigga")
                    label.setStyleSheet("color: white; font-size: 50px; background-color: black;")
                    self.tag_list_area.layout().addWidget(label)
               
         

   

