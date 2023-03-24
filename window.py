from PyQt5.QtWidgets import *#QGraphicsScene, QGraphicsSceneMouseEvent,QGraphicsPixmapItem, QLabel, QGraphicsView, QMainWindow, QApplication,QVBoxLayout, QGraphicsItem, QPushButton, QWidget, QHBoxLayout, QLineEdit, QGraphicsSceneDragDropEvent
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtCore
from qasync import QEventLoop

import os

from client import *


def filter1(a,b):
    return a[1]<b[1]


class card(QGraphicsProxyWidget):
    def __init__(self, str, x, y, window):
        super().__init__()
        self.window=window
        self.card=str
        label=QLabel()
        path=os.path.dirname(os.path.abspath(__file__))
        print(path +'/data/H6.jpg')
        pixmap=QPixmap()
        pixmap.load(path +'/data/H6.jpg')
        label.setPixmap(pixmap)
        self.setWidget(label)        
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
 
        #self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.position=(x,y)
        #self.setPos(x,y)
        self.setAcceptDrops(True)
        self.DragMode='att'     #'att': player can drop cards all over the window to attack with them
                                #'def': player needs to drop card on another card
                                #'off': cards are not draggable
        
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:


        if self.DragMode=='att' and self.window.IsInNumbers(self.card):
            print(1)
            self.DragMode='off'
            self.window.acc.append(self.card)
            self.window.playercards.remove(self)
            self.window.playercardsAcc.append(self)
            self.setPos(*self.window.tablePoint)

        elif self.DragMode=='def' and self.window.IsValid(self.scene.itemAt(event.scenePos), self.card):
            print(2)
            self.DragMode=='off'
            self.window.acc.append(self.card, self.itemAt(event.scenePos).card)
            self.window.playercards.remove(self)
        else:
            self.setPos(*self.position)
        print(self.position)
        QGraphicsPixmapItem.mouseReleaseEvent(self, event)
    



    # def dragEnterEvent(self, event):
    #         print("Enter")

    # def dropEvent(self, event):
    #         print("drop")
class cardList(QGraphicsLinearLayout):
    def __init__(self):
        super().__init__(1)
        self.cards=[]
        
    def insert(self, item:card):
        for i, v in enumerate(self.cards):
            if filter1(item.card, v):
                self.cards.insert(i, item.card)#
                cont = QGraphicsWidget()
                cont.setGraphicsItem(item)
                self.insertItem(i, cont)
                return
        cont = QGraphicsWidget()
        cont.setGraphicsItem(item)
        self.cards.append(item.card)
        self.addItem(cont)
        self.activate()
    


class opponent(QWidget):
    def __init__(self, str, num, isSelf=False):
        super().__init__()
        self.isSelf=isSelf
        self.name=str
        self.cards=QLabel(f"cards: {num}")            
        layout=QVBoxLayout()
        if isSelf:       #return Dummy Opponent to indicate players place in order
            self.setStyleSheet("background-color:black")
            layout.addWidget(QLabel('YOU'))
        else:
            layout.addWidget(QLabel(str))
        layout.addWidget(self.cards)
        self.setLayout(layout)

        
        #scaledToWidth(100)

