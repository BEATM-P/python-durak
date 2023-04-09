from PyQt5.QtWidgets import *#QGraphicsScene, QGraphicsSceneMouseEvent,QGraphicsPixmapItem, QLabel, QGraphicsView, QMainWindow, QApplication,QVBoxLayout, QGraphicsItem, QPushButton, QWidget, QHBoxLayout, QLineEdit, QGraphicsSceneDragDropEvent
from PyQt5.QtGui import QPixmap, QColor, QBrush, QPainter, QTransform
from PyQt5 import QtCore
from qasync import QEventLoop
import socketio
import asyncio

import os
from player import player

class local(player):
    
    def __init__(self, name, window):
        self.cards=[]
        self.name=(name)
        self.trump=None
        self.window=window
        self.state='off'

    def take(self,c):
        self.cards+=c
        for i in c:
            #self.window.playercards.insert(card(i, *self.window.deckPoint, self.window))
            self.window.playercards.insert(card(i, self.window))
            # self.window.deckPoint=self.window.deckPoint[0]+50, self.window.deckPoint[1]      
        #print("taking "+(str(card)))

    def attack(self,table):
        ##setup attack
        self.state='att'
        self.window.cardAcc=[]
        self.window.sendButton.setText('Attack')
        self.window.sendButton.clicked.connect((self.sendAttack))
        for i in self.window.playercards.cards:
            i.DragMode='att'
        print("ATTACK")

    def stopAttack(self):
        asyncio.ensure_future(self.window.sio.emit("stop_attack", None))

    def sendAttack(self):
        asyncio.ensure_future(self.goAttack())   

    async def goAttack(self):     
        a=await (self.window.sio.call("attacking", self.window.cardAcc))
        print(a)
        if a==True:
            self.window.cardAcc=[]
        else:
            for i in self.window.cardAcc:
                self.window.table.removeByStr(i)
                self.window.playercards.insert(card(i, self.window))
    
    def schiebt(self,table):
        #window.display(table)
        #return table[0][1]==window.getCard(self.name,self.cards)
        self.window.table.display(table)
        self.state='att'
        self.window.cardAcc=[]
        self.window.sendButton.setText("Schieben")
        self.window.sendButton.clicked.connect((self.sendSchub))
        for i in self.window.playercards.cards:
            i.DragMode='att'
        print("Schub")
    
    def sendSchub(self):
        asyncio.ensure_future(self.goSchub())
        
    
    async def goSchub(self):
        a= await self.window.sio.call("schieben", self.window.cardAcc)
        a=self.window.cardAcc.copy()
        self.window.cardAcc=[]
        if not a:
            for i in a:
                self.window.table.removeByStr(i)
                self.window.playercards.insert(card(i, self.window))
            

    def defend(self):
        self.window.concedeButton.clicked.connect(self.stopDefense)
        self.state='def'
        self.window.cardAcc=[]
        self.window.sendButton.setText("Defend")
        self.window.sendButton.clicked.connect(self.sendDefense)
        for i in self.window.playercards.cards:
            i.DragMode='def'
        print("Defense")
        
    def stopDefense(self):
        asyncio.ensure_future(self.window.sio.emit("stop_defense", None))

    def sendDefense(self):
        asyncio.ensure_future(self.goDefense())

    async def goDefense(self):
        pass;   





def filter1(a,b):
    return a[1]<b[1]


