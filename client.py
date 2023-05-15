


from player import player
from window import card,opponent, asyncio, socketio
#local = local player with GUI
#console = terminal input player for debugging purposes


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

        