class window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.opps=[]             #! stores the return value of scene.addWidget(x), not x
        self.playercards=cardList()            #! stores the return value of scene.addWidget(x), not x
        self.numbers=[]
        self.table1=cardList()
        self.table2=cardList()

    async def setup(self):

        self.sio=socketio.AsyncClient()
        
        """sio events"""
        ##startup events
        @self.sio.event
        async def connect():
            await self.sio.emit('namechange', self.name)

        @self.sio.event
        def message(txt):
            print(txt)
            #try:    
            self.textOut.setText(self.textOut.text()+'\n'+txt)
            #except:
            #    pass
 
        @self.sio.event
        def trump(string):
            self.player.trump=string
            print("Trump: ",string)
            
        @self.sio.event
        def game_start(players):
            opps=[]
            self.readyButton.deleteLater()
            for i in players:
                if i==self.name:
                    opps.append(opponent(i, 6, True))
                else:
                    opps.append(opponent(i, 6))
            self.displayOpponents(opps)

        @self.sio.event         #!currently unused
        async def request_game_state():
            await self.sio.emit('request_game_state')

        ##UI EVENTs
        @self.sio.event
        def acc_game_state(data):
            print(data)
            self.refresh_game_state(data)

        ##PLAYER EVENTS     (just passed onto players)
        @self.sio.event
        def take(card):
            self.player.take(card)

        @self.sio.event
        async def attack(card):    
            self.playercardsAcc=[]
            self.numbers=card
            self.player.attack(card)
            while self.player.att:               #! fucking disgusting
                valid= await self.sio.call("attacking", self.acc, )
                if not valid:
                    self.player.att=False
                    self.playercards+=self.palyercardsAcc
                else:
                    for i in self.acc:
                        self.player.cards.remove(i)
        @self.sio.event
        def defend(card):
            return self.player.defend(card)

        @self.sio.event
        def schiebt(card):
            return self.player.schiebt(card)

        @self.sio.event
        def finished():
            self.player.finished

    def welcomer(self):
        self.setWindowTitle("python-durak")

        Serverbutton=QPushButton("Server")
        Serverbutton.clicked.connect(self.server_setup)
        Clientbutton=QPushButton("Client")
        Clientbutton.clicked.connect((self.client_setup))

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
        self.Name.textEdited.connect(self.name_input)
        self.Server=QLineEdit()
        self.Server.setPlaceholderText("Enter Server IP")
        self.Server.textEdited.connect(self.server_input)
        self.server=""
        button=QPushButton("Continue")
        button.clicked.connect(self.getValues)


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

    def getValues(self):
        l=QLabel("      Waiting...")
        self.server='http://'+self.server
        self.setCentralWidget(l)
        asyncio.ensure_future(self.startClient())

    async def startClient(self):
        try:
            await self.sio.connect(self.server)
        except socketio.exceptions.ConnectionError:
            self.setCentralWidget(QLabel('      Server Connection failed'))
            await asyncio.sleep(3)
            self.client_setup()
        else:
            print("Name12 "+self.name)
            print("Server "+self.server)


            #Playing scene with movable cards
            self.scene = QGraphicsScene(0,0,800,600)
            self.view=QGraphicsView(self.scene)
            
            
            deck=QGraphicsWidget(layout=self.playercards)
            self.scene.addItem(deck)
            deck.setPos(100,500)

            cont1=(QGraphicsWidget(layout=self.table1))
            self.scene.addItem(cont1)
            cont1.setPos(100,200)

            cont2=(QGraphicsWidget(layout=self.table2))
            self.scene.addItem(cont2)
            cont2.setPos(100,250)

            self.deckPoint=(100,500)
            self.playerPoint=100,50
            self.tablePoint=100, 200



            self.view.setBackgroundBrush((QColor(0,128,0)))
            self.resize(1200,720)

            self.readyButton=QPushButton("Ready?")

            self.readyButton.clicked.connect(self.ready)
            w=self.scene.addWidget(self.readyButton)
            w.setPos(400,300)
            
            
            #console and buttons
            sublayout=QVBoxLayout()

            self.doneButton=QPushButton("Done")
            #self.doneButton.GrayedOut()

            self.quitButton=QPushButton("Quit")
            self.quitButton.clicked.connect(self.quit)
            
            self.concedeButton=QPushButton("Concede")
            #self.concedeButton.GrayedOut()

            self.textOut=QLabel()
            self.textOut.setWordWrap(True)
            

            self.textIn=QLineEdit()
            self.textIn.returnPressed.connect(self.sendMessage)

            sublayout.addWidget(self.quitButton)
            sublayout.addWidget(self.doneButton)
            sublayout.addWidget(self.concedeButton)
            sublayout.addWidget(self.textOut)
            sublayout.addWidget(self.textIn)


            cont=QWidget()
            cont.setLayout(sublayout)

            layout=QHBoxLayout()
            layout.addWidget(self.view)
            layout.addWidget(cont)


            self.widget=QWidget()
            self.widget.setLayout(layout)

            self.setCentralWidget(self.widget)

            self.player=local(self.Name, self)

    #DEPRECIATED
    def init_game_state(self,game_state, cards):
        for i in cards:
            self.scene.addItem(card(i, self.deckPoint[0], self.deckPoint[1]))
            self.deckPoint=(self.deckPoint[0]+50, self.deckPoint[1])
            print("debug")


        
           
    def refresh_game_state(self,game_state):
        # refresh opponents card counter and attacker and defender indication
        for i in self.opps:   
            if game_state["isDone"]["i.name"]!=None:
                self.opps.remove(i)
                i.widget().setStyleSheet("background-color:yellow")
                i.widget().cards.setText('0')
                break
            if game_state["players"][i.name][2]=='att':
                i.widget().setStyleSheet("background-color:blue")          #TODO Make the colors global variables so custom themes can exist
            elif game_state["players"][i.name][2]=='def':
                i.widget().setStyleSheet("background-color:red")
            elif i.isSelf:
                i.widget().setStyleSheet("background-color:black")
            else:
                i.widget().setStyleSheet("background-color:grey")
            i.widget().cards.setText(str(game_state["players"][i.name][1]))
            


    def refresh_player_state(self, list):
        for i in reversed(range(self.playercards.count())): 
            widgetToRemove = self.playercards.itemAt(i).widget()
            # remove it from the layout list
            self.playercards.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)        
        for i in list:
            self.playercards.addWidget(card(i).scaledToWidth(100))

    def ready(self):
        print("ready")
        asyncio.ensure_future(self.sio.emit('sta'))
        print("debug")
        self.readyButton.setText("Waiting:...")
        self.readyButton.clicked.disconnect()
        #self.readyButton.GrayedOut()

    def sendMessage(self):
        asyncio.ensure_future(self.sio.emit('message', self.textIn.text()))
        self.textIn.setText("")

        
    def quit(self):
        #cleanup and exit application
        asyncio.ensure_future(self.sio.disconnect())
        loop.stop()

    def displayOpponents(self, opps):
        n=len(opps)
        for i, opp in enumerate(opps):
            self.opps.append(self.scene.addWidget(opp))
            self.opps[i].setPos(self.playerPoint[0], self.playerPoint[1])
            self.playerPoint=(self.playerPoint[0]+800//n, self.playerPoint[1])
        
    def IsInNumbers(self, str):
        if len(str)!=2:
            raise Exception(f'card corrupted, {str}')
        else:
            for i in self.numbers:
                if i[1]==str[1]:
                    return True
                
    def IsValid(self, item, card):
        if type(item)!=card:
            return False
        else:
            b=item.str
            if b[0]==card[0] and b[1]<card[1]:
                return True
            elif  b[0]!=card[0] and card[0]==self.player.trump[0]:
                return True
            return False


if __name__=="__main__":

    app=QApplication([])

    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    win=window()

    win.show()

    with loop:
        asyncio.ensure_future(win.setup())
        win.welcomer()
        loop.run_forever()
