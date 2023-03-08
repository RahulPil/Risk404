import socket
import re
import pickle
import math
from map import Map
from player import Player

# Sources
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close
# https://stackoverflow.com/questions/71857924/checking-all-user-input-for-a-specific-value


def gameHost(gameID, client_server_name, client_port_number, player_count, serverSocket: socket):
    # establishes the socket from which the other players will connect to
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind((client_server_name, client_port_number))
    host_socket.listen(player_count)
    number_of_connections = 0
    clients = {}

    # intailize amount of troops per player
    troopPerPlayer = 35
    tempPlayerCount = player_count
    while (tempPlayerCount > 3):
        troopPerPlayer = troopPerPlayer - 5
        tempPlayerCount = tempPlayerCount - 1
    
    # this while loop will loop untill the playercount is reached
    # each new connection is added to the client array
    # this array will hold the socket information
    while number_of_connections < player_count:
        connectionSocket, addr = host_socket.accept()

        username = connectionSocket.recv(1024).decode()
        clients[username] = connectionSocket
        playerArray[number_of_connections].name = username

        print(f'Player {number_of_connections + 1}, also known as {username} has joined!')
        number_of_connections = number_of_connections + 1

    # creates an Array of players
    # also sets the default troop amount
    playerArray = [player_count]
    i = 0
    for key in clients:
        playerArray[i] = Player(key, i + 1, mainMap)
        playerArray[i].setSoliderCount(troopPerPlayer)
        i = i + 1

    # intilizes the game map
    mainMap = Map(player_count)

    # place at least 1 troop on territory
    for player in playerArray:
        listOfPlayerTerritory = player.listTerritories()
        for territory in listOfPlayerTerritory:
            player.addTroop(territory, 1)

    # this loop begins the game proccess
    # because the host has to play on the same connection
    # the host address of the address
    indexOflist = 0
    while mainMap.oneWinner() == False:
        for i in playerArray:
            # counts user territory if it's above a certin amount the player will get more troops
            amountToBeAdded = 3 if playerArray[0].troopCount <= 9 else int(math.floor(playerArray[0].troopCount / 3))
            playerArray[0].troopCount = playerArray[0].troopCount + amountToBeAdded

            indexOflist = indexOflist + 1
            if playerArray[0].id == 1:
                indexOflist = 0
                print("Hello Player 1")
                playerArray[0].printTroopTerritories()

                # get soldiers, this means that as long as the player can
                # place soliders the must place them, they can't hold them in storage
                # this completes the placing troop proccess
                while (playerArray[0].troopCount > 0):
                    territory_name = userHostInput("Where do you want to place your troops?: ")
                    soilder_amount = int(userHostInput("How many troops?: "))

                    if playerArray[0].addTroops(territory_name, soilder_amount) == False:
                        print("You can't place troops there")

                playerArray[0].printTroopTerritories()

                # COMBAT PHASE
                print("Who would you like to conquer!!!!!")
                print("Type No, when you're finished")
                inGame = True
                # checks it he user decides to quit
                while (inGame):
                    defendingTerritory = userHostInput("What territory would you like to conquer?: ")
                    attackingTerritory = userHostInput("From which territroy would you like to conquer?: ")
                    diceAmount = userHostInput("How many dice would you like to use, the most is 3, given that you have 3 or more troops on the attacking territory")
                    if (defendingTerritory == "No" or attackingTerritory == "No" or diceAmount == "No"):
                        inGame = False
                    else:
                        # prints terriotires
                        playerArray[0].printTroopTerritories()

                        # converts dice to integer number
                        diceAmount = int(diceAmount)

                        # if the battle was succefull
                        if (playerArray[0].battle(attackingTerritory, defendingTerritory, diceAmount)):
                            # print the territoreis
                            print(playerArray[0].getTroopTerritories())

                            # if the defending territory still has troops
                            if (playerArray[0].getTroopCount(defendingTerritory) > 0):

                                # the boolean indicating if if the the user wants to continue to attack the same teritory
                                continueAttacking = True
                                while (continueAttacking == True):
                                    input = userHostInput("Would you like to keep attacking the same territory, say No or Yes")
                                    if (input == "No"):
                                        continueAttacking = False
                                    else:
                                        # checks if a battle occured
                                        if (playerArray[0].battle(attackingTerritory, defendingTerritory, diceAmount)):
                                            # checks if the troop count of the defender has hit 0
                                            if (playerArray[0].getTroopCount(defendingTerritory) > 0):
                                                print(f'{defendingTerritory} TroopCount: {playerArray[0].mapView().getTroopCount(defendingTerritory)}')
                                                print(f'{attackingTerritory} TroopCount: {playerArray[0].mapView().getTroopCount(attackingTerritory)}')
                                            else:
                                                # the terriotry can be conquered
                                                print("You can conquer this territory!")
                                                troupAmount = int(userHostInput("How many troops would you like to move?: "))

                                                # loops until the user enters a valid amount of troops to send to the new territory
                                                while (playerArray[0].conquer(attackingTerritory, defendingTerritory, troupAmount) == False):
                                                    print("Enter a valid amount of troops")
                                                    troupAmount = int(userHostInput("How many troops would you like to move?: "))
                                                continueAttacking = False
                                        else:
                                            # the troop count has gone too low
                                            print("You've run out of Troops!")
                                            continueAttacking = False
                            else:
                                print("You can conquer this territory!")
                                troupAmount = int(userHostInput("How many troops would you like to move?: "))
                                while (playerArray[0].conquer(attackingTerritory, defendingTerritory, troupAmount) == False):
                                    print("False troop movement amount")
                                    troupAmount = int(userHostInput("How many troops would you like to move?: "))
                        else:
                            print("This battle cannot happen, either because of too few troops, or the selected territory isn't bordering yours")
                playerArray[0].printTroopTerritories()

                # troop moving phase
                isMove = userHostInput('Would you like to move territories from one territory to another?, say Yes, or No: ')
                if (isMove == 'Yes'):
                    quitButton = False
                    while quitButton:
                        print("Type No to end this phase")
                        movingTerritory = 'What territory would you like to take troops from?'
                        amountOfTroops = 'How many troops would you like to move?'
                        receivingTerritory = 'Which territory would you like to move these Troops?'
                        if ((movingTerritory == "No") == False or (amountOfTroops == "No") == False or (receivingTerritory == "No") == False):
                            amountOfTroops = int(amountOfTroops)
                            if (playerArray[0].moveTroops()):
                                quitButton = True
                            else:
                                print("This move is incorrect")
                        else:
                            quitButton = True
                playerArray[0].printTroopTerritories()
                
                # updates final map with new information
                mainMap = playerArray[0].sendMap()

            else:
                # HANDELS THE CONNECTION W/ other user

                # player i gets new map & the associated socket
                playerArray[i].receiveNewMap(mainMap)
                currentSocket = clients.get(playerArray[i].name)

                # uses pickile to serlize the map, then sends it via socket
                sendingPlayer = pickle.dumps(playerArray[i])
                connectionSocket.send(sendingPlayer.encode())

                # waits for a socket response
                badPlayerData = currentSocket.recv(1024).decode()
                if (badPlayerData != "SERVER QUIT"):
                    # uses pickile to load map
                    playerData = pickle.loads(badPlayerData)

                    # changes player array with new player, then updates main map
                    # with new data
                    playerArray[i] = playerData
                    mainMap = playerData.sendMap()
                else :
                    # intiaize the client quit proccess
                    print ("A user has Quit, will return to main screen shortly")
                    for p2 in playerArray:
                        if (p2.id != 1):
                            subClient = clients[p2.username]
                            subClient.send("A user has Quit, will return to main screen shortly")
                            subClient.close()
                            beginServerConnection(serverSocket)
                    
                    # send to server SERVER QUIT
                    serverSocket.send("SERVER QUIT")
                    beginServerConnection(serverSocket)

    # If there is one winner, then all the territories will have the same
    playerId = playerArray[0].mapView.listOfTerritories["Canada"][0]
    if (playerId == 1):
        print("Congratulations Winner!")
    else :
        print("You lost (loser)")
    
    for p2 in playerArray:
        if (p2.id != 1 and p2.id != playerId):
            subClient = clients[p2.username]
            subClient.send("You lost (loser)")
            subClient.close()
        elif(p2.id == playerId):
            subClient = clients[p2.username]
            subClient.send("Congratulations Winner!")
            subClient.close()
    serverSocket.send("SERVER QUIT")
    beginServerConnection(serverSocket)
    
    # idea from sources
    def userHostInput(msg):
        userInput = input(msg)
        if userInput == "SERVER QUIT":
            print ("Your a Baby!")
            for p2 in playerArray:
                if (p2.id != 1 and p2.username):
                    subClient = clients[p2.username]
                    subClient.send("A user has Quit, will return to main screen shortly")
                    subClient.close()
                    
            # send to server SERVER QUIT
            serverSocket.send("SERVER QUIT")
            beginServerConnection(serverSocket)
        return userInput


