import eventlet
import socketio
from Hit import Hit
from Hit import HitsMenu
from Player import Player
import os
import time
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio)

players = []
turn_index = 0
turn = "null"


@sio.event
def register(sid, nickname):
    sio.enter_room(sid, "players")
    players.append(Player(sid, nickname))
    if len(players) == 2:
        players[turn_index].XP += 10
        sio.emit('play', to=players[turn_index].sid)
        sio.emit('watch', to=players[(turn_index+1) % 2].sid)


@sio.event
def my_hit_options(sid):
    for p in players:
        if p.sid == sid:
            myself = p
    sio.emit('my_hit_options', json.dumps(myself.getHitsOptions()), room=sid)


@sio.event
def get_news(sid):
    global turn
    sio.emit('get_news', json.dumps(turn), room=sid)


@sio.event
def make_move(sid, cmd):
    global turn
    global turn_index
    hit = HitsMenu[cmd]

    for i in range(len(players)):
        if players[i].sid == sid:
            attacker = i
        else:
            victim = i

    turn = {
        "attacker": players[attacker].nickname,
        "victim": players[victim].nickname,
        "move": hit.toJson()
    }

    players[attacker].XP -= hit.cost
    players[victim].HP -= hit.damage

    turn_index = (turn_index + 1) % 2

    if players[victim].HP <= 0:
        sio.emit('end_game', {"winner": players[attacker].nickname})
    else:
        players[turn_index].XP += 10
        sio.emit('play', to=players[turn_index].sid)
        sio.emit('watch', to=players[(turn_index+1) % 2].sid)


@sio.event
def reset(sid):
    players = []


@sio.event
def get_players(sid):
    players_json = []
    for p in players:
        players_json.append(p.toJson())
        if p.sid == sid:
            myself = p

    ret = json.dumps({
        "self": myself.toJson(),
        "players": players_json
    })

    sio.emit('get_players', ret, room=sid)


@sio.event
def disconnect(sid):
    global players
    for p in players:
        if p.sid == sid:
            myself = p
    print(myself.nickname + " left the server.. ")
    players = list(filter(lambda p: p.sid != sid, players))


port = int(os.environ.get('PORT', 3000))
eventlet.wsgi.server(eventlet.listen(('', port)), app)
