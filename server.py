import socketio
from aiohttp import web
import socket
import upnpy


from logic import game
from remote import remote

class server():
    def __init__(self, n_player=None):
        if n_player==None:                      #script is being executed in terminal; else script is run from test
            n_player=int(input("how many players?"))

        self.session=game()
        self.votes= set()

        self.sio = socketio.AsyncServer(logger=True, engineio_logger=True, async_mode='aiohttp')
        portforwarding()
        app=web.Application()
#        self.sio.listen('', 5005)
        self.print_con_info()
        
        

        @self.sio.event
        def connect(sid, environ):
            print(sid)
            self.sio.enter_room(sid, 'all')
            self.session.players.append(remote(self.sio,sid))
            self.sio.emit("message", f'Connection from {sid}', 'all',skip_sid=sid)

        @self.sio.event
        async def sta(sid):
            print("ready:", sid)
            self.votes.add(sid)
            if len(self.votes)>=n_player:
                await self.sio.emit('message',"Game starting", 'all')
                await self.session.setup()
                await self.sio.emit('trump', self.session.table.trump, 'all')
                await self.session.game()
                
                
            else:
                await self.sio.emit('message', ('Players ready: '+str(len(self.votes))), 'all')

        @self.sio.event
        def name(sid, name):
            print(sid, name)

        @self.sio.event
        def namechange(sid, name):
            print(sid)
            for i in self.session.players:
                if i.sid==sid:
                    i.name=name


        self.sio.attach(app)
        web.run_app(app)    
        #setup internet connections
        # while len(self.session.players)<n_player:
        #     pass
            # True:
                #self.session.players.append(p)
                #sock.sendto(b'ready', address)
                #clients.append(c)
        
        print('all players connected starting game')
        # @self.sio.event
        # def connect(sid, environ):
        #     print("Illegal connection made by", sid)        
        #     self.sio.emit('Illegal connect', "Please no longer connect as game is already running.", room=sid)   

        print("game finished")

# Example output of the get_input_arguments method for the "AddPortMapping" action

    def print_con_info(self):
        host=socket.gethostname()
        IP = socket.gethostbyname(host)
        print("info:  ")
        print(host, IP)               # TODO: print out host ip and port so other client players can specify server to connect to


        #print(host)
        #self.self.sio.bind((host,5003))
        #self.self.sio.listen(5)  


def portforwarding():
    print("portforwarding")
    #see https://upnpy.readthedocs.io/en/latest/Introduction/
    upnp=upnpy.UPnP() 

    devices=upnp.discover()

    device=upnp.get_igd()

    service=device['WANIPConn1']

    service.get_actions()

    host=socket.gethostname()
    IP = socket.gethostbyname(host)

    #service.addPortMapping.get_input_arguments()

    service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=8080,
        NewProtocol='TCP',
        NewInternalPort=8080,
        NewInternalClient=IP,
        NewEnabled=1,
        NewPortMappingDescription='Port Mapping for p2p game client',
        NewLeaseDuration=0
    )

if __name__=="__main__":
    a=server()