class card(QGraphicsPixmapItem):
    def __init__(self, str, window):
        
        self.window=window
        self.card=str
        label=QLabel()
        path=os.path.dirname(os.path.abspath(__file__))
        print(path +'/data/H6.jpg')
        pixmap=QPixmap()
        pixmap.load(path +'/data/H6.jpg')
        super().__init__(pixmap.scaledToWidth(100))        
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
    
        #self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        #self.position=(x,y)
        #self.setPos(x,y)
        self.setAcceptDrops(False)
        self.DragMode='off'     #'att': player can drop cards all over the window to attack with them
                                #'def': player needs to drop card on another card
                                #'off': cards are not draggable
    def setPos(self, x,y):
        super().setPos(x,y)
        self.position=x,y

    def fakecard(str):
        rect=QGraphicsRectItem(0,0,100,200)
        rect.setAcceptDrops(True)
        rect.card=str
        #rect.setBrush(QColor.grey)
        rect.setVisible(False)
        return rect

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        if self.DragMode=='att':
            #for i in self.window.table.cardrow2:
                #print(type(i))
                #if type(i)==QGraphicsRectItem:
            self.window.attackIndicator.setVisible(True)
        elif self.DragMode=='def':
            for i in self.window.table.cardrow2:
                i.setVisible(True)
        QGraphicsPixmapItem.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print(self.DragMode=='def', self.window.IsValidDefense(self.window.scene.itemAt(event.lastScenePos(), QTransform()), self.card))
        
        if self.DragMode=='att' and self.window.IsInNumbers(self.card) and event.lastScenePos().y()<400:
            self.DragMode='off'
            self.window.cardAcc.append(self.card)
            self.window.playercards.remove(self)
            self.window.table.insert(self)
            self.window.numbers.append(self.card)
            #self.window.player.sendAttack()
            self.window.sendButton.click()
            print(event.lastScenePos(), self.DragMode)
            print(f"Attacking with card {self.card}")

        
        else: 
            self.setPos(*self.position)
            print(self.position, self.DragMode)
        if self.DragMode=='def' and self.window.IsValidDefense(self.window.scene.itemAt(event.lastScenePos(), QTransform()), self.card)==True:
            print("debug")

            self.DragMode=='off'

            fakecard=self.window.scene.itemAt(event.lastScenePos(), QTransform())

            print("debug2")
            self.window.cardAcc.append(fakecard.card)
            self.window.cardAcc.append(self.card)

            print("debug3")


            self.window.playercards.remove(self)
            self.window.table.cardrow2[self.window.table.cardrow2.index(fakecard)]=card(self.card, self.window)
            self.window.table.refresh()

            #self.window.sendButton.click()
            print(f"defending {fakecard.card} with {self.card}")
            for i in self.window.table.cardrow2:
                if type(i)==QGraphicsRectItem:
                    i.setVisible(False)            #CLEANUP

        elif self.DragMode=='att':
            self.window.attackIndicator.setVisible(False)
        #DEBUG INFO

        print(self.DragMode=='def', self.window.IsValidDefense(self.window.scene.itemAt(event.lastScenePos(), QTransform()), self.card))
        print(self.window.scene.itemAt(event.lastScenePos(), QTransform()))
        print(f"Moved {self.card}")
        
        QGraphicsPixmapItem.mouseReleaseEvent(self, event)
    



    # def dragEnterEvent(self, event):
    #         print("Enter")

    # def dropEvent(self, event):
    #         print("drop")
class cardList():
    def __init__(self, x, y, window):
        self.cards=[]
        self.pos=x,y
        self.window=window

    def insert(self, item:card):
        for i, v in enumerate(self.cards):
            if filter1(item.card, v.card):
                self.window.scene.addItem(item)
                self.cards.insert(i, item)
                self.refresh()
                return
        self.window.scene.addItem(item)
        self.cards.append(item)
        self.refresh()

    def remove(self, item:card):
        self.cards.remove(item)
        self.window.scene.removeItem(item)
        self.refresh()

    def refresh(self):
        for i, v in enumerate(self.cards):
            v.setPos(self.pos[0]+ (600/len(self.cards)*i), self.pos[1])
            v.setZValue(len(self.cards)-i)

    def clear(self):
        for v in self.cards:
            self.window.scene.removeItem(v)

class table():
    def __init__(self,x,y, window):
        self.pos=x,y
        self.window=window
        self.active_cards=[]
        self.cardrow1=[]
        self.cardrow2=[]

    def activeByStr(self):
        res=[]
        for i in self.cardrow1:
            res.append(i.card)
        return res

    def insert(self, item:card):
        for i, v in enumerate(self.cardrow1):
            if filter1(item.card, v.card):
                self.window.scene.addItem(item)
                self.cardrow1.insert(i, item)
                f=card.fakecard(item.card)
                self.cardrow2.insert(i, f)
                self.window.scene.addItem(f)
                self.refresh()
                return
        self.window.scene.addItem(item)
        self.cardrow1.append(item)
        f=card.fakecard(item.card)
        self.cardrow2.append(f)
        self.window.scene.addItem(f)
        self.refresh()
        
    def removeByStr(self, item:str):
        for i in self.cardrow1:
            if i.card==item:
                self.window.scene.removeItem(i)
                self.cardrow1.remove(i)
                return
        
    def display(self, cards):
        acc=False
        for str in cards:
            acc=False
            for i, c in enumerate(self.cardrow1):
                
                if c.card ==str:
                    acc=True
            if not acc:
                self.insert(card(str, self.window))
        self.refresh()

    def addDefense(self, cards):
        pass


    def refresh(self):
        for i, v in enumerate(self.cardrow1):
            pos=self.pos[0]+ (600/len(self.cardrow1)*i), self.pos[1]
            v.setPos(*pos)
            self.cardrow2[i].setPos(pos[0],pos[1]+10)


    def clear(self):
        for v in self.cardrow1:
            self.window.scene.removeItem(v)
        for v in self.cardrow2:
            self.window.scene.removeItem(v)

