# Based on a RISK game map
# I used this map as a refrence
# https://risk-global-domination.fandom.com/wiki/Simple_World_Map

# this file uses the map.py class to simulate a MAP
# this file essentialy acts like a driver to implement the rules of the game

from map import Map
import sys


def main():
    # intillizes the map and the player array
    mainMap = Map(sys.argv[1])
    mainMap.intializeMap()
    playerNumberArray = []
    for i in range(sys.argv[1]):
        playerNumberArray.append(i + 1)
    
    while (mainMap.oneWinner() == False):

    
    




if __name__ == "__main__":
    main()
