from PyQt5.QtWidgets import *#QGraphicsScene, QGraphicsSceneMouseEvent,QGraphicsPixmapItem, QLabel, QGraphicsView, QMainWindow, QApplication,QVBoxLayout, QGraphicsItem, QPushButton, QWidget, QHBoxLayout, QLineEdit, QGraphicsSceneDragDropEvent
from PyQt5.QtGui import QPixmap, QColor, QBrush, QPainter, QTransform
from PyQt5 import QtCore
from qasync import QEventLoop
import socketio
import asyncio
import sys
import os

from player import player
import logic


settings={"dbg": True,"deck":9, "trump":1}



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
        #self.window.sendButton.setText('Attack')
        #self.window.sendButton.clicked.connect((self.sendAttack))
        self.window.concedeButton.clicked.connect(self.stopAttack)
        for i in self.window.playercards.cards:
            i.DragMode='att'
        print("ATTACK")

    def stopAttack(self):
        asyncio.ensure_future(self.window.sio.emit("stop_attack", None))

    def sendAttack(self, Acc):
        asyncio.ensure_future(self.goAttack(Acc))   

    async def goAttack(self, Acc):     
        a=await (self.window.sio.call("attacking", Acc))
        if settings["dbg"]:
            print(a)
        if not a:
            for i in Acc:
                self.window.table.removeByStr(i)
                self.window.playercards.insert(card(i, self.window))


    def schiebt(self,table):
        #window.display(table)
        #return table[0][1]==window.getCard(self.name,self.c              ards)
        self.window.cardAcc=[]
        self.window.table.display(table)
        self.state='sch'
        print("Schub")
        self.defend()
        
    
    def sendSchub(self, Acc):
        #Acc=self.window.cardAcc.copy()
        #self.window.cardAcc=[]
        if settings['dbg']:
            print(f'Emmiting Schieben with {Acc}')
        asyncio.ensure_future(self.goSchub(Acc))        #!! BROKEN
        
    
    async def goSchub(self, Acc):
        a= await self.window.sio.call("schieben", Acc)
        if not a:   
            for i in Acc:
                self.window.table.removeByStr(i)
                self.window.playercards.insert(card(i, self.window, 'att'))
            

    def defend(self):
        if self.state!='sch':
            self.state='def'
        if settings['dbg']:
            print(f'self.state {self.state}')
        self.window.table.initDefense()
        self.window.cardAcc=[]
        self.window.concedeButton.clicked.connect(self.stopDefense)
        # self.window.sendButton.setText("Defend")
        # self.window.sendButton.clicked.connect(self.sendDefense)
        for i in self.window.playercards.cards:
            i.DragMode='def'
        print("Defense")
        
    def stopDefense(self):
        if self.state=="sch":
            asyncio.ensure_future(self.goSchub([]))
        asyncio.ensure_future(self.window.sio.emit("stop_defense", None))

    def sendDefense(self, Acc):
        asyncio.ensure_future(self.goDefense(Acc))

    async def goDefense(self, Acc):
        b=await self.window.sio.call("defending", Acc);   
        if b:
           #TODO
           self.window.cardAcc=[] 




def filter1(a,b):
    return a[1]<b[1]



