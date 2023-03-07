import random
from remote import remote

cards=[ 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
        'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9',
        'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']

class game:
    def __init__(self) -> None:
        self.players=[]

    async def setup(self):
        self.table=table()
        await self.deal()

    async def deal(self):
        for i in range(6):
            for i in self.players:
                await i.take([self.table.get_card()])


    async def game(self):
        self.playernum=1                 #determines which player gets attacked TODO Find lowest trump card
        n=len(self.players)
        while n>1:
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
        if self.table.isEmpty():
            b=await att1.attack(list(self.table.numbers))               #return 0 if defending player wins, otherwise 1
            self.table.add_active(b)
        
        if len(self.table.numbers)==1:
            a=await defe.schiebt(list(self.table.numbers))
            if a:
                self.table.active+= a                           #dont change table, but next player will be attacked
                return 1
        if att2!=None:
            a=await att2.attack(list(self.table.numbers))   
        while len(self.table.active)<len(defe.cards)and self.table.active!=[]:
            a,b =await defe.defend(self.table.active)
            if a == []:
                break;
            for i in b:
                self.player.cards.remove(b)
            self.table.remove_active(a,b)
            self.table.add_active(await att1.attack(list(self.table.numbers)))
            if att2!=None:
                self.table.add_active(await att2.attack(list(self.table.numbers)))
        #print("round finished\n\n\n")    
        if self.table.active== []:
            self.table.reset()
            return 1                    #-> p2 has won-> return 0
        else:
            await defe.take(self.table.active+self.table.passive)
            self.table.reset()
            return 2 


class table():
    def __init__(self):
        self.deck=self.mix()                #stores the stack of unused cards
        self.trump=self.deck[0]             #stores the trump card
        self.active=[]                      #stores all cards that need to be taken or trumped
        self.passive=[]                     #stores already trumped cards that need to be taken if more cards are added and not beaten
        self.numbers=set()                  #stores all numbers with which attackers can legally attack

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
            if len(self.numbers)==0 or int(i[1])in self.numbers:
                self.active.append(i)
                self.numbers.add(int(i[1]))

    def remove_active(self, cards,trumps):          #req: defending player returns two lists, the cards at each index of the two lists are the tuples of card and trumping card
        if len(cards)!=len(trumps):
            raise Exception("defending cards do not match cards on table")
        for i, card in enumerate(cards):
            if card[0]==trumps[i][0] and card[1]<trumps[i][1]:
                self.active.remove(card)
                self.passive.append(card)
                self.passive.append(trumps[i])
                self.numbers.add(int(trumps[i][1]))
            elif card[0]!=trumps[i][0] and trumps[i][0]==self.trump[0]:
                self.active.remove(card)
                self.passive.append(card)
                self.passive.append(trumps[i])
                self.numbers.add(int(trumps[i][1]))
            else:
                raise Exception("defending cards do not match cards on table")
        

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