class stack(QGraphicsProxyWidget):
    def __init__(self):
        super().__init__()
        
        cont=QWidget()
        layout=QHBoxLayout()
        self.number=QLabel()
        self.trump=QLabel()
        layout.addWidget(self.trump)
        layout.addWidget(self.number)
        cont.setLayout(layout)
        self.setWidget(cont)
    
    def setTrump(self, str):        #TODO
        pass

    def refresh(self,n):
        if n==0:
            self.deleteLater()
            return
        self.number.setText(f'Cards left: {n}')


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
        self.playercards=cardList(100, 500, self)            #! stores the return value of scene.addWidget(x), not x
        self.numbers=[]
        self.table=table(100,200, self)
        self.stack=stack()


    async def setup(self):

        self.sio=socketio.AsyncClient(logger=True)
        
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
        def changed_game_state(data):
            print(data)
            self.refresh_game_state(data)

        ##PLAYER EVENTS     (just passed onto players)
        @self.sio.event
        def take(card):
            self.player.take(card)

        @self.sio.event
        def attack(data):    
            self.numbers=data
            print("debug")
            self.player.attack(data) 

            # while self.player.att:               #! fucking disgusting
            #     valid= await self.sio.call("attacking", self.acc, )
            #     if not valid:
            #         self.player.att=False
            #         self.playercards+=self.palyercardsAcc
            #     else:
            #         for i in self.acc:
            #             self.player.cards.remove(i)
        @self.sio.event
        def defend():
            self.player.defend()

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
            
            self.scene.addItem(self.stack)
            self.stack.setPos(750, 300)
            
            # deck=QGraphicsWidget(layout=self.playercards)
            # self.scene.addItem(deck)
            # deck.setPos(100,500)

            # cont1=(QGraphicsWidget(layout=self.table1))
            # self.scene.addItem(cont1)
            # cont1.setPos(100,200)

            # cont2=(QGraphicsWidget(layout=self.table2))
            # self.scene.addItem(cont2)
            # cont2.setPos(100,250)

            self.deckPoint=(100,500)
            
            self.playerPoint=100,50
            # self.tablePoint=100, 200

            self.attackIndicator=QGraphicsRectItem(0,0,800,400)
            self.scene.addItem(self.attackIndicator)
            self.attackIndicator.setVisible(False)

            self.view.setBackgroundBrush((QColor(0,128,0)))
            self.resize(1200,720)

            self.readyButton=QPushButton("Ready?")

            self.readyButton.clicked.connect(self.ready)
            w=self.scene.addWidget(self.readyButton)
            w.setPos(400,300)
            
            
            #console and buttons
            sublayout=QVBoxLayout()

            self.sendButton=QPushButton("Attack")
            #self.sendButton.GrayedOut()

            self.quitButton=QPushButton("Quit")
            self.quitButton.clicked.connect(self.quit)
            
            self.concedeButton=QPushButton("Concede")
            #self.concedeButton.GrayedOut()

            self.textOut=QLabel()
            self.textOut.setWordWrap(True)
            

            self.textIn=QLineEdit()
            self.textIn.returnPressed.connect(self.sendMessage)

            sublayout.addWidget(self.quitButton)
            sublayout.addWidget(self.sendButton)
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


        
           
    def refresh_game_state(self,game_state):    #See Documentation for structure of game_state data
        # refresh opponents card counter and attacker and defender indication
        for i in self.opps:   
            try:
                game_state["players"][i.widget().name]==None
            except:
                self.opps.remove(i)
                i.widget().setStyleSheet("background-color:yellow")
                i.widget().cards.setText('0')
                break
            if game_state["players"][i.widget().name][2]=='att':
                if i.widget().name==self.player.name:
                    self.player.state='att'
                i.widget().setStyleSheet("background-color:blue")          #TODO Make the colors global variables so custom themes can exist
            elif game_state["players"][i.widget().name][2]=='def':
                if i.widget().name==self.player.name:
                    self.player.state='def'
                i.widget().setStyleSheet("background-color:red")
            else:
                i.widget().setStyleSheet("background-color:grey")
            i.widget().cards.setText(str(game_state["players"][i.widget().name][0]))

        #refresh table
        self.table.display(game_state["table"][0])
        self.table.addDefense(game_state["table"][1])
        if self.player.state!='att':
            self.numbers=game_state['numbers']
        else:
            self.numbers+=game_state['numbers']

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
        self.loop.stop()

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
            if self.numbers==[]:            #! fucks up the if check in card.mouseReleaseEvent
                return True
            for i in self.numbers:
                if i[1]==str[1]:
                    return True
                
    def IsValidDefense(self, item, c)-> bool:
        if type(item)!=QGraphicsRectItem:
            print(f"item type:  {type(item)}")
            return False
        else:
            print(f"item card: {item.card}, played card: {c}")
            b=item.card
            if b[0]==c[0] and b[1]<c[1]:
                return True
            elif  b[0]!=c[0] and c[0]==self.player.trump[0]:
                return True
            return False

    def exec(self):

        self.loop = QEventLoop(app)

        asyncio.set_event_loop(self.loop)

        with self.loop:
            asyncio.ensure_future(win.setup())
            win.welcomer()
            self.loop.run_forever()


if __name__=="__main__":
    app=QApplication([])
    win=window()
    win.show()
    win.exec()

    