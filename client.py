import socket
import window
from player import player


class local(player):
    def __init__(self, name):
        self.cards=[]
        self.name=input(name)

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

    def active(self,table):
        print(table)
        if input("Write anything to try defending this attack")=="":
            return ["F"]
        else:
            return ["T"]
        

    def defend(self, table):
        res=[]
        
        print(table)
        for i in table:
            print("select card to defend "+i)
            print(self.cards)
            a=input()
            if a=="":
                break;
            elif a in self.cards and a[0]==i[0] and int(a[1])>int(i[1]):
                res.append((a,i))
                table.remove(i)
            else:
                print("invalid input. Give empty input to concede")
        return res,table
        
    def schiebt(self,table):
        #window.display(table)
        #return table[0][1]==window.getCard(self.name,self.cards)
        return ["F"]


def convert(string):
    string=string[1:]
    string=string[:len(string)-1]
    string.replace("'","")
    return string.split(',')





class client():
    def __init__(self,name=None, port=None):
        if name==None:
            name=input(name)
        if port==None:
            port=int(input(port))
        

        ##setup internet connection to hosting server
        self.player=local(name)
        self.sock=socket.socket()
        host=socket.gethostbyname("localhost")
        self.sock.bind((host,port))
        self.sock.connect(("127.0.0.1", 5003))
        self.sock.sendall(player.name.encode())


        ##continuosly receive messages, let the player do a move and send the move back to server
        while True:
            req=self.receive()
            for i in req.split('|'):           ##sometimes the server sends multiple moves at the same time
                res=self.handle(req)        ##moves are separated by | charac
                if res=='0':
                    break;
                elif res!=None:
                    self.send(res)


    def receive(self):
        rec=self.sock.receive(512)
        rec.decode()
        print(rec)
        return rec
        
    def handle(self, data):           #TODO: Implement a case for gamestate being transmitted
        print(data)
        action=data[0]              #determines which move is being requested
        data=data[1:]               
        list=data.strip('][').replace("'","").split(', ')
        if action=='T':
            self.player.take(list)
            return ""
        elif action=='A':
            return self.player.attack(list)     
         
        elif action=='D':
            return self.player.defend(list)
        
        elif action=='S':
            return self.player.schiebt(list)  

        # elif action=='F':
        #     return self.player.finished()
    
        # elif action=='C':
        #     return self.player.active()

        print(data)
        raise Exception("Communication Failed")

       
    # def run_client(name=None, port=None):
        



    #         #address=(input("server ip address"), int(input("server port")))
    #         s=socket.socket()
    #         host=socket.gethostbyname("localhost")
    #         print(host)
    #         s.bind((host, port))
    #         s.connect()            
    #         s.sendall(player.name.encode())


    #         while True:
    #             data=s.recv(1024).decode()
    #             print(data)
    #             #data=data[1:]
    #             data=data[:len(data)-1]
    #             send=[]
    #             for i in data.split('|'):
    #                 if i !="":
    #                     send+=handle(i,player)
    #             if send=='0':
    #                 break
    #             else:
    #                 s.sendall(str(send).replace(" ","").encode())



