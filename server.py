import socketio
from aiohttp import web
import socket
import upnpy
import sys


from logic import game
from remote import remote

class server():
    def __init__(self,args, min_player=None):

        if min_player==None:
            self.min_player=2


        self.session=game()
        self.votes= set()

        self.sio = socketio.AsyncServer(logger=True, engineio_logger=False, async_mode='aiohttp', ping_timeout=60)
        app=web.Application()
#        self.sio.listen('', 5005)

        #if len(args)>1 and args[1]=='-l':
        self.print_con_info()
            #portforwarding()

        

        @self.sio.event
        async def connect(sid, environ):
            print(sid)
            self.sio.enter_room(sid, 'all')
            data=[]
            for i in self.session.players:
                data.append((i.sid, i.name))
            await self.sio.emit("connection",data, room=sid)
            await self.sio.emit("message", f'[Console]: Connection from {sid}', 'all',skip_sid=sid)

        @self.sio.event
        async def disconnect(sid):
            print(sid)
            self.sio.leave_room(sid, 'all')
            p=self.findPlayerBySid(sid)
            self.session.players.remove(p)
            await self.sio.emit("message", f"[Console]: {p.name} has disconnected", 'all')

        @self.sio.event
        async def message(sid, txt):
            p=self.findPlayerBySid(sid)
            await self.sio.emit('message', f'{p.name}: {txt}')

        @self.sio.event
        async def sta(sid):
            print("ready:", sid)
            self.votes.add(sid)
            await self.sio.emit('message', f'Players ready: {len(self.votes)}/{len(self.session.players)}', 'all')
            if len(self.votes)>=len(self.session.players) and len(self.session.players)>=self.min_player:       #start the game
                await self.sio.emit('game_start', 'all')
                await self.session.setup()
                await self.sio.emit('trump', self.session.table.trump, 'all')
                await self.session.game()

                

        # @self.sio.event
        # def name(sid, name):
        #     print(sid, name)

        @self.sio.event
        async def namechange(sid, name):
            self.session.players.append(remote(self.sio,sid, name))
            print(sid)
            await self.sio.emit("connection", [(sid, name)])


        @self.sio.event
        async def attacking(sid, cards):
            print(f"{sid} is attacking with {str(cards)}")
            if len(cards)<=self.session.table.allowedCardNumber and self.session.validNumbers(cards):
                self.session.table.add_active(cards)
                p=self.findPlayerBySid(sid)
                print(f"removing {cards} from p.cards")
                for i in cards:
                    p.cards.remove(i)
                #await self.sio.emit('changed_game_state',self.session.gameData.get(),'all', skip_sid=sid)f
                return True
            return False

        @self.sio.event
        async def stop_attack(sid):
            self.findPlayerBySid(sid).stoppedAttack=True

        @self.sio.event
        async def defending(sid, cards):
            if self.session.validDefense(cards):
                p=self.findPlayerBySid(sid)
                print(f"removing {cards} from p.cards")
                for i in range(len(cards)//2):
                        p.cards.remove(cards[i*2+1])
                try:
                    self.session.table.remove_active(cards)
                except ValueError:
                    for i in range(len(cards)//2):
                        p.take(cards[2*i+1])
                    return False
                #await self.sio.emit('changed_game_state',self.session.gameData.get(), 'all', skip_sid=sid)
                return True
            return False

        @self.sio.event
        async def stop_defense(sid):
            self.findPlayerBySid(sid).stoppedDefense=True

        @self.sio.event
        async def schieben(sid, cards):

            if cards==[]:
                self.findPlayerBySid(sid).stoppedSchub=1
                print(f"{sid} is not schiebing")
                return True
            if len(cards)<self.session.table.allowedCardNumber and self.session.validNumbers(cards):
                p=self.findPlayerBySid(sid)
                print(f"removing {cards} from p.cards")
                for i in cards:
                    p.cards.remove(i)
                                        
                print(f"{sid} is schiebing with {str(cards)}")
                self.session.table.add_active(cards)
                #await self.sio.emit('changed_                                                                                                                                                                                                                                                                                                                                                                                                                                       game_state',self.session.gameData.get(),'all', skip_sid=sid)
                self.findPlayerBySid(sid).stoppedSchub=2
                return True
            return False

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

    def findPlayerBySid(self, sid):
        for i in self.session.players:
            if i.sid==sid:
                return i

    def print_con_info(self):
        host=socket.gethostname()
        IP = socket.gethostbyname(host)
        print("info:  ")
        print(host, IP)               # TODO: print out host ip and port so other client players can specify server to connect to

    def getAllPlayernames(self):
        res=[]
        for i in self.session.players:
            res.append(i.name)
        return res

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
    a=server(sys.argv)
