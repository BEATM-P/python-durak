import random
cards=['H1','H2','H3','H4', 'H5', 'H6', 'H7', 'H8','H9,','H10', 'H11', 'H12', 'H13', 'H14']



class player():
    def __init__(self) -> None:
        cards=[]

    def take(card):
        cards.insert(card)


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

    def deal_one(self):
        if self.curr_deck !=[]:
            return self.curr_deck.pop()

    def game(self):
        playernum=0
        while len(self.players)>1:
            self.play(self.players[1],self.players[2], self.players[1], [])

    def play(self,p1, p2, p3):
        table=p1.attack([])
        if p2.schiebt():

        while True:
            table+=p1.attack(table)
            table=p2.defend(table)
            table+=p3.attack(table)


    