class card(QGraphicsPixmapItem):
    def __init__(self, str, window, dragMode='off'):
        
        self.window=window
        self.card=str
        label=QLabel()
        path=os.path.dirname(os.path.abspath(__file__))
        print(f"{path}/data/{self.card}.jpg")
        pixmap=QPixmap()
        pixmap.load(f"{path}/data/{self.card}.png")
        super().__init__(pixmap.scaledToWidth(100))        
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

        self.setAcceptDrops(False)
        self.DragMode='off'                         
        #'att': player can drop cards all over the window to attack with them
        #'def': player needs to drop card on another card
        #'off': cards are not draggable
        self.dropIndicator=None                                                 
    
   

    def setPos(self, x,y):
        super().setPos(x,y)
        self.position=x,y
        if self.dropIndicator:
            self.dropIndicator.setPos(x,y+30)

    def setZValue(self, z: float) -> None:
        if self.dropIndicator:
            self.dropIndicator.setZValue(z+1)
        return super().setZValue(z)

    def addDrop(self, item):
        if not self.dropIndicator:
            self.dropIndicator=item
            self.window.scene.addItem(self.dropIndicator)
            self.dropIndicator.setPos(self.position[0]+10, self.position[1])    

    


    def showDropIndicator(self):
        if self.dropIndicator==None:
            pass
        
    def fakecard(str):
        rect=QGraphicsRectItem(0,0,100,200)
        rect.setAcceptDrops(True)
        rect.card=str
        #rect.setBrush(QColor.grey)
        rect.setVisible(False)
        return rect

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        if self.DragMode=='att' or self.window.player.state=='sch':
            #for i in self.window.table.cardrow2:
                #print(type(i))
                #if type(i)==QGraphicsRectItem:
            self.window.attackIndicator.setVisible(True)
        if self.DragMode=='def':
            for i in self.window.table.cardrow:
                i.showDropIndicator()
        QGraphicsPixmapItem.mousePressEvent(self, event)


    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if settings["dbg"]:
            print(self.DragMode=='def', logic.checks.ClientIsValidDefense(self.window.scene.itemAt(event.lastScenePos(), QTransform()), self.card, self.window.player.trump))
        
        if self.DragMode=='att' and logic.checks.IsInNumbers(self.card, self.window.numbers) and event.lastScenePos().y()<400:
            self.DragMode='off'
            #self.window.cardAcc.append(self.card)
            self.window.playercards.remove(self)
            self.window.table.insert(self)
            self.window.numbers.append(self.card)
            self.window.player.sendAttack([self.card])
            #self.window.sendButton.click()
            
            if settings["dbg"]:
                print(event.lastScenePos(), self.DragMode)
                print(f"Attacking with card {self.card}")

        
        else:                   #NEEDS TO BE EXECED BEFORE THE IsValidDefense Check
            self.setPos(*self.position)
            if settings["dbg"]:
                print(self.position, self.DragMode)
        
        if self.DragMode=='def' and event.lastScenePos().y()<400 and logic.checks.ClientIsValidDefense(self.window.scene.itemAt(event.lastScenePos(), QTransform()), self.card, self.window.player.trump)==True:          
            
            self.DragMode=='off'
            if settings["dbg"]:
                print(f'player.state {self.window.player.state}')
            if self.window.player.state=='sch':
                #self.window.cardAcc=[]
                self.window.player.sendSchub([])
                self.window.player.state='def'
            fakecard=self.window.scene.itemAt(event.lastScenePos(), QTransform())
            if fakecard.DragMode=="drp":
            
            #self.window.cardAcc.append(fakecard.card)
            #self.window.cardAcc.append(self.card)
                self.window.playercards.remove(self)
                self.window.table.addDefense(fakecard.card, self.card)
                self.window.table.refresh()
                self.window.player.sendDefense([fakecard.card, self.card])
            #self.window.sendButton.click()
            if settings["dbg"]:
                print(f"cardacc: {self.window.cardAcc}")
                print(f"defending {fakecard.card} with {self.card}")
            
        elif self.DragMode=='def' and self.window.player.state=='sch' and logic.checks.IsInNumbers(self.card, self.window.numbers) and event.lastScenePos().y()<400:
            #self.window.cardAcc.append(self.card)
            self.window.playercards.remove(self)
            self.window.table.insert(self)
            self.window.numbers.append(self.card)
            self.window.player.sendSchub([self.card])
                               #CLEANUP
        if self.DragMode=='att' or self.window.player.state=='sch':
            self.window.attackIndicator.setVisible(False)
        
        
        #DEBUG INFO

        # print(self.DragMode=='def', self.window.IsValidDefense(self.window.scene.itemAt(event.lastScenePos(), QTransform()), self.card))
        # print(self.window.scene.itemAt(event.lastScenePos(), QTransform()))
        # print(f"Moved {self.card}")
        
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
            if v.dropIndicator:
                self.window.scene.removeItem(v.dropIndicator)
            self.window.scene.removeItem(v)

