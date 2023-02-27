import socket
from logic import game
from remote import remote


n_player=int(input("how many players?"))

known_port = 50002

sock = socket.socket()
host=socket.gethostbyname("localhost")
print(host)
sock.bind((host,5003))
 
session=game()
sock.listen(5)
while True:
    clients=[]

    while True:
        c, address=sock.accept()
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