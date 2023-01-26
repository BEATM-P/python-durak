class IO:
    def __init__(self) -> None:
        # setup windows and shit ://
        pass

    def getAttack(self,string, cards):
        if cards==[]:
            return []
        print(string + " is Attacking... choose cards from")
        (cards)
        try:
            b=int(input("hand: "+ str(cards)))
        except:
            "NaN"
            return self.getAttack(string, cards)
        return [cards[b]]+self.getAttack(string,cards.remove(cards[b]))

    def getDefense(self,string, cards, table):
        if table==[]:
            return True
        print(string + " is Defending...  choose card to defend, input card higher than "+len(table)+" to take all")
        try:
            a= int(input("table: "+table))
        except:
            "NaN"
            return self.getDefense(string, cards,table)
        try:
            b=int(input("hand: "+ cards))
        except:
            "NaN"
            return self.getDefense(string, cards,table)
        if table[a][0]==cards[b][0] and table[a][1]<cards[b][1]:
            return self.getDefense(string, cards.remove(cards[b]), table.remove(table[a]))
        else:
            return False

    def display(self, cards):
        print(cards)
