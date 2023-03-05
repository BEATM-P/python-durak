from player import player

        


class remote(player):
    def __init__(self,sio,sid):
        super(player,self).__init__()
        self.sio=sio
        self.sid=sid
        self.name="player"
        self.cards=[]
        self.data=None

    def get_data(self, data):
        self.data=data


    async def take(self,card):
        self.cards+=card
        await self.sio.call('take', card, self.sid, callback=self.get_data())
        await self.sio.emit('changed_game_state', None, 'all')
        

    async def attack(self,table):
        await self.sio.call('attack', table, self.sid, callback=self.get_data())
        await self.sio.emit('changed_game_state', None, 'all')
        return self.data
                

    async def defend(self, table):
        await self.sio.call('defend', table, self.sid, callback=self.get_data())
        await self.sio.emit('changed_game_state', None, 'all')
        return self.data

    async def schiebt(self,table):
        await self.sio.call('schiebt', table, self.sid, callback=self.get_data())
        await self.sio.emit('changed_game_state',None,'all')
        return self.data

    async def finished(self):
        await self.sio.call('finished', None, self.sid)
        await self.sio.emit('changed_game_state',None,'all')


