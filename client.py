import socket
import re
import pickle
from map import Map
from player import Player

# Sources
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/


# is the actual host of the game
def gameHost(gameID, client_server_name, client_port_number, player_count, gamehost_username):
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind((client_server_name, client_port_number))
    host_socket.listen(player_count)
    number_of_connections = 0
    clients = {}
    while number_of_connections < player_count:
        connectionSocket, addr = host_socket.accept()
        
        username = clientSocket.recv(1024).decode('ascii')
        clients[username] = connectionSocket

        print(
            f'Player {number_of_connections + 1}, also known as {username} has joined!')
        number_of_connections = number_of_connections + 1

     # SEND FULL MSG TO HOST

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

    # place at least 1 troop on territory
    for player in playerArray:
        listOfPlayerTerritory = player.listTerritories()
        for territory in listOfPlayerTerritory:
            player.addTroop(territory, 1)
            player.addTroopCount(-1)

    # this loop begins the game proccess
    # because the host has to play on the same connection
    # the host address is
    while mainMap.oneWinner() == False:
        for i in playerArray:
            if playerArray[0].id == 1:
                print("Hello Player 1, remember the first number is the player number, the 2nd number is the amount of troops on that territory")
                playerArray[0].printTroopTerritories()

                # get soldiers, this means that as long as the player can
                # place soliders the must place them, they can't hold them in storage
                # this completes the placing troop proccess
                while (troopPerPlayer > 0):
                    territory_name = input(
                        "Where do you want to place your troops?: ")
                    soilder_amount = int(input("How many troops?: "))

                    if playerArray[0].addTroops(territory_name, soilder_amount) == False:
                        print("You can't place troops there")

                # combat phase
                print("Who would you like to conquer!!!!!")
                print("Type Done, when you're finished")
                inGame = True
                while (inGame):
                    defendingTerritory = input("What territory would you like to conquer?: ")
                    attackingTerritory = input("From which territroy would you like to conquer?: ")
                    diceAmount = input("How many dice would you like to use, the most is 3, given that you have 3 or more troops on the attacking territory")
                    if (defendingTerritory == "Done" or attackingTerritory == "Done" or diceAmount == "Done"):
                        inGame = False
                    else:
                        diceAmount = int(diceAmount)
                        if (playerArray[0].battle(attackingTerritory, defendingTerritory, diceAmount)):
                            print(playerArray[0].getTroopTerritories())

                            if (playerArray[0].battle(attackingTerritory, defendingTerritory, diceAmount) > 0):

                                continueAttacking = True
                                while (continueAttacking == True):
                                    input = input("Would you like to keep attacking the same territory, say No or Yes")
                                    if (input == "No"):
                                        continueAttacking = False
                                    else:
                                        if (playerArray[0].battle(attackingTerritory, defendingTerritory, diceAmount)):
                                            if (playerArray[0].getTroopCount(defendingTerritory) > 0):
                                                print(
                                                    f'{defendingTerritory} current stats, vs {attackingTerritory} current stats')
                                                playerArray[0].printTerritroyStats(
                                                    defendingTerritory)
                                                playerArray[0].printTerritroyStats(
                                                    attackingTerritory)

                                            else:
                                                print("You can conquer this territory!")
                                                troupAmount = int(input("How many troops would you like to move?: "))
                                                playerArray[0].conquer(attackingTerritory, defendingTerritory, troupAmount)
                                                continueAttacking = False

                                        else:
                                            print("You've run out of Troops!")
                                            continueAttacking = False
                            else :
                                print("You can conquer this territory!")
                                troupAmount = int(input("How many troops would you like to move?: "))
                                playerArray[0].conquer(attackingTerritory, defendingTerritory, troupAmount)
                                break
                        else:
                            print("This battle cannot happen, either because of too few troops, or the selected territory isn't bordering yours")

            # moving phase
            print("You can move players now, what territory ")


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
    
    gamehost_username = clientSocket.recv(1024).decode('ascii')

    # get game information from host
    client_server_name = input("What is your server's name?: ")
    client_port_number = input("What is your port number?: ")
    player_count = input("How many players?: ")
    
    # go to game function
    gameHost(gameID, client_server_name, int(
        client_port_number), int(player_count), gamehost_username)
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
