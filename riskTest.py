# tests for the code
from map import Map
from player import Player


def main():
    testNumber = int(input("Which test would you like?: "))
    mainMap = Map(3)
    mainMap.intializeMap()
    p1 = Player("Abdalrahman", 1, mainMap)
    p2 = Player("Rahul", 2, mainMap)
    p3 = Player("Napoleon", 3, mainMap)

    if testNumber == 1:
        print("THIS IS TEST 1")
        print("Intialized Map")
        print(mainMap.getMap())

    if testNumber == 2:
        print("THIS IS TEST 2")
        print("Tests that players can get correct information from Map")
        print("\n")

        print("T.1: The list of territories without troop count")
        print(f'Player 1: {p1.listTerritories()}')
        print(f'Player 2: {p2.listTerritories()}')
        print(f'Player 3: {p3.listTerritories()}')
        print("\n")

        print("T.2: The list of territories w/ troops count")
        print(f'Player 1: {p1.getTroopTerritories()}')
        print(f'Player 2: {p2.getTroopTerritories()}')
        print(f'Player 3: {p3.getTroopTerritories()}')

    if testNumber == 3:
        print("This is TEST 3")
        print(
            "This tests if players can iniate a battle sequence, and then conquer territory")

        print("T.1 adding troops to United States and Canada")
        p1.addTroopCount(50)
        p1.addTroops('United States of America', 25)
        p1.addTroops('Canada', 25)
        print(f'Player 1: {p1.mapView.getMap()}')
        print("\n")
        

        print("T.2 p1 intaites a battle sequence with a territory it CANNOT conquer")
        print(f'Did p1 battle p2?: {p1.battle("United States", "Central Africa", 2)}')
        print("\n")

        print("T.3 p1 intaites a battle sequence with a territory it CAN conquer")
        print(f'Did p1 battle p3?: {p1.battle("Canada", "Russia", 3)}')
        print(f'The main Map\n {p1.mapView.getMap()}')
        print("\n")

        print("T.4 p1 should conquer p3's territory")
        print(f'Did p1 conquer p3?: {p1.conquer("Canada", "Russia", 4)}')
        print(f'The main Map\n {p1.mapView.getMap()}')


if __name__ == "__main__":
    main()
