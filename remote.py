from player import player

class remote(player):
    def __init__(self,c,name):
        super(player,self).__init__()
        self.sock=c
        self.name=name

    def take(self,card):
        self.sock.sendall(("T"+str(card)+"|").encode())

    def attack(self,table):
        self.sock.sendall(("A"+str(table)+"|").encode())

    def defend(self, table):
        self.sock.sendall(("D"+str(table)+"|").encode())
        
    def schiebt(self,table):
        self.sock.sendall(("S"+str(table)+"|").encode())

    def finished(self):
        self.sock.sendall(b"F|")

    def active(self):
        self.sock.sendall(b"C|")        

