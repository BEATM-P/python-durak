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
        data=self.sock.recv(1024)
        data=str(data)
        data=data[2:]
        data=data[:len(data)-1]
        return data.split(",")

    def defend(self, table):
        self.sock.sendall(("D"+str(table)+"|").encode())
        data=self.sock.recv(1024)
        #parse data
        return data

    def schiebt(self,table):
        self.sock.sendall(("S"+str(table)+"|").encode())
        data=self.sock.recv(1024)
        data=str(data)
        data=data[2:]
        data=data[:len(data)-1]
        return data.split(",")

    def finished(self):
        self.sock.sendall(b"F|")
        data=self.sock.recv(1024)
        data=str(data)
        data=data[2:]
        data=data[:len(data)-1]
        return data=="True"

    def active(self):
        self.sock.sendall(b"C|")        
        data=self.sock.recv(1024)
        data=str(data)
        data=data[2:]
        data=data[:len(data)-1]
        return data=="True"

