from client import *
from server import *
from logic import *
from remote import *
from window import *


def connection_test():
    sock = socket.socket()
    host=socket.gethostbyname("localhost")
    print(host)
    sock.bind((host,5003))
    sock.listen(5)  
    c=client("test", "5007")
    player=remote(c.sock, "test")
    print("wtf")
    player.take(['H6', 'H7'])

if __name__=="__main__":
    print("Select Test:")
    print("1: Connection")
    print("")
    if int(input())==1:
        connection_test()