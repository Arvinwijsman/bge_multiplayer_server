import bge
import socket
import pickle
import Player

HOST, PORT = "localhost", 0
#UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

#init BGE controller ands scene
cont = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
own = cont.owner
opponents = []

def connect():
    key = cont.sensors['connect']

    #player data
    data = {'username': own['name'], 'playermodel': own['character']}

    #connect
    if key.positive:
        #send data
        sock.sendto(pickle.dumps(data), (HOST, PORT))
        own['connected'] = True
        
        #receive list of connected opponents
        received = sock.recv(4096)
        opponent_data = pickle.loads(received)
        
        #spawn opponents
        for p in opponent_data:
            spawnOpponent(p)

def sendPosition():
    if own['connected'] == True:
        #save player location and orientation
        pos = own.position
        rot = own.worldOrientation.to_euler()
        location = [pos[0], pos[1], pos[2], rot.z]
        #send to server
        sock.sendto(pickle.dumps(location), (HOST, PORT))

def updatePositions():
    if own['connected'] == True:
        # listen for opponents positions
        try:
            received = sock.recv(4096)
        except socket.error:
            print('No data received')

        opponent_data = pickle.loads(received)

        # when location info received: update opponent locations in-game
        if isinstance(opponent_data, list):
            for player in opponent_data:
                for ob in opponents:
                    # matching in playerlist
                    if ob['username'] == player.getname():
                        # update opponents position and z-axis rotation
                        ob.worldPosition = player.getpos()
                        ob.worldOrientation.z = player.getrot()
        # if opponent not recognised, spawn as new
        else:
            spawnOpponent(data)

def spawnOpponent(p):
    #off-screen opponent spawner
    empty = scene.objects["Spawner"]
    
    #add opponent player-mesh
    model = p.getmodel()
    if model == 'model_boot':
        ob = scene.addObject("opponent_boat", empty)
    elif model == 'model_tank':
        ob = scene.addObject("opponent_tank", empty)
    elif model == 'model_wheel':
        ob = scene.addObject("opponent_wheel", empty)
    else:
        ob = scene.addObject("opponent", empty)

    #update opponent list    
    ob['username'] = p.getname()
    opponents.append(ob)
