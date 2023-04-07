


from player import player
from window import card,opponent, asyncio, socketio
#local = local player with GUI
#console = terminal input player for debugging purposes

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

class console(player):
    
    def __init__(self, name):
        self.cards=[]
        self.name=(name)
        self.trump=None
    def take(self,card):
        self.cards+=card
        print("taking "+(str(card)))

    def attack(self,table):
        res=[]
        while True:
            if table==[]:
                print("attack with any card")
                print(self.cards)
                a=input()
                if a in self.cards:
                    res.append(a)
                    table.append(a)
                    self.cards.remove(a)
                else:
                    print("You are forced to attack. Please select valid card")
            print(table)
            print(self.cards)
            b=input("Want to add cards? Give empty input to finish")
            if b=="":
                return res
            elif b in self.cards:       #TODO check if valid move
                table.append(b)
                res.append(b)
                self.cards.remove(b)
            else:
                print("Invalid Input")

       

    def defend(self, table):
        cards=[]
        trumps=[]
        while table!=[]:
            print(table)
            a=int(input("select card index to defend"))
            print(self.cards)
            b=(input("which card to defend with"))
            if b=="":
                break;
            b=int(b)
            card=table[a]
            trump=self.cards[b]
            if card[0]==trump[0] and card[1]<trump[1]:
                table.remove(card)
                cards.append(card)
                trumps.append(trump)
                self.cards.remove(trump)
            elif card[0]!=trump[0] and trump[0]==self.trump[0]:
                table.remove(card)
                cards.append(card)
                trumps.append(trump)
                self.cards.remove(trump)
            else:
                print("invalid input. Give empty input to concede")
        return cards, trumps
        
    def schiebt(self,table):
        #window.display(table)
        #return table[0][1]==window.getCard(self.name,self.cards)
        return None

        