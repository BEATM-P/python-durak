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
        await self.sio.call('take', card, self.sid)
        await self.sio.emit('changed_game_state', None, 'all')
        

    async def attack(self,table):
        x=await self.sio.call('attack', table, self.sid)
        await self.sio.emit('changed_game_state', None, 'all')
        for i in x:
            try:
                self.cards.remove(i)
            except:
                raise Exception("player "+ player.name+" is cheater scum")
        return x
                

    async def defend(self, table):
        x=await self.sio.call('defend', table, self.sid)
        await self.sio.emit('changed_game_state', None, 'all')
        return x

    async def schiebt(self,table):
        x=await self.sio.call('schiebt', table, self.sid)
        await self.sio.emit('changed_game_state',None,'all')
        return x

    async def finished(self):
        await self.sio.call('finished', None, self.sid)
        await self.sio.emit('changed_game_state',None,'all')


