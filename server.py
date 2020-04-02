import eventlet
import socketio
from Hit import Hit
from Player import Player
import os
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio)

players = []

@sio.event
def connect(sid, environ):
    global players
    players.append(Player(sid, "Player " + str(len(players)+1)))


@sio.event
def my_hit_options(sid):
    for p in players:
        if p.sid == sid:
            myself = p
    sio.emit('my_hit_options', json.dumps(myself.getHitsOptions()), room=sid)


@sio.event
def disconnect(sid):
    global players
    players = list(filter(lambda p: p.sid != sid, players))


port = int(os.environ.get('PORT', 3000))
print("started listening on 0.0.0.0:"+str(port))
eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)
