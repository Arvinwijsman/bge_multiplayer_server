import socketserver
import ast
import pickle
from models.player import Player

class MyUDPHandler(socketserver.BaseRequestHandler):
    # handle received package
    def handle(self):
        # Extract from udp package
        player_data = pickle.loads(self.request[0])
        message = str(player_data)
        # socket of sender
        socket = self.request[1]

        # if new player connection
        if isinstance(player_data, dict):
            # build player object
            username = player_data['username']
            model = player_data['playermodel']
            print("New player connected! username: " + username)
            player = Player(username, self.client_address, model)

            # inform all connections of new player
            for p in connected_players:
                socket.sendto(pickle.dumps(player), p.getaddress())

            # inform new player of all opponents
            socket.sendto(pickle.dumps(connected_players), self.client_address)

            # save new player
            connected_players.append(player)

        # if update request package by player
        else:
            loc = ast.literal_eval(message)
            opponentinfo = []

            #update location for sender
            for player in connected_players:
                #update location for sender
                if player.address == self.client_address:
                    player.setpos(loc[0], loc[1], loc[2])
                    player.setrot(loc[3])

                # gather opponents data
                else:
                    opponent_info.append(p)

            # return package with opponent data
            socket.sendto(pickle.dumps(opponent_info), self.client_address)

# start server
if __name__ == "__main__":
    HOST, PORT = "localhost", 5000
    connected_players = []
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()
