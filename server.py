import socket
from logic import game
from remote import remote

class server():
    def __init__(self, n_player=None):
        if n_player==None:                      #script is being executed in terminal; else script is run from test
            n_player=int(input("how many players?"))

        session=game()

        #setup internet connections
        self.setup()
        while True: 
            clients=[]
            while True:
                c, address=self.sock.accept()
                data = c.recv(1024)
                print('connection from: {}'.format(address))
                p=remote(c, data)
                session.players.append(p)
                #sock.sendto(b'ready', address)
                clients.append(c)

                if len(clients)==n_player:
                    print('all players connected starting game')
                    break
            session.setup()
            session.game()

            print("game finished")


    def setup(self):
        self.sock = socket.socket()
        host=socket.gethostbyname("localhost")
        print(host)
        self.sock.bind((host,5003))
        self.sock.listen(5)  