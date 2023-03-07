from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QPixmap, QIcon

import sys

class window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupdata=[]
        self.setWindowTitle("python-durak")

        Serverbutton=QPushButton("Server")
        Serverbutton.clicked.connect(self.server_setup)
        Clientbutton=QPushButton("Client")
        Clientbutton.clicked.connect(self.client_setup)

        self.layout = QVBoxLayout()
        self.layout.addWidget(Serverbutton)
        self.layout.addWidget(Clientbutton)

        container=QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    
    def server_setup(self):
        import server
        pass

    def client_setup(self):
        self.Name=QLineEdit()
        self.Name.setPlaceholderText("Enter Name")
        name=""
        self.Name.textEdited.connect(self.name_input)
        self.Server=QLineEdit()
        self.Server.setPlaceholderText("Enter Server IP")
        self.Server.textEdited.connect(self.server_input)

        button=QPushButton("Continue")
        button.clicked.connect(self.startClient)



        layout=QVBoxLayout()
        layout.addWidget(self.Name)
        layout.addWidget(self.Server)
        layout.addWidget(button)

        cont=QWidget()
        cont.setLayout(layout)
        self.setCentralWidget(cont)

    def server_input(self,s):
        self.server=s

    def name_input(self, s):
        self.name=s

    def startClient(self):
        print("Name "+self.name)
        print("Server "+self.server)
        self.playercards=QHBoxLayout()
        self.rest=QVBoxLayout()
        self.opps=QHBoxLayout()
        self.table=QGridLayout()

        self.playercards_cont=QWidget()
        self.playercards_cont.setLayout(self.playercards)

        self.opps_cont=QWidget()
        self.opps_cont.setLayout(self.opps)

        self.table_cont=QWidget()
        self.table_cont.setLayout(self.table)

        self.rest_cont=QWidget()
        self.rest.addWidget(self.table_cont)
        self.rest.addWidget(self.opps_cont)
        self.rest_cont.setLayout(self.rest)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.rest_cont)
        self.layout.addWidget(self.playercards_cont)


        self.container=QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.init_game_state(None)

    def init_game_state(self,game_state):
        
        deck=["H6", "H7", "H8", "H9"]
        self.playercards.addWidget(card("H6"))
        self.playercards.addWidget(card("H6"))
        self.playercards.addWidget(card("H6"))

        
           
    def refresh_game_state(self,game_state):
        pass

    

    def refresh_player_state(self, list):
        for i in reversed(range(self.playercards.count())): 
            widgetToRemove = self.playercards.itemAt(i).widget()
            # remove it from the layout list
            self.playercards.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)        
        for i in list:
            self.playercards.addWidget(card(i))


def card(str):
    print("H6")
    layout=QHBoxLayout()
    label=QLabel()
    label.setPixmap(QPixmap('H6.png'))
    #icon=QIcon('H6.jpg')
    #icon=QIcon(pixmap)
    button=QPushButton()
    #button.setGeometry(,100,150,40)
    layout.addWidget(label)
    layout.addWidget(button)

    card=QWidget()
    card.setLayout(layout)
    
    #button.setIcon(icon)

    return card


if __name__=="__main__":
    app=QApplication([])
    q=window()
    q.show()
    app.exec()