def gamePlayer(clientSocket : socket, serverSocket: socket):
    # begins the client conenction to the Server

    # waits for a socket response
    badPlayerData = clientSocket.recv(1024).decode()

    if (badPlayerData != "A user has Quit, will return to main screen shortly" or "Congratulations Winner!" or "You lost (loser)"):
        # uses pickile to load map
        playerData = pickle.loads(badPlayerData)

        # if it receives client data
        if playerData.mapView.oneWinner() == False:
            # counts user territory if it's above a certain amount the player will get more troops
            amountToBeAdded = 3 if playerData.troopCount <= 9 else int(math.floor(playerData.troopCount / 3))
            playerData.troopCount = playerData.troopCount + amountToBeAdded

            print(f'Hello Player {playerData.id}')
            playerData.printTroopTerritories()

            # get soldiers, this means that as long as the player can
            # place soliders the must place them, they can't hold them in storage
            # this completes the placing troop proccess
            while (playerData.troopCount > 0):
                territory_name = userClientInput("Where do you want to place your troops?: ")
                soilder_amount = int(userClientInput("How many troops?: "))
                if playerData.addTroops(territory_name, soilder_amount) == False:
                    print("You can't place troops there")
            playerData.printTroopTerritories()

            # combat phase
            print("Who would you like to conquer!!!!!")
            print("Type No, when you're finished")
            inGame = True
            # checks it he user decides to quit
            while (inGame):
                defendingTerritory = userClientInput("What territory would you like to conquer?: ")
                attackingTerritory = userClientInput("From which territroy would you like to conquer?: ")
                diceAmount = userClientInput("How many dice would you like to use, the most is 3, given that you have 3 or more troops on the attacking territory")
                if (defendingTerritory == "No" or attackingTerritory == "No" or diceAmount == "No"):
                    inGame = False
                else:
                    # converts dice to integer number
                    diceAmount = int(diceAmount)

                    # if the battle was succefull
                    if (playerData.battle(attackingTerritory, defendingTerritory, diceAmount)):
                        # print the territoreis
                        print(playerData.getTroopTerritories())

                        # if the defending territory still has troops
                        if (playerData.getTroopCount(defendingTerritory) > 0):

                            # the boolean indicating if if the the user wants to continue to attack the same teritory
                            continueAttacking = True
                            while (continueAttacking == True):
                                input = userClientInput("Would you like to keep attacking the same territory, say No or Yes")
                                if (input == "No"):
                                    continueAttacking = False
                                else:
                                    # checks if a battle can be conquered
                                    if (playerData.battle(attackingTerritory, defendingTerritory, diceAmount)):
                                        # checks if the troop count of the defender has hit 0
                                        if (playerData.getTroopCount(defendingTerritory) > 0):
                                            print(f'{defendingTerritory} TroopCount: {playerData.mapView().getTroopCount(defendingTerritory)}')
                                            print(f'{attackingTerritory} TroopCount: {playerData.mapView().getTroopCount(attackingTerritory)}')
                                        else:
                                            # the terriotry can be conquered
                                            print("You can conquer this territory!")
                                            troupAmount = int(userClientInput("How many troops would you like to move?: "))

                                            # loops until the user enters a valid amount of troops to send to the new territory
                                            while (playerData.conquer(attackingTerritory, defendingTerritory, troupAmount) == False):
                                                print("Enter a valid amount of troops")
                                                troupAmount = int(userClientInput("How many troops would you like to move?: "))
                                                continueAttacking = False
                                    else:
                                        # the troop count has gone too low
                                        print("You've run out of Troops!")
                                        continueAttacking = False
                        else:
                            print("You can conquer this territory!")
                            troupAmount = int(userClientInput("How many troops would you like to move?: "))
                            while (playerData.conquer(attackingTerritory, defendingTerritory, troupAmount) == False):
                                print("False troop movement amount")
                                troupAmount = int(userClientInput("How many troops would you like to move?: "))
                    else:
                        print("This battle cannot happen, either because of too few troops, or the selected territory isn't bordering yours")
                playerData.printTroopTerritories()

                # troop moving phase
                isMove = userClientInput('Would you like to move territories from one territory to another?, say Yes, or No: ')
                if (isMove == 'Yes'):
                    quitButton = False
                    while quitButton:
                        print("Type No to end this phase")
                        movingTerritory = 'What territory would you like to take troops from?'
                        amountOfTroops = 'How many troops would you like to move?'
                        receivingTerritory = 'Which territory would you like to move these Troops?'
                        if ((movingTerritory == "No") == False or (amountOfTroops == "No") == False or (receivingTerritory == "No") == False):
                            amountOfTroops = int(amountOfTroops)
                            if (playerData.moveTroops(receivingTerritory, movingTerritory, amountOfTroops)):
                                quitButton = True
                            else:
                                print("This move is incorrect")
                        else:
                            quitButton = True
                playerData.printTroopTerritories()

                # sends updated player view back to the host
                sendingPlayer = pickle.dumps(playerData)
                clientSocket.send(sendingPlayer.encode())

                # idea from sources
                def userClientInput(msg):
                    userInput = input(msg)
                    if userInput == "SERVER QUIT":
                        # send quit msg, username, and wait until host response with confirmation
                        clientSocket.send("SERVER QUIT")

                        # when the response in answered, the connection to the host is closed
                        hostResponse = clientSocket.recv(1024).decode()
                        if hostResponse == "QUIT AKNOWLEDGED":
                            clientSocket.close()
                    return userInput
    else :
        print(badPlayerData)
        clientSocket.close()
        serverSocket.send("SERVER QUIT")
        beginServerConnection(serverSocket)

