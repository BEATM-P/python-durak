import random
from remote import remote
import time
import asyncio

cards=[ 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
        'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9',
        'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']


class gameState():
    def __init__(self, game):
        self.game=game

    def get(self):
        result={}
        players={}
        for i, p in enumerate(self.game.players):
            if i == self.game.playernum:
                players[p.name]=(len(p.cards),p.sid, 'def')
            elif i==self.game.playernum-1 or i==self.game.playernum+1:
                players[p.name]=(len(p.cards),p.sid, 'att')
            else:
                players[p.name]=(len(p.cards),p.sid, None)
        table=self.game.table.active, self.game.table.passive
        result["players"]=players
        result["table"]=table
        result["numbers"]=list(self.game.table.numbers)
        return result

class game():
    def __init__(self) -> None:
        self.players=[]
        self.gameData=gameState(self)
        self.table=table()

    async def setup(self):
        await self.deal()

    async def deal(self):
        for i in range(6):
            for i in self.players:
                await i.take([self.table.get_card()])


    async def game(self):
        self.playernum=1  
                    #determines which player gets attacked TODO Find lowest trump card
        n=len(self.players)
        while n>1:
            print("self.playernum",self.playernum)   
            n=len(self.players)
            if n>2:      
                self.playernum+=await self.play(self.players[self.playernum % n],self.players[(self.playernum-1) % n], self.players[self.playernum+1])
            else:
                self.playernum+=await self.play(self.players[self.playernum % n],self.players[(self.playernum-1) % n])  
            if self.table.active==[]:              #if table is not empty attack is still going(schiebung)
                for i in self.players:
                    if self.table.stack_empty() and len(i.cards)==0:
                        i.finished()
                        self.player.remove(i)
                    while (not self.table.stack_empty()) and len(i.cards)<6:
                        await i.take(self.table.get_card())
                        
            self.playernum % len(self.players)
        

    async def play(self,defe, att1, att2=None): 
        await defe.sio.emit('changed_game_state', self.gameData.get(), 'all') 
        self.table.allowedCardNumber=len(defe.cards)
        
        await att1.attack(list(self.table.numbers))               #return 0 if defending player wins, otherwise 1
        #await defe.sio.emit('changed_game_state', self.gameData.get(), 'all') 
        while self.table.active==[]:
            time.sleep(3)
            await defe.sio.emit('changed_game_state', self.gameData.get(), 'all')
        
        await defe.schiebt((self.table.active))
                               #dont change table, but next player will be attacked
        while defe.stoppedSchub==0:
            time.sleep(3)
            print("waiting for schub")
            await defe.sio.emit('changed_game_state', self.gameData.get(), 'all')
        if defe.stoppedSchub==2:
            return 1

        await defe.defend(self.table.active)

        if att2!=None:
            await att2.attack(list(self.table.numbers))   

        if not att2!=None:
            while (not defe.stoppedDefense) and not (att1.stoppedAttack and att2.stoppedAttack):
                time.sleep(3)
                await defe.sio.emit('changed_game_state', self.gameData.get(), 'all')
                #wait (defe.sio.emit('changed_game_state', self.gameData.get(), 'all'))     #!ugly, sio is in every remote player and always the same
        while (not defe.stoppedDefense) and not (att1.stoppedAttack):
                time.sleep(3)
                await defe.sio.emit('changed_game_state', self.gameData.get(), 'all')

        if self.table.active== []:
            self.table.reset()
            await defe.sio.emit('reset_table', None, all)
            return 1                    #-> p2 has won-> return 0
        else:
            await defe.take(self.table.active+self.table.passive)
            self.table.reset()
            defe.sio.emit('reset_table', None, all)
            return 2 

    def validNumbers(self,cards):
        for i in cards:
            if not self.validNumber(i):
                print(i)
                return False
        return True
        
    def validNumber(self, card):
        if len(self.table.numbers)==0:
            self.table.numbers.add(card)
            print(card)
            return True
        for x in self.table.numbers:
            print(card)
            print(x[1], card[1])
            if x[1]==card[1]:
                return True
        return False
                    
        return True

    def validDefense(self,cards):
        if len(cards) % 2 !=0:
            #raise Exception('Invalid Defense')
            return False
        for i in range(len(cards)/2):
            a=cards[i*2]
            b=cards[i*2+1]
            if a[0]==b[0] and a[1]<b[1]:
                pass
            elif a[0]!=b[0] and b[0]==self.trump[0]:
                pass
            else:
                return False
        return True

class table():
    def __init__(self):
        self.deck=self.mix()                #stores the stack of unused cards
        self.trump=self.deck[0]             #stores the trump card
        self.active=[]                      #stores all cards that need to be taken or trumped
        self.passive=[]                     #stores already trumped cards that need to be taken if more cards are added and not beaten
        self.numbers=set()                  #stores all numbers with which attackers can legally attack
        self.allowedCardNumber=0

    def mix(self):
        mix=[]  
        deck=cards.copy()
        for i in reversed(range(len(deck))):
            a=random.randint(0,i)
            card=deck[a]
            mix.append(card)
            deck.remove(card)
        return mix

    def add_active(self, cards):
        for i in cards:
            self.active.append(i)
            self.allowedCardNumber-=1

    def remove_active(self, cards):          #req: defending player returns two lists, the cards at each index of the two lists are the tuples of card and trumping card
        self.passive+=cards
        for i in range(len(cards)/2):
            self.active.remove(cards[i*2])
        

    def get_card(self):
        return self.deck.pop()

    def stack_empty(self):
        return self.deck==[]

    def reset(self):
        self.numbers=set()
        self.active=[]
        self.passive=[]


    def isEmpty(self):
        return self.active==[]and self.passive==[]






