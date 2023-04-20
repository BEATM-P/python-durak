from player import player

        


class remote(player):
    def __init__(self,sio,sid):
        super(player,self).__init__()
        self.sio=sio
        self.sid=sid
        self.name="player"
        self.cards=[]
        self.data=None
        self.stoppedDefense=False
        self.stoppedSchub=0
        self.stoppedAttack=False             #0: still Deciding; 1: no Schiebing; 2: Schiebt

    def get_data(self, data):
        self.data=data




    async def take(self,card:list):
        self.cards+=card
        await self.sio.emit('take', card, self.sid)
        #await self.sio.emit('changed_game_state', None, 'all')


    async def attack(self,numbers):
        self.stoppedAttack=False
        await self.sio.emit('attack',numbers, self.sid)

        #await self.sio.emit('changed_game_state', None, 'all')
        

    async def defend(self, table):
        self.stoppedDefense=False
        await self.sio.emit('defend',None, self.sid)
        #await self.sio.emit('changed_game_state', None, 'all')
        

    async def schiebt(self,table):
        self.stoppedSchub=0
        await self.sio.emit('schiebt',table, self.sid)
        #await self.sio.emit('changed_game_state',None,'all')
    

    async def finished(self):
        x=await self.sio.call('finished', None, self.sid)
        #await self.sio.emit('changed_game_state',None,'all')
        return x

