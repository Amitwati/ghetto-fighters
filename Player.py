from Hit import HitsMenu

class Player:
    def __init__(self, sid, nickname):
        self.sid = sid
        self.nickname = nickname
        self.HP = 100
        self.XP = 10
    
    def __str__(self):
        return "sid : " + self.sid

    def getHitsOptions(self):
        my_options = {}
        f_hint = filter(lambda x: HitsMenu[x].cost <= self.XP, HitsMenu)
        for k,v in HitsMenu:
            if k in f_hint:
                my_options[k] = v
        return my_options

