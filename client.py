import socket
import re
import pickle
import math
from map import Map
from player import Player
import sys

# Sources
# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close
# https://stackoverflow.com/questions/71857924/checking-all-user-input-for-a-specific-value


# fixes country/string input
def fixCountryInput(territory_name):
    territory_name = territory_name.lower()
    territory_name = territory_name.title()
    return territory_name

# fixes the input of integer
# the string value is the inter, the option is for which
# method
def fixIntegerInput(inputMethod, args):
    value = inputMethod(args)
    while (value.isdigit() == False):
        print("Bad Integer")
        value = (inputMethod(args))
    return value


def gameHost(gameID, client_server_name, client_port_number, player_count, serverSocket: socket):
    # idea from sources
    # acts a input checker
    def userHostInput(msg):
        userInput = input(msg)
        if userInput == "SERVER QUIT":
            print ("Your a Baby!")
            for p2 in playerArray:
                if (p2.id != 1):
                    subClient = clients[p2.name]
                    sendingPlayer = pickle.dumps(str("A user has Quit, will return to main screen shortly"))
                    subClient.send(sendingPlayer)
                    subClient.close()
                    
            # send to server SERVER QUIT
            serverSocket.send((f'SERVER QUIT: {gameID}').encode())
            host_socket.close()
            beginServerConnection(serverSocket)
        return userInput

    # establishes the socket from which the other players will connect to
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        
        username = serverSocket.recv(1024).decode()
        clients[username] = connectionSocket

        print(f'Player {number_of_connections + 2}, also known as {username} has joined!')
        number_of_connections = number_of_connections + 1
    
    # intilizes the game map
    mainMap = Map(player_count + 1)
    mainMap.intializeMap()
    print(mainMap.getMap())

    # creates an Array of players
    # also sets the default troop amount
    playerArray = [None] * (player_count + 1)
    playerArray[0] = Player("Host", 1, mainMap)
    playerArray[0].setTroopCount(troopPerPlayer)

    # allocates each player in array of players
    index = 1
    for key in clients:
        playerArray[index] = Player(key, index + 1, mainMap)
        playerArray[index].setTroopCount(troopPerPlayer)
        index = index + 1

    # place at least 1 troop on territory
    for player in playerArray:
        listOfPlayerTerritory = player.listTerritories()
        for territory in listOfPlayerTerritory:
            player.addTroopCount(-1)

    # this loop begins the game proccess
    # because the host has to play on the same connection
    # the host address of the address
    while mainMap.oneWinner() == False:
        for player in playerArray:
            if player.id == 1:
                # counts user territory if it's above a certin amount the player will get more troops
                amountToBeAdded = 3 if player.troopCount <= 9 else int(math.floor(player.troopCount / 3))
                player.addTroopCount(amountToBeAdded)

                print(f'Hello Player {player.id}')
                player.printTroopTerritories()
                print(f'Total Troop Amount: {player.troopCount}')

                # get troop, this means that as long as the player can
                # place troops the must place them, they can't hold them in storage
                # this completes the placing troop proccess
                while (player.troopCount > 0):
                    territory_name = fixCountryInput(userHostInput("Where do you want to place your troops?: "))
                    if (player.isPlayerTerritory(territory_name) == False):
                        print("Bad Country Name")
                        continue
                    soilder_amount = fixIntegerInput(userHostInput, "How many troops?: ")
                    if (player.addTroops(territory_name, int(soilder_amount)) == False):
                        print("Bad Troop count")
                    else:
                        player.printTroopTerritories()

                # COMBAT PHASE
                print("WELCOME CONQUERER!!!")
                player.printCombatView()
                print("Type No, if you don't want to")
                inGame = True
                # checks it the user decides to quit
                while (inGame):
                    defendingTerritory = fixCountryInput(userHostInput("What territory would you like to conquer?: "))
                    if defendingTerritory.lower() == "no":
                        break

                    attackingTerritory = fixCountryInput(userHostInput("From which territory would you like to conquer?: "))
                    if attackingTerritory.lower() == "no":
                        break
                    
                    diceAmount = fixIntegerInput(userHostInput, "How many dice would you like to use, the most is 3, given that you have 3 or more troops on the attacking territory?: ")
                    if diceAmount.lower() == "no":
                        break
                    
                    if (defendingTerritory.lower() == "no" or attackingTerritory == "no" or diceAmount == "no"):
                        inGame = False
                    else:
                        # converts dice to integer number
                        diceAmount = int(diceAmount)

                        # if the battle was succefull
                        if (player.battle(attackingTerritory, defendingTerritory, diceAmount)):
                            # print the stats about that territory, and their territory
                            print(f'{defendingTerritory} TroopCount: {player.mapView.getTroopCount(defendingTerritory)}')
                            print(f'{attackingTerritory} TroopCount: {player.mapView.getTroopCount(attackingTerritory)}')

                            # if the defending territory still has troops
                            if (player.mapView.getTroopCount(defendingTerritory) > 0):

                                # the boolean indicating if if the the user wants to continue to attack the same teritory
                                continueAttacking = True
                                while (continueAttacking == True):
                                    inp1 = userHostInput("Would you like to keep attacking the same territory, say Yes or No")
                                    if (inp1.lower() == "no"):
                                        continueAttacking = False
                                    else:
                                        # checks if the battle wasy succefull
                                        if (player.battle(attackingTerritory, defendingTerritory, diceAmount)):
                                            # checks if the troop count of the defender has hit 0
                                            if (player.mapView.getTroopCount(defendingTerritory) > 0):
                                                print(f'{defendingTerritory} TroopCount: {player.mapView.getTroopCount(defendingTerritory)}')
                                                print(f'{attackingTerritory} TroopCount: {player.mapView.getTroopCount(attackingTerritory)}')
                                            else:
                                                # the terriotry can be conquered
                                                print("You can conquer this territory!")
                                                print(f'Updated Troop Count: {attackingTerritory} TroopCount: {player.mapView.getTroopCount(attackingTerritory)}')
                                                troupAmount = int(fixIntegerInput(userHostInput, "How many troops would you like to move?: "))

                                                # loops until the user enters a valid amount of troops to send to the new territory
                                                while (player.conquer(attackingTerritory, defendingTerritory, int(troupAmount)) == False):
                                                    print("Enter a valid amount of troops")
                                                    troupAmount = int(fixIntegerInput(userHostInput, "How many troops would you like to move?: "))
                                                continueAttacking = False
                                        else:
                                            # the troop count has gone too low
                                            print("You've run out of Troops!")
                                            continueAttacking = False
                            else:
                                print("You can conquer this territory!")
                                print(f'Updated Troop Count: {attackingTerritory} TroopCount: {player.mapView.getTroopCount(attackingTerritory)}')
                                troupAmount = int(fixIntegerInput(userHostInput, "How many troops would you like to move?: "))
                                while (player.conquer(attackingTerritory, defendingTerritory, int(troupAmount) == False)):
                                    print("False troop movement amount")
                                    troupAmount = int(fixIntegerInput(userHostInput, "How many troops would you like to move?: "))
                        else:
                            print("This battle cannot happen, either because of too few troops, or the selected territory isn't bordering yours")
                player.printTroopTerritories()

                # troop moving phase
                isMove = userHostInput('Would you like to move territories from one territory to another?, say yes, or no: ')
                if (isMove.lower() == 'yes'):
                    quitButton = False
                    while quitButton == False:
                        print("Type no to end this phase")
                        movingTerritory = fixCountryInput(userHostInput('What territory would you like to take troops from?: '))
                        if movingTerritory.lower() == 'no':
                            break

                        amountOfTroops = fixIntegerInput(userHostInput, 'How many troops would you like to move?: ')
                        if amountOfTroops.lower() == 'no':
                            break

                        receivingTerritory = fixCountryInput(userHostInput('Which territory would you like to move these Troops?'))
                        if receivingTerritory.lower() == 'no':
                            break

                        if ((movingTerritory.lower() == "no") == False or (amountOfTroops.lower() == "no") == False or (receivingTerritory.lower() == "no") == False):
                            amountOfTroops = int(amountOfTroops)
                            if (player.moveTroops()):
                                player.printTroopTerritories()
                                quitButton = True
                            else:
                                print("This move is incorrect")
                        else:
                            quitButton = True
                
                # updates final map with new information
                mainMap = player.sendMap()
            else:
                # HANDELS THE CONNECTION W/ other user

                # player i gets new map & the associated socket
                player.receiveNewMap(mainMap)
                currentSocket = clients.get(player.name)

                # uses pickile to serlize the map, then sends it via socket
                sendingPlayer = pickle.dumps(player)
                currentSocket.send(sendingPlayer)
        
                # waits for a socket response
                badPlayerData = currentSocket.recv(1024)
                print("We got Something!")

                # uses pickile to load map
                playerData = pickle.loads(badPlayerData)
                print(f'CHECKING HOST PICKILE RECEIV VALUE: {isinstance(playerData, Player)}')
                if (isinstance(playerData, Player)):
                    print("We got the player!")
                    # changes player array with new player, then updates main map
                    # with new data
                    player = playerData
                    mainMap = playerData.sendMap()
                else :
                    # intiaize the client quit proccess
                    print ("A user has Quit, will return to main screen shortly")
                    for p2 in playerArray:
                        if (p2.id != 1):
                            subClient = clients[p2.name]
                            sendingPlayer = pickle.dumps(str("A user has Quit, will return to main screen shortly"))
                            subClient.send(sendingPlayer)
                            subClient.close()                    
                    # send to server SERVER QUIT
                    host_socket.close()
                    serverSocket.send((f'SERVER QUIT: {gameID}').encode())
                    beginServerConnection(serverSocket)

    # If there is one winner, then all the territories will have the same
    playerId = playerArray[0].mapView.listOfTerritories["Canada"][0]
    if (playerId == 1):
        print("Congratulations Winner!")
    else :
        print("You lost (loser)")
    
    for p2 in playerArray:
        if (p2.id != 1 and p2.id != playerId):
            subClient = clients[p2.name]
            sendingPlayer = pickle.dumps(str("You lost (loser)"))
            subClient.send(sendingPlayer)
            subClient.close()
        elif(p2.id == playerId):
            subClient = clients[p2.name]
            sendingPlayer = pickle.dumps(str("Congratulations Winner!"))
            subClient.send(sendingPlayer)
            subClient.close()
    serverSocket.send((f'SERVER QUIT: {gameID}').encode())
    host_socket.close()
    beginServerConnection(serverSocket)

