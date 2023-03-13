from PyQt5.QtWidgets import QGraphicsScene, QLabel, QGraphicsView, QMainWindow, QApplication,QVBoxLayout, QGraphicsItem, QPushButton, QWidget, QHBoxLayout, QLineEdit, QGraphicsSceneDragDropEvent
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtCore
import os
from GlobalObject import GlobalObject

from client import *


class card(QPixmap):
    def __init__(self, str, x, y):
        super().__init__()
        path=os.path.dirname(os.path.abspath(__file__))
        print(path +'/data/H6.jpg')
        self.load(path +'/data/H6.jpg')
        self.pos=(x, y)         # not working for some reason


class opponent(QWidget):
    def __init__(self, str, num):
        super().__init__()
        layout=QVBoxLayout()
        layout.addWidget(QLabel(str))
        layout.addWidget(QLabel(f"cards: {num}"))
        self.setLayout(layout)
        #scaledToWidth(100)

class window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.players=[]
        self.cards=[]

        self.client=client()


        self.setWindowTitle("python-durak")

        Serverbutton=QPushButton("Server")
        Serverbutton.clicked.connect(self.server_setup)
        Clientbutton=QPushButton("Client")
        Clientbutton.clicked.connect(asyncio.run(self.client_setup()))

        self.layout = QVBoxLayout()
        self.layout.addWidget(Serverbutton)
        self.layout.addWidget(Clientbutton)

        container=QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def server_setup(self):
        import server
        pass

    async def client_setup(self):
        self.Name=QLineEdit()
        self.Name.setPlaceholderText("Enter Name")
        self.Name.textEdited.connect(self.name_input)
        self.Server=QLineEdit()
        self.Server.setPlaceholderText("Enter Server IP")
        self.Server.textEdited.connect(self.server_input)

        button=QPushButton("Continue")
        button.clicked.connect(await self.getValues())


        layout=QVBoxLayout()
        layout.addWidget(self.Name)
        layout.addWidget(self.Server)
        layout.addWidget(button)

        cont=QWidget()
        cont.setLayout(layout)
        self.setCentralWidget(cont)


    def server_input(self,s):
        self.client.server=s

    def name_input(self, s):
        self.client.name=s

    async def getValues(self):
        l=QLabel("      Waiting...")
        self.setCentralWidget(l)
        await self.client.setup()
        await self.client.sio.emit('sta')
        self.startClient()        

    def startClient(self):
        print("Name12 "+self.name)
        print("Server "+self.server)
        self.scene = QGraphicsScene(0,0,800,600)
        self.view=QGraphicsView(self.scene)
        self.deckPoint=(100,500)
        self.playerPoint=100,50
        self.view.setBackgroundBrush((QColor(0,128,0)))
        self.resize(1024,720)
        self.setCentralWidget(self.view)
        while True:
            pass
    
    def init_game_state(self,game_state, cards):
        for i in cards:
            c=self.scene.addPixmap(card(i, self.deckPoint[0], self.deckPoint[1]).scaledToWidth(100))
            c.setPos(self.deckPoint[0], self.deckPoint[1])
            self.deckPoint=(self.deckPoint[0]+50, self.deckPoint[1])
            c.setFlag(QGraphicsItem.ItemIsMovable)
            print("debug")
    

        
           
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
            self.playercards.addWidget(card(i).scaledToWidth(100))




app=QApplication([])

win=window()

win.show()

asyncio.run(app.exec())


#l=card('H6', 100, 450).scaledToWidth(100)
#c=scene.addPixmap(l)
#c.setPos(100,450)
#c.setFlag(QGraphicsItem.ItemIsMovable)

#opp=opponent('test', 5)
#o=scene.addWidget(opp)
#o.setPos(25,25)



#view.setBackgroundBrush((QColor(0,128,0)))#

#view.show()
#app.exec()











# from PyQt6.QtCore import QSize, Qt
# from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
# from PyQt6.QtGui import QPixmap, QIcon

# import sys

# class window(QMainWindow):
#     def __init__(self) -> None:
#         super().__init__()
#         self.setupdata=[]
#         self.setWindowTitle("python-durak")

#         Serverbutton=QPushButton("Server")
#         Serverbutton.clicked.connect(self.server_setup)
#         Clientbutton=QPushButton("Client")
#         Clientbutton.clicked.connect(self.client_setup)

#         self.layout = QVBoxLayout()
#         self.layout.addWidget(Serverbutton)
#         self.layout.addWidget(Clientbutton)

#         container=QWidget()
#         container.setLayout(self.layout)
#         self.setCentralWidget(container)

    
#     def server_setup(self):
#         import server
#         pass

#     def client_setup(self):
#         self.Name=QLineEdit()
#         self.Name.setPlaceholderText("Enter Name")
#         name=""
#         self.Name.textEdited.connect(self.name_input)
#         self.Server=QLineEdit()
#         self.Server.setPlaceholderText("Enter Server IP")
#         self.Server.textEdited.connect(self.server_input)

#         button=QPushButton("Continue")
#         button.clicked.connect(self.startClient)



#         layout=QVBoxLayout()
#         layout.addWidget(self.Name)
#         layout.addWidget(self.Server)
#         layout.addWidget(button)

#         cont=QWidget()
#         cont.setLayout(layout)
#         self.setCentralWidget(cont)

#     def server_input(self,s):
#         self.server=s

#     def name_input(self, s):
#         self.name=s

#     def startClient(self):
#         print("Name "+self.name)
#         print("Server "+self.server)
#         self.playercards=QHBoxLayout()
#         self.rest=QVBoxLayout()
#         self.opps=QHBoxLayout()
#         self.table=QGridLayout()

#         self.playercards_cont=QWidget()
#         self.playercards_cont.setLayout(self.playercards)

#         self.opps_cont=QWidget()
#         self.opps_cont.setLayout(self.opps)

#         self.table_cont=QWidget()
#         self.table_cont.setLayout(self.table)

#         self.rest_cont=QWidget()
#         self.rest.addWidget(self.table_cont)
#         self.rest.addWidget(self.opps_cont)
#         self.rest_cont.setLayout(self.rest)


#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.rest_cont)
#         self.layout.addWidget(self.playercards_cont)


#         self.container=QWidget()
#         self.container.setLayout(self.layout)
#         self.setCentralWidget(self.container)
#         self.init_game_state(None)

#     def init_game_state(self,game_state):
        
#         deck=["H6", "H7", "H8", "H9"]
#         self.playercards.addWidget(card("H6"))
#         self.playercards.addWidget(card("H6"))
#         self.playercards.addWidget(card("H6"))

        
           
#     def refresh_game_state(self,game_state):
#         pass

    

#     def refresh_player_state(self, list):
#         for i in reversed(range(self.playercards.count())): 
#             widgetToRemove = self.playercards.itemAt(i).widget()
#             # remove it from the layout list
#             self.playercards.removeWidget(widgetToRemove)
#             # remove it from the gui
#             widgetToRemove.setParent(None)        
#         for i in list:
#             self.playercards.addWidget(card(i))


# def card(str):
#     print("H6")
#     layout=QHBoxLayout()
#     label=QLabel()
#     label.setPixmap(QPixmap('H6.png'))
#     #icon=QIcon('H6.jpg')
#     #icon=QIcon(pixmap)
#     button=QPushButton()
#     #button.setGeometry(,100,150,40)
#     layout.addWidget(label)
#     layout.addWidget(button)

#     card=QWidget()
#     card.setLayout(layout)
    
#     #button.setIcon(icon)

#     return card


# if __name__=="__main__":
#     app=QApplication([])
#     q=window()
#     q.show()
#     app.exec()


