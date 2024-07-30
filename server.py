import socket
from _thread import *
from player import Player
from game import Game
import pickle
import random
import pygame
import details
pygame.init()


server = details.IP
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

GREEN = (255, 127, 127)
RED = (118, 242, 104)

AQUA = (0, 175, 185)
LIGHTRED = (240, 113, 103)
SAIL = (254, 217, 183)
LIGHTYELLOW = (253, 252, 220)

oldcolor = (65,105,225)
oldcolor2 = (220,20,60)


connected = set()
games = {}
idCount = 0

def threaded_client(conn, player, gameId):
    global idCount
    conn.send(pickle.dumps(games[gameId].players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 6))  # Use pickle.loads() to deserialize the received data

            if gameId in games:
                game = games[gameId]
                if data == "getID":
                    conn.send(pickle.dumps(player))
                    continue
                elif data == "getGame":
                    conn.send(pickle.dumps(game))
                    continue
                elif data == "winner":
                    game.winner = True
                    conn.send(pickle.dumps(game))
                    continue
                elif data == "reset":
                    game.winner = False
                    game.reset = True
                    conn.send(pickle.dumps(game))
                    continue
                elif data == "unreset":
                    game.reset = False
                    conn.send(pickle.dumps(game))
                    continue
                game.players[player] = data

                if not data:
                    print("Disconnected")
                    break
                else:
                    if player == 1:
                        reply = game.players[0]
                    elif player == 0:
                        reply = game.players[1]

                    conn.sendall(pickle.dumps(reply))  # Use pickle.dumps() to serialize the reply data

        except:
            break
    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    player = 0 
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        player = 1

    start_new_thread(threaded_client, (conn, player, gameId))
    print(player, "Connected")