class player():
    def __init__(self,name) -> None:
        self.cards=[]

    def take(self,card)->None:
        self.cards+=card

    def attack(self, table)->list:
        return []
        
    def defend(self, table)->bool:
        return False

    def schiebt(self,table)->bool:
        return False

    def finished(self)->bool:
        return self.cards==[]

    def active(self)->bool:
        return False