from Hit import HitsMenu

class Player:
    def __init__(self, sid, nickname):
        self.sid = sid
        self.nickname = nickname
        self.HP = 100
        self.XP = 10

    def __str__(self):
        return "sid : " + self.sid

    def toJson(self):
        return {
            "nickname": self.nickname,
            "HP": self.HP,
            "XP": self.XP
        }

    def getHitsOptions(self):
        my_options = {}
        f_hits = list(filter(lambda x: HitsMenu[x].cost <= self.XP, HitsMenu))
        for k in f_hits:
            my_options[k] = HitsMenu[k].toJson()
        return my_options