class table():
    def __init__(self,x,y, window):
        self.pos=x,y
        self.window=window
        self.active_cards=[]
        self.cardrow=[]

    def activeByStr(self):
        res=[]
        for i in self.cardrow:
            res.append(i.card)
        return res

    def insert(self, item:card):
        for i, v in enumerate(self.cardrow):
            if filter1(item.card, v.card):
                self.window.scene.addItem(item)
                self.cardrow.insert(i, item)
                self.refresh()
                return
        self.window.scene.addItem(item)
        self.cardrow.append(item)
        self.refresh()
        
    def removeByStr(self, item:str):
        for i in self.cardrow:
            if i.card==item:
                self.window.scene.removeItem(i)
                self.cardrow.remove(i)
                return
        
    def display(self, cards):
        acc=False
        for str in cards:
            acc=False
            for i, c in enumerate(self.cardrow):
                
                if c.card ==str:
                    acc=True
            if not acc:
                self.insert(card(str, self.window, "drp"))
        self.refresh()

    def addDefense(self, c1, c2):
        for i in (self.cardrow):
            if i.card==c1:
                i.addDrop(card(c2, self.window, 'off'))
        self.refresh()

    def initDefense(self):
        for i in self.cardrow:
            i.DragMode=="drp"


    def refresh(self):
        for i, v in enumerate(self.cardrow):
            pos=self.pos[0]+ (600/len(self.cardrow)*i), self.pos[1]
            v.setPos(*pos)
            v.setZValue(len(self.cardrow)-i)


    def clear(self):
        for v in self.cardrow:
            if v.dropIndicator:
                self.window.scene.removeItem(v.dropIndicator)
                v.dropIndicator=None
            self.window.scene.removeItem(v)
        self.cardrow=[]
        self.window.player.state='off'

        

class stack(QGraphicsProxyWidget):
    def __init__(self):
        super().__init__()
        
        cont=QWidget()
        layout=QVBoxLayout()
        self.number=QLabel()
        self.trump=QLabel()
        layout.addWidget(self.trump)
        layout.addWidget(self.number)
        cont.setLayout(layout)
        self.setWidget(cont)
    
    def setTrump(self, str):
        c=card(str,None)
        print(f"setting trump as {str}")
        self.trump.setPixmap(c.pixmap().scaledToWidth(75))


    def refresh(self,n):
        if n==0:
            self.deleteLater()
            return
        self.number.setText(f'Cards left: {n}')

#TEst ing github
class opponent(QGraphicsProxyWidget):
    def __init__(self, sid, str ,num=0, isSelf=False):
        super().__init__()
        self.sid=sid
        self.isSelf=isSelf
        self.name=str
        self.cards=QLabel(f"cards: {num}")            
        layout=QVBoxLayout()
        cont=QWidget()
        if isSelf:       #return Dummy Opponent to indicate players place in order
            cont.setStyleSheet("background-color:black")
            layout.addWidget(QLabel('YOU'))
        else:
            layout.addWidget(QLabel(str))
        layout.addWidget(self.cards)
        cont.setLayout(layout)
        self.setWidget(cont)
        
        #scaledToWidth(100)


#https://www.geeksforgeeks.org/pyqt5-scrollable-label/
class chat(QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)
        #self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)


        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        #used to scroll down to screen automatically
        self.fakelabel=QLabel()
        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)
        lay.addWidget(self.fakelabel)
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
        self.ensureWidgetVisible(self.fakelabel)
    def text(self):
        return self.label.text()



class lobby(QWidget):
    def __init__(self, window) -> None:
        self.layout=QHBoxLayout()
        self.label=QLabel("Players:  ")
        self.layout.addWidget(self.label)
        self.window=window
        self.ids=[]
        super().__init__()
        self.setLayout(self.layout)

    def display(self):
        for i in self.window.opps:
            if not (i.sid in self.ids):
                self.add(i)

    def add(self, opp):
        self.label.setText(f'{self.label.text()}\n{opp.name}')
        self.ids.append(opp.sid)        
        #self.layout.addWidget(QLabel(f"{opp.name}"))


