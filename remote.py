from player import player

class remote(player):
    def __init__(self,sio,sid):
        super(player,self).__init__()
        self.sio=sio
        self.sid=sid
        self.name="player"
        self.cards=[]

    def take(self,card):
        self.cards+=card
        self.sio.emit('take', card, self.sid)
        self.sio.emit('changed_game_state', None, 'all')

    def attack(self,table):
        self.sio.emit('attack', table, self.sid)
        self.sio.emit('changed_game_state', None, 'all')
        #for i in list:
        #    self.cards.remove(i)
        return list

    def defend(self, table):
        self.sio.emit('defend', table, self.sid)
        self.sio.emit('changed_game_state', None, 'all')


    def schiebt(self,table):
        self.sio.emit('schiebt', table, self.sid)

    def finished(self):
        self.sio.emit('finished', None, self.sid)
        self.sio.emit('changed_game_state',None,'all')


