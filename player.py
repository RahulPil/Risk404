# Based on a RISK game map
# I used this map as a refrence
# https://risk-global-domination.fandom.com/wiki/Simple_World_Map

# the map allows for the conquering of territories
# keeps track of which players, and how many troops per peice of territory is conquered
# checks if a territory CAN be conquered, by checking borders

import random
import copy
from map import Map

class Player:
    # intalizes the name of the player, their name, & their ID (1, 2, 3, etc.)
    # it also intailzes them to a map
    def __init__(self, newName, newNumber, newMap : Map):
        self.name = newName
        self.id = newNumber
        self.soliderCount = 0
        self.mapView = copy.deepcopy(newMap)
    
    # sets the initial solider count
    def setSoliderCount(self, count):
        self.soliderCount = count
    
    # adds to the solider count
    def addSoliders(self, count):
        self.setSoliderCount = self.soliderCount + count
    
    # add soliders to territory
    def placeSoliders(self, territory_name, soilder_amount):
        return self.mapView.placeTroops(territory_name, self.id, soilder_amount)
        
    # list all territories controled by the player
    # this method encapsulates the getPlayerTerritoryList in the map.py object
    def listTerritories(self) :
        return self.mapView.getPlayerTerritoryList(self.id)

    # list all territories controled by the player, with solider count
    # this methid encapsulates the getCountySoliderCount in the map.py object 
    def getSoliderTerritories(self) :
        return self.mapView.getCountySoliderCount(self.id)
    
    # conquers the territory based on the territioryName & assighns soliders for
    # that territory
    def conquerTerritory(self, territoryName, soliderCount):
        # checks if the territory can be conquered
        if (self.mapView.canBeConquered(territoryName, self.id) == False) :
            return False
        else :
            self.mapView.conquerTerritory(territoryName, self.id, soliderCount)
            return True
    
    # this will receive a newMap
    def receiveNewMap(self, newMap : Map):
        self.mapView = newMap

    # this will send a deepcopy of this players mapView
    def sendMap(self):
        return copy.deepcopy(self.mapView)