def gamePlayer(clientSocket : socket, serverSocket: socket):
    # idea from sources
    def userClientInput(msg):
        userInput = input(msg)
        print(f'msg after input: {userInput}')
        print(userInput=='SERVER QUIT')
        if userInput == "SERVER QUIT":
            # send quit msg, username, and wait until host response with confirmation
            print("HERE 55")
            sendingPlayer = pickle.dumps(str("SERVER QUIT"))
            clientSocket.send(sendingPlayer)
            clientSocket.close()
            serverSocket.send(("SERVER QUIT").encode())
            beginServerConnection(serverSocket)
        return userInput

    # begins the client conenction to the Server
    # waits for a socket response
    while(True):
        badPlayerData = clientSocket.recv(1024)
        while(badPlayerData == None):
            badPlayerData = clientSocket.recv(1024)
        
        playerData = pickle.loads(badPlayerData)

        if (isinstance(playerData, str) == False):
            if playerData != None:
                # if it receives client data
                if playerData.mapView.oneWinner() == False:
                    # counts user territory if it's above a certin amount the player will get more troops
                    amountToBeAdded = 3 if playerData.troopCount <= 9 else int(math.floor(playerData.troopCount / 3))
                    playerData.addTroopCount(amountToBeAdded)

                    print(f'Hello Player {playerData.id}')
                    playerData.printTroopTerritories()
                    print(f'Total Troop Amount: {playerData.troopCount}')

                    # get troop, this means that as long as the player can
                    # place troops the must place them, they can't hold them in storage
                    # this completes the placing troop proccess
                    while (playerData.troopCount > 0):
                        territory_name = fixCountryInput(userClientInput("Where do you want to place your troops?: "))
                        print(territory_name)
                        if (playerData.isPlayerTerritory(territory_name) == False):
                            print("Bad Country Name")
                            continue
                        soilder_amount = fixIntegerInput(userClientInput, "How many troops?: ")
                        if (playerData.addTroops(territory_name, int(soilder_amount)) == False):
                            print("Enter valid Troop count")
                        else:
                            playerData.printTroopTerritories()

                    # COMBAT PHASE
                    print("WELCOME CONQUERER!!!")
                    playerData.printCombatView()
                    print("Type No, if you don't want to")
                    inGame = True
                    # checks it the user decides to quit
                    while (inGame):
                        defendingTerritory = fixCountryInput(userClientInput("What territory would you like to conquer?: "))
                        if defendingTerritory.lower() == "no":
                            break
                        
                        attackingTerritory = fixCountryInput(userClientInput("From which territroy would you like to conquer?: "))
                        if attackingTerritory.lower() == "no":
                            break

                        diceAmount = fixIntegerInput(userClientInput, "How many dice would you like to use, the most is 3, given that you have 3 or more troops on the attacking territory?: ")
                        if diceAmount.lower() == "no":
                            break
                        
                        if (defendingTerritory.lower() == "no" or attackingTerritory == "no" or diceAmount == "no"):
                            inGame = False
                        else:
                            # converts dice to integer number
                            diceAmount = int(diceAmount)

                            # if the battle was succefull
                            if (playerData.battle(attackingTerritory, defendingTerritory, diceAmount)):
                                # print the stats about that territory, and their territory
                                print(f'{defendingTerritory} TroopCount: {playerData.mapView.getTroopCount(defendingTerritory)}')
                                print(f'{attackingTerritory} TroopCount: {playerData.mapView.getTroopCount(attackingTerritory)}')

                                # if the defending territory still has troops
                                if (playerData.mapView.getTroopCount(defendingTerritory) > 0):

                                    # the boolean indicating if if the the user wants to continue to attack the same teritory
                                    continueAttacking = True
                                    while (continueAttacking == True):
                                        inp1 = userClientInput("Would you like to keep attacking the same territory, say Yes or No")
                                        if (inp1.lower() == "no"):
                                            continueAttacking = False
                                        else:
                                            # checks if the battle wasy succefull
                                            if (playerData.battle(attackingTerritory, defendingTerritory, diceAmount)):
                                                # checks if the troop count of the defender has hit 0
                                                if (playerData.mapView.getTroopCount(defendingTerritory) > 0):
                                                    print(f'{defendingTerritory} TroopCount: {playerData.mapView.getTroopCount(defendingTerritory)}')
                                                    print(f'{attackingTerritory} TroopCount: {playerData.mapView.getTroopCount(attackingTerritory)}')
                                                else:
                                                    # the terriotry can be conquered
                                                    print("You can conquer this territory!")
                                                    print(f'Updated Troop Count: {attackingTerritory} TroopCount: {playerData.mapView.getTroopCount(attackingTerritory)}')
                                                    troupAmount = int(fixIntegerInput(userClientInput, "How many troops would you like to move?: "))

                                                    # loops until the user enters a valid amount of troops to send to the new territory
                                                    while (playerData.conquer(attackingTerritory, defendingTerritory, troupAmount) == False):
                                                        print("Enter a valid amount of troops")
                                                        troupAmount = int(fixIntegerInput(userClientInput, "How many troops would you like to move?: "))
                                                    continueAttacking = False
                                            else:
                                                # the troop count has gone too low
                                                print("You've run out of Troops!")
                                                continueAttacking = False
                                else:
                                    print("You can conquer this territory!")
                                    print(f'Updated Troop Count: {attackingTerritory} TroopCount: {playerData.mapView.getTroopCount(attackingTerritory)}')
                                    troupAmount = int(fixIntegerInput(userClientInput, "How many troops would you like to move?: "))
                                    while (playerData.conquer(attackingTerritory, defendingTerritory, troupAmount) == False):
                                        print("False troop movement amount")
                                        troupAmount = int(fixIntegerInput(userClientInput, "How many troops would you like to move?: "))
                            else:
                                print("This battle cannot happen, either because of too few troops, or the selected territory isn't bordering yours")
                    playerData.printTroopTerritories()

                    # troop moving phase
                    isMove = userClientInput('Would you like to move territories from one territory to another?, say yes, or no: ')
                    if (isMove.lower() == 'yes'):
                        quitButton = False
                        while quitButton == False:
                            print("Type no to end this phase")
                            movingTerritory = fixCountryInput(userClientInput('What territory would you like to take troops from?: '))
                            if movingTerritory.lower() == 'no':
                                break

                            amountOfTroops = userClientInput('How many troops would you like to move?: ')
                            if amountOfTroops.lower() == 'no':
                                break

                            receivingTerritory = fixCountryInput(userClientInput('Which territory would you like to move these Troops?'))
                            if receivingTerritory.lower() == 'no':
                                break

                            if ((movingTerritory.lower() == "no") == False or (amountOfTroops.lower() == "no") == False or (receivingTerritory.lower() == "no") == False):
                                amountOfTroops = int(amountOfTroops)
                                if (playerData.moveTroops()):
                                    playerData.printTroopTerritories()
                                    quitButton = True
                                    playerData.printTroopTerritories()
                                else:
                                    print("This move is incorrect")
                            else:
                                quitButton = True
                    
                    # sends player Object back to host
                    sendingPlayer = pickle.dumps(playerData)
                    clientSocket.send(sendingPlayer)
        else:    
            print(playerData)
            clientSocket.close()
            serverSocket.send(("SERVER QUIT").encode())
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
        if "username:" in dataDecoded or "Username" in dataDecoded:
            clientUsername = input('Username: ')
            serverSocket.send(clientUsername.encode())
        
        elif "valid game session" in dataDecoded:
            client_game_sess = input('Game Session: ')
            serverSocket.send(client_game_sess.encode())
        elif "no current" in dataDecoded:
            continue

        elif "Game Host:" not in dataDecoded and "Valid game sessions:" not in dataDecoded and "username:" not in dataDecoded and "Username" not in dataDecoded:
            clientChoise = input('Option: ')
            #reslicinece towards invalid inputs

            serverSocket.send(clientChoise.encode())

            if (clientChoise == '3'):
                serverSocket.close()
                sys.exit()
        else:
            run = False

    # if the client wants to host the game
    if ("Game Host:" in dataDecoded):
        # regex for the gameID
        gameID = re.search("[0-9]+", dataDecoded)
        gameID = gameID.group()
        print(gameID)

        # get game information from host
        client_server_name = input("What is your server's name?: ")
        client_port_number = input("What is your port number?: ")
        player_count = fixIntegerInput(input, "How many players, excluding yourself?: ")
        
        serverSocket.send(client_server_name.encode())
        serverSocket.send(client_port_number.encode())
        
        # go to game function
        gameHost(gameID, client_server_name, int(client_port_number), int(player_count), serverSocket)
    else:
        # if the client just wants to join a game

        # regex for list of IDs
        validIds = (re.search("\[.+\]", dataDecoded)).group()

        # user inputs the ID
        serverSocket.send(input("What session would you like to join?: ").encode())

        # receives the connectection from the ID
        check = True
        data = serverSocket.recv(4096)

        while check:
            if "Please choose a" in data.decode():
                print(data.decode())
                serverSocket.send(input("What session would you like to join?: ").encode())
                data = serverSocket.recv(4096)
                print(type(data.decode()))
            elif "Thank you" in data.decode():
                data = serverSocket.recv(4096)
                check = False
            else:
                check = False
        
        host_socket = pickle.loads(data)


        # extracts information from the host_socket and connect to it
        hostSocketInteraction = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostSocketInteraction.connect((host_socket[0], int(host_socket[1])))

        # to recieve on the client side you need to do  and then
        gamePlayer(hostSocketInteraction, serverSocket)


    
def main():
    # main server information
    server_name = 'csslab8.uwb.edu'
    server_port = 5176

    print("Welcome to Simple Risk")

    # begins the client conenction to the Server
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((server_name, int(server_port)))
    beginServerConnection(serverSocket)


if __name__ == "__main__":
    main()

# will be used as the main way to check for anysort of end
# to the game
# got the idea fromthe bellow link
# https://stackoverflow.com/questions/71857924/checking-all-user-input-for-a-specific-value

