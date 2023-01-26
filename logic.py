import random
from window import IO
cards=['H6', 'H7', 'H8','H9,','H10', 'H11', 'H12', 'H13', 'H14',
        'S6', 'S7', 'S8','S9,','S10', 'S11', 'S12', 'S13', 'S14',
        'E6', 'E7', 'E8','E9,','E10', 'E11', 'E12', 'E13', 'E14',
        'B6', 'B7', 'B8','B9,','B10', 'B11', 'B12', 'B13', 'B14']

window=IO()


class player(): #somehow distinguish remote and local players 
    def __init__(self) -> None:
        self.cards=[]
        self.name=input("Playername: ")

    def take(self,card)->None:
        None

    def attack(self, table)->list:
        return []
        
    def defend(self, table)->bool:
        return False

    def schiebt(self,table)->bool:
        return False

class local(player):
    def take(self,card):
        self.cards+=card

    def attack(self,table):
        window.display(table)
        return table+window.getAttack(self.name,self.cards)

    def defend(self, table):
        window.display(table)
        return window.getDefense(self.name,self.cards, table)
        
    def schiebt(self,table):
        window.display(table)
        return table[0][1]==window.getCard(self.name,self.cards)




class game:
    def __init__(self) -> None:
        self.curr_deck=self.mix()
        self.players=[]
        for i in range(int(input("Player Number"))):
            a=local()
            self.players.append(a)
        self.deal()
        self.trump= self.curr_deck[0]


    def mix(self):
        mix=[]  
        deck=cards.copy()
        for i in reversed(range(len(deck))):
            mix.append(deck[random.randint(0,i)])
        return mix

    def deal(self):
        for i in range(6):
            for i in self.players:
                i.take([self.curr_deck.pop()])

    def deal_one(self):
        if self.curr_deck !=[]:
            return self.curr_deck.pop()

    def game(self):
        playernum=1                 #determines which player gets attacked TODO Find lowest trump card
        self.table=[]
        while len(self.players)>1:      
            playernum+=self.play(self.players[playernum-1],self.players[playernum], self.players[playernum+1])  
            if self.table==[]:              #if table is not empty attack is still going(schiebung)
                for i in self.players:
                    i.take_stack(6-len(i.cards))
                    if i.isDone():
                        self.players.remove(i)              #if there are no more cards and a player has no cards hes finished
            playernum % len(self.players)
        


    def play(self,p1, p2, p3):                      #return 0 if defending player wins, otherwise 1
        self.table+=p1.attack([])
        if p2.schiebt():                            #dont change table, but next player will be attacked
            return 1
        self.table+=p2.attack(self.table)   
        while p2.defend() and len(self.table)<len(p2.cards):
            self.table+=p1.attack(self.table)
            self.table+=p3.attack(self.table)
        p2.defend()
        if self.table==[]:  
            return 0                    #-> p2 has won-> return 0
        else:
            p2.take(self.table)
            return 1 


if __name__=="__main__":
    a=game()
    a.game()