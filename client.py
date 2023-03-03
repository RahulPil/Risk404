import socket
import re
import pickle
from map import Map
from player import Player

# Sources
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/


# is the actual host of the game
def gameHost(gameID, client_server_name, client_port_number, player_count):
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind((client_server_name, client_port_number))
    host_socket.listen(player_count)
    number_of_connections = 0
    clients = {}
    while number_of_connections < player_count:
        connectionSocket, addr = host_socket.accept()

        connectionSocket.send('Username? '.encode('ascii'))
        username = connectionSocket.recv(1024).decode('ascii')
        clients[username] = connectionSocket

        print(
            f'Player {number_of_connections + 1}, also known as {username} has joined!')
        number_of_connections = number_of_connections + 1

    # intilizes the game map
    mainMap = Map(player_count)

    # intailize amount of troops per player
    troopPerPlayer = 35
    tempPlayerCount = player_count
    while (tempPlayerCount > 3):
        troopPerPlayer = 35 - 5
        tempPlayerCount = tempPlayerCount - 1

    # creates an Array of players
    # also sets the default troop amount
    playerArray = [player_count]
    i = 0
    for key in clients:
        playerArray[i] = Player(key, i + 1, mainMap)
        playerArray[i].setSoliderCount(troopPerPlayer)
        i = i + 1

    # this loop begins the game proccess
    # because the host has to play on the same connection
    # the host address is
    while mainMap.oneWinner() == False:
        for i in playerArray:
            if playerArray[0].id == 1:
                print("Hello Player 1")
                print(mainMap.getPlayerTerritoryList(1))

                # get soldiers, this means that as long as the player can
                # place soliders the must place them, they can't hold them in storage
                # this completes the placing troop proccess
                while (troopPerPlayer > 0):
                    territory_name = input("Where do you want to place your soilders?: ")
                    soilder_amount = int(input("How many soilders?: "))

                    if playerArray[0].placeSoliders(territory_name, soilder_amount) == False:
                        print ("You can't place troops there")

                territory_name
                troop_amount = 0
                while territory_name != "Done" and troop_amount != "Done":
                    territory_name = input("What territory would you like to conquer?: ")
                    


                # handels a non-host player


def gamePlayer(host_socket):
    print("HERE")

# this activates the actual mechanics of the game
# the input is an array of the sockets for the game


def actualGame(socketArray):
    print("WE playing")


# main server information
server_name = 'csslab8.uwb.edu'
server_port = 5176

print("Welcome to Simple Risk")

# begins the client conenction to the Server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((server_name, server_port))

# this message variable will server as the server's conenction point
dataDecoded = ""

# begins the interaction with the SERVER socket
while True:
    # message received from server and decoded
    data = clientSocket.recv(1024)
    dataDecoded = data.decode('ascii')

    if "Game Host" not in dataDecoded or "Valid game sessions" not in dataDecoded:
        print(dataDecoded)
        clientChoise = input('Option: ')

        if (clientChoise == 'EXIT'):
            clientSocket.close()
            clientSocket.send(3)
            exit(0)

        clientSocket.send(int(clientChoise.encode('ascii')))
    else:
        break


# if the client wants to host the game
if ("Game Host" in dataDecoded):
    # regex for the gameID
    gameID = re.search("[0-9]*", dataDecoded)

    # get game information from host
    client_server_name = input("What is your server's name?: ")
    client_port_number = input("What is your port number?: ")
    player_count = input("How many players?: ")

    # go to game function
    gameHost(gameID, client_server_name, int(
        client_port_number), int(player_count))
else:
    # if the client just wants to join a game

    # regex for list of IDs
    validIds = re.search("\[.+\]", dataDecoded)

    # user inputs the ID
    print(f'Here are the valid game sessions: {validIds}')
    clientSocket.send(int(input("What session would you like to joining?: ")))

    # receives the connectection from the ID
    data = clientSocket.recv(4096).decode('ascii')
    host_socket = pickle.loads(data)

    # to recieve on the client side you need to do  and then
    gamePlayer(host_socket)