class window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.opps=[]             #! stores the return value of scene.addWidget(x), not x
        self.playercards=cardList(100, 500, self)            #! stores the return value of scene.addWidget(x), not x
        self.numbers=[]
        self.table=table(100,200, self)
        self.stack=stack()
        self.Lobby=lobby(self)


    async def setup(self):

        self.sio=socketio.AsyncClient(logger=True)
        
        """sio events"""
        ##startup events
        @self.sio.event
        async def connect():
            await self.sio.emit('namechange', self.name)

        @self.sio.event
        def message(txt):
            self.textOut.setText(self.textOut.text()+'\n'+txt)
            # if self.textOut.lineCount>19:
            #     self.textOut.setText(self.textOut.text().split('\n', 1)[1])
            # else:
            #     self.textOut.lineCount+=1
 
        @self.sio.event
        def trump(string):
            self.player.trump=string
            self.stack.setTrump(string)
            print("Trump: ",string)
            

        @self.sio.event
        def connection(data):
            if settings["dbg"]:
                print(f"connection {data}")
            for i in data:
                if i[0]==self.sio.get_sid():
                    self.opps.append(opponent(*i, isSelf=True))
                else:
                    self.opps.append(opponent(*i))
            self.Lobby.display()

        @self.sio.event
        def game_start(players):
            self.readyButton.deleteLater()
            self.displayOpponents()

        @self.sio.event         #!currently unused
        async def request_game_state():
            await self.sio.emit('request_game_state')

        ##UI EVENTs
        @self.sio.event
        def changed_game_state(data):
            print(data)
            self.refresh_game_state(data)

        @self.sio.event
        def reset_table():
            self.table.clear()


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

    def welcomer(self,argv):
        self.setWindowTitle("python-durak")
        if argv:
            self.client_setup(argv)
            return
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
        from server import server
        self.loop.stop()
        a=server([])
        

    def client_setup(self, argv):
        if argv:
            self.name=argv[1]
            self.server=argv[2]
            self.getValues()
            return
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
            self.stack.setPos(650, 250)
            
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
            
            
            #chat and buttons
            sublayout=QVBoxLayout()

            #self.sendButton=QPushButton("Attack")
            #self.sendButton.GrayedOut()
            self.quitButton=QPushButton("Quit")
            self.quitButton.clicked.connect(self.quit)
            
            self.concedeButton=QPushButton("Concede")
            #self.concedeButton.GrayedOut()

            self.textOut=chat()
            #self.textOut.setWordWrap(True)
            #self.textOut.lineCount=0
            #self.textOut.setMaximumHeight(200)

            

            self.textIn=QLineEdit()
            self.textIn.returnPressed.connect(self.sendMessage)

            sublayout.addWidget(self.quitButton)
            #sublayout.addWidget(self.sendButton)
            sublayout.addWidget(self.concedeButton)
            sublayout.addWidget(self.Lobby)
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

            self.player=local(self.name, self)

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
                game_state["players"][i.name]==None
            except:
                self.opps.remove(i)
                i.widget().setStyleSheet("background-color:yellow")
                i.cards.setText('0')
                break
            if game_state["players"][i.name][2]=='att':
                # if i..name==self.player.name:
                #     self.player.state='att'
                i.widget().setStyleSheet("background-color:blue")          #TODO Make the colors global variables so custom themes can exist
            elif game_state["players"][i.name][2]=='def':
                # if i..name==self.player.name:
                #     self.player.state='def'
                i.widget().setStyleSheet("background-color:red")
            else:
                i.widget().setStyleSheet("background-color:grey")
            i.cards.setText(str(game_state["players"][i.name][0]))

        #refresh table
        self.table.display(game_state["table"][0])
        for i in range(len(game_state["table"][1])//2):
            self.table.addDefense(game_state["table"][1][i*2], game_state["table"][1][i*2+1])
        if self.player.state!='att':
            self.numbers=game_state['numbers']
        else:
            self.numbers+=game_state['numbers']

        #refresh stack
        self.stack.refresh(game_state['stack'][0])



        #?used idk
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

    def displayOpponents(self):
        n=len(self.opps)
        for i, opp in enumerate(self.opps):
            self.scene.addItem(opp)
            opp.setPos(self.playerPoint[0], self.playerPoint[1])
            self.playerPoint=(self.playerPoint[0]+800//n, self.playerPoint[1])
        
    # def IsInNumbers(self, str):
    #     if len(str)!=2:
    #         raise Exception(f'card corrupted, {str}')
    #     else:
    #         if self.numbers==[]:            #! fucks up the if check in card.mouseReleaseEvent
    #             return True
    #         for i in self.numbers:
    #             if i[1]==str[1]:
    #                 return True
                
    # def IsValidDefense(self, item, c)-> bool:
    #     if type(item)!=card:
    #         print(f"item type:  {type(item)}")
    #         return False
    #     else:
    #         print(f"item card: {item.card}, played card: {c}")
    #         b=item.card
    #         if b[0]==c[0] and b[1]<c[1]:
    #             return True
    #         elif  b[0]!=c[0] and c[0]==self.player.trump[0]:
    #             return True
    #         return False

    def exec(self, argv):

        self.loop = QEventLoop(app)

        asyncio.set_event_loop(self.loop)

        with self.loop:
            asyncio.ensure_future(win.setup())
            if len(argv)>1:
                win.welcomer(argv)
            else:
                win.welcomer([])
            self.loop.run_forever()


if __name__=="__main__":
    app=QApplication([])
    win=window()
    win.show()
    win.exec(sys.argv)

    