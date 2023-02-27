import random
from remote import remote

cards=['H6', 'H7', 'H8','H9,','H10', 'H11', 'H12', 'H13', 'H14',
        'S6', 'S7', 'S8','S9,','S10', 'S11', 'S12', 'S13', 'S14',
        'E6', 'E7', 'E8','E9,','E10', 'E11', 'E12', 'E13', 'E14',
        'B6', 'B7', 'B8','B9,','B10', 'B11', 'B12', 'B13', 'B14']

class game:
    def __init__(self) -> None:
        self.players=[]

    def setup(self):
        self.curr_deck=self.mix()
        #for i in range(int(input("Player Number"))):
        #    a=local()
        #    self.players.append(a)
        self.deal()
        self.trump= self.curr_deck[0]


    def mix(self):
        mix=[]  
        deck=cards.copy()
        for i in reversed(range(len(deck))):
            mix.append(deck[random.randint(0,i)])#FIX THIS SHIT
        return mix

    def deal(self):
        for i in range(6):
            for i in self.players:
                i.take([self.curr_deck.pop()])

    def deal_one(self):
        if self.curr_deck !=[]:
            return self.curr_deck.pop()

    def game(self):
        self.playernum=1                 #determines which player gets attacked TODO Find lowest trump card
        self.active_table=[]
        self.passive_table=[]
        n=len(self.players)
        while n>1:
            n=len(self.players)
            if n>2:      
                self.playernum+=self.play(self.players[self.playernum],self.players[self.playernum-1], self.players[self.playernum+1])
            else:
                self.playernum+=self.play(self.players[self.playernum],self.players[self.playernum-1])  
            if self.active_table==[]:              #if table is not empty attack is still going(schiebung)
                for i in self.players:
                    i.take_stack(6-len(i.cards))
                    if i.isDone():
                        self.players.remove(i)    
                self.passive_table=[]          #if there are no more cards and a player has no cards hes finished
            self.playernum % len(self.players)
        

    def play(self,defe, att1, att2=None):  
        if self.active_table==[]:
            b=att1.attack([])               #return 0 if defending player wins, otherwise 1
            self.active_table+=b
        if self.passive_table==[] and defe.schiebt(self.active_table):                            #dont change table, but next player will be attacked
            return 1
        if att2!=None:
            self.table+=att2.attack(self.active_table)   
        while defe.active(self.active_table) and len(self.active_table)<len(defe.cards):
            self.passive_table+=defe.defend(self.active_table)
            self.active_table+=att1.attack(self.active_table+self.passive_table)
            if att2!=None:
                self.active_table+=att2.attack(self.active_table+self.passive_table)
        if self.active_table== []:
            return 1                    #-> p2 has won-> return 0
        else:
            defe.take(self.active_table+self.passive_table)
            return 2 

