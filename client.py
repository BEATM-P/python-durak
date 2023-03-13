import socketio
import asyncio

#from window import *
from player import player


class local(player):
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

class client():
    def __init__(self):
        self.server=""
        self.name=""
        
    async def setup(self):
        ##setup internet connection to hosting server
    
        self.player=local("lel")
        self.sio=socketio.AsyncClient()


        ##MISC EVENTS
        @self.sio.event
        async def connect():
            await self.sio.emit('namechange', 'player')
            if self.ready_condition():
                print("ready")
                await self.sio.emit('sta')
                print("debug")

        @self.sio.event
        def trump(string):
            self.player.trump=string
            
        @self.sio.event
        async def change_game_state():
            await self.sio.emit('get_game_state')


        ##UI EVENTs
        @self.sio.event
        def recv_game_state(data):
            print(data)


        ##PLAYER EVENTS
        @self.sio.event
        def take(card):
            self.player.take(card)

        @self.sio.event
        def attack(card):
            return self.player.attack(card)

        @self.sio.event
        def defend(card):
            return self.player.defend(card)

        @self.sio.event
        def schiebt(card):
            return self.player.schiebt(card)

        @self.sio.event
        def finished():
            self.player.finished


        #await self.sio.connect(self.server)

        await self.sio.wait()

    def ready_condition(self):
        a=input("Ready? y/n")
        return a=='y'
        

        while True:
            pass

# a=client('n', 4)
#asyncio.run(a.setup())