# intaites the proccess in which a user begins to play the game
def beginServerConnection(serverSocket):
    # this message variable will server as the server's conenction point
    dataDecoded = ""
    run = True
    # begins the interaction with the SERVER socket
    while run:
        # message received from server and decoded
        data = serverSocket.recv(1024)
        dataDecoded = data.decode()
        print(dataDecoded)
        if "username:" in dataDecoded:
            clientUsername = input('Username: ')
            serverSocket.send(clientUsername.encode())
        elif "Game Host:" not in dataDecoded and "Valid game sessions:" not in dataDecoded and "username:" not in dataDecoded:
            clientChoise = input('Option: ')

            if (clientChoise == 'EXIT'):
                serverSocket.close()
                #potential shit
                serverSocket.send(3)
                exit(0)

            serverSocket.send(clientChoise.encode())
        else:
            run = False

    # if the client wants to host the game
    if ("Game Host:" in dataDecoded):
        print('inside game host if statement')
        # regex for the gameID
        gameID = re.search("[0-9]+", dataDecoded)
        gameID = gameID.group()
        print(gameID)

        # get game information from host
        client_server_name = input("What is your server's name?: ")
        client_port_number = input("What is your port number?: ")
        player_count = input("How many players?: ")

        # go to game function
        gameHost(gameID, client_server_name, int(client_port_number), int(player_count), serverSocket)
    else:
        # if the client just wants to join a game

        # regex for list of IDs
        validIds = (re.search("\[.+\]", dataDecoded)).group()

        # user inputs the ID
        print(f'Here are the valid game sessions: {validIds}')
        serverSocket.send(input("What session would you like to joining?: "))

        # receives the connectection from the ID
        data = serverSocket.recv(4096).decode()
        host_socket = pickle.loads(data)

        # extracts information from the host_socket and connect to it
        hostSocketInteraction = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostSocketInteraction.connect((host_socket.gethostname(), host_socket.getsockname()[1]))

        # to recieve on the client side you need to do  and then
        gamePlayer(hostSocketInteraction, serverSocket)


    
def main():
    # main server information
    server_name = 'csslab8.uwb.edu'
    server_port = 5176

    print("Welcome to Simple Risk")

    # begins the client conenction to the Server
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((server_name, server_port))
    beginServerConnection(serverSocket)


if __name__ == "__main__":
    main()

# will be used as the main way to check for anysort of end
# to the game
# got the idea fromthe bellow link
# https://stackoverflow.com/questions/71857924/checking-all-user-input-for-a-specific-value

