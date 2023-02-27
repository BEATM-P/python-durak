import socket
import window
from player import player


class local(player):
    def __init__(self):
        self.cards=[]
        self.name=input("name")

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
                self.cards.remove(a)
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
    string=string[2:]
    string=string[:len(string)-1]
    return string.split(',')


def handle(data, player):
    print(data[0])
    if data[0]=='T':
        player.take(convert(data[1:]))
        return 'T'
    elif data[0]=='A':
        return player.attack(convert(data[1:]))
         
    elif data[0]=='D':
        return player.defend(convert(data[1:]))
        
    elif data[0]=='S':
        return [player.schiebt(convert(data[1:]))]  
    
    elif data[0]=='F':
        return [player.finished(convert(data[1:]))]
    
    elif data[0]=='C':
        return [player.active(convert(data[1:]))]

    print(data)
    raise Exception("Communication Failed")
    



player=local()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #address=(input("server ip address"), int(input("server port")))
            s=socket.socket()
            host=socket.gethostbyname("localhost")
            print(host)
            s.bind((host,int(input("Port"))))
            s.connect(("127.0.0.1", 5003))
            
            s.sendall(player.name.encode())
            while True:
                data=s.recv(1024)
                st=str(data)
                print(st)
                st=st[2:]
                st=st[:len(st)-1]
                send=[]
                for i in st.split('|'):
                    if i !="":
                        send+=handle(i,player)
                if send=='0':
                    break
                else:
                    s.sendall(str(send).encode())