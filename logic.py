import random
from window import playerdisplay
cards=['H1','H2','H3','H4', 'H5', 'H6', 'H7', 'H8','H9,','H10', 'H11', 'H12', 'H13', 'H14']



class player(): #somehow distinguish remote and local players 
    def __init__(self) -> None:
        self.cards=[]

    def take(self,card):
        self.cards.append(card)

    def attack(self, table):
        return playerdisplay.getAttack(self.cards, table)
    
    def defend(self, table):
        return playerdisplay.getDefense(self.cards,table)
    

class game:
    def __init__(self) -> None:
        self.curr_deck=self.mix()
        self.players=[]
        for i in input("Player Number"):
            self.players.append(player())
        self.deal()
        self.trump= self.curr_deck.pop()


    def mix(self):
        mix=[]  
        deck=cards.copy()
        for i in reversed(range(len(deck))):
            mix.append(deck[random.randint(i)])
        return mix

    def deal(self):
        self.curr_deck()
        for i in range(6):
            for i in self.players:
                i.take(self.curr_deck.pop())
        self.trump=self.curr_deck[0]

    def deal_one(self):
        if self.curr_deck !=[]:
            return self.curr_deck.pop()

    def game(self):
        playernum=1                 #determines which player gets attacked TODO Find lowest trump card
        self.table=[]
        while len(self.players)>1:
            playernum+=self.play(self.players[playernum-1],self.players[playernum], self.players[playernum+1], self.table)  
            if self.table==[]:              #if table is not empty attack is still going(schiebung)
                for i in self.players:
                    i.take_stack(6-len(i.cards))
                    if i.isDone():
                        self.players.remove(i)              #if there are no more cards and a player has no cards hes finished
            playernum % len(self.players)
        


    def play(self,p1, p2, p3):                      #return 0 if defending player wins, otherwise 1
        self.table=p1.attack([])
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


    