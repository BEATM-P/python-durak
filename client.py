import socketio
import asyncio

import window

from player import player


class local(player):
    def __init__(self, name):
        self.cards=[]
        self.name=(name)

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
        res=[]
        
        print(table)
        for i in table:
            print("select card to defend "+i)
            print(self.cards)
            a=input()
            if a=="":
                break;
            elif a in self.cards and a[0]==i[0] and int(a[1])>int(i[1]):
                res.append((a,i))
                table.remove(i)
            else:
                print("invalid input. Give empty input to concede")
        return res,table
        
    def schiebt(self,table):
        #window.display(table)
        #return table[0][1]==window.getCard(self.name,self.cards)
        return [False]

class client():
    def __init__(self,name=None, port=None):
        if name==None:
            name=input('name')
        if port==None:
            port=int(input('port'))
        
    async def setup(self):
        ##setup internet connection to hosting server
        self.player=local("lel")
        self.sio=socketio.AsyncClient()

        @self.sio.event
        async def connect():
            await self.sio.emit('namechange', 'player')
            #if input("Press anything to mark ready")=="1":
            #    print("ready")
            await self.sio.emit('sta', None)
            #    print("debug")

        @self.sio.event
        def take(data):
            self.player.take(data)

        @self.sio.event
        async def attack(data):
            await self.sio.emit('attaking', self.player.attack(data))

        @self.sio.event
        async def defend(data):
            await self.sio.emit(self.player.defend(data))
        
        @self.sio.event
        async def schiebt(data):
            await self.sio.emit('schiebing',self.player.defend(data))

        @self.sio.event
        def finished():
            self.player.finished()
            
        @self.sio.event
        async def change_game_state():
            await self.sio.emit('get_game_state')

        @self.sio.event
        def recv_game_state(data):
            print(data)


        await self.sio.connect('http://0.0.0.0:8080/')

        await self.sio.emit('test')
        

        

        while True:
            pass

a=client('n', 4)
asyncio.run(a.setup())
