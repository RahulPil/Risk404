# will acts the driver to test the new features of the game
from map import Map
from player import Player

def main():
    print("Welcome to the Testing Terminal")
    print("For Map tests input 1:")
    print("For Player Tests w/ map input 2:")
    arg = int(input("Enter Command Here: "))

    if (arg == 1):
         mapTests()
    elif (arg == 2):
        playerTests()


def mapTests():
    mainMap = Map(2)
    mainMap.intializeMap()
    print("The intializiation of the map has finished")

    print("User 1's territories")
    print(mainMap.getPlayerTerritoryList(1))

    print("\n")

    print("User 2's territories")
    print(mainMap.getPlayerTerritoryList(2))

    print("\n")

    print("User 2 will conquer the United Kingdom")
    mainMap.conquerTerritory('United Kingdom', 2, 0)
    print("User 1's territories")
    print(mainMap.getPlayerTerritoryList(1))

    print("\n")

    print("User 2's territories")
    print(mainMap.getPlayerTerritoryList(2))

    print("User 1 will try to conquer territory that can't be conqured")
    if (mainMap.canBeConquered("Middle East", 1)):
            mainMap.conquerTerritory("Middle East", 1, 0)
            print("Success")
    else:
            print("Can't be conquered")

            print("Player 1 places 5000 troops in Northen Europe")
            mainMap.placeTroops("Northern Europe", 1, 5000)

            print("\nPlayer 2 places 4 troops in Russia")
            mainMap.placeTroops("Russia", 2, 4)

            print("Player 2 conquers all of Player 1's territories")
            mainMap.conquerTerritory('Canada', 2, 0)
            mainMap.conquerTerritory('Greenland', 2, 0)
            mainMap.conquerTerritory('United States of America', 2, 0)
            mainMap.conquerTerritory('Mexico', 2, 0)
            mainMap.conquerTerritory('Upper South America', 2, 0)
            mainMap.conquerTerritory('Lower South America', 2, 0)
            mainMap.conquerTerritory('Brazil', 2, 0)
            mainMap.conquerTerritory('Northern Europe', 2, 0)
            mainMap.conquerTerritory('Left Australia', 2, 0)

            print("User 1's territories")
            print(mainMap.getPlayerTerritoryList(1))
            print("\n")
            print("User 2's territories")
            print(mainMap.getPlayerTerritoryList(2))

            print(f'\nDid someone win?:     {mainMap.oneWinner()}')


def playerTests():
    # intailizes the map
    mainMap = Map(2)
    mainMap.intializeMap()

    # intalizes the players
    player1 = Player("Alexander the Great", 1, mainMap)
    player2 = Player("Gengis Khan", 2, mainMap)

    # lists each person territories
    print(f'Player1:\n{player1.listTerritories()} \n')
    print(f'Player2:\n{player2.listTerritories()}\n')
    

    # player 1's map should change, but NOT player 2's map
    print("Player 1's should change, Player 2's map SHOULD NOT")
    player1.conquerTerritory("North Africa", 50)
    print(f'Player1:\n{player1.listTerritories()}\n')
    print(f'Player2:\n{player2.listTerritories()}\n')

    # player 1's should return false, since no borders between 
    # player 1 and Right A
    ifConq = player1.conquerTerritory("Central Asia", 50)
    print("The following statement should be False")
    print(f'Can player 1 conquer Central Asia:  {ifConq} ')

    # player 2 should be updated to loose North Africa
    player2.receiveNewMap(player1.sendMap())


    print("Player 2 should no longer have north africa")
    print(f'Player1:\n{player1.listTerritories()}\n')
    print(f'Player2:\n{player2.listTerritories()}\n')


    # player 2 reconquers territory
    player2.conquerTerritory("North Africa", 50)
    print("Player 2 should have North Africa, but not Player 1")
    print(f'Player1:\n{player1.listTerritories()}\n')
    print(f'Player2:\n{player2.listTerritories()}\n')

    # player 1 should now have updated map
    player1.receiveNewMap(player2.sendMap())
    print(f'Player1:\n{player1.listTerritories()}\n')
    print(f'Player2:\n{player2.listTerritories()}\n')


if __name__ == "__main__":
    main()
