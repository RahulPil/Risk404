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
    def __init__(self, newName, newNumber, newMap: Map):
        self.name = newName
        self.id = newNumber
        self.TroopCount = 0
        self.mapView = copy.deepcopy(newMap)

    # sets the initial Troop count
    def setTroopCount(self, count):
        self.TroopCount = count

    # adds to the Troop count
    def addTroopCount(self, count):
        self.setTroopCount = self.TroopCount + count

    # list all territories controled by the player
    # this method encapsulates the getPlayerTerritoryList in the map.py object
    def listTerritories(self):
        return self.mapView.getPlayerTerritoryList(self.id)

    # list all territories controled by the player, with Troop count
    # this methid encapsulates the getCountyTroopCount in the map.py object
    def getTroopTerritories(self):
        return self.mapView.getPlayerSoldierList(self.id)
    
    # prints all territories w/ Troop Count
    def printTroopTerritories(self):
        for territroyFact in self.mapView.getPlayerSoldierList(self.id):
            print(f'{territroyFact[0]}: {territroyFact[2]}\n')

    # playes out a battle sequence
    def battle(self, attackTerritory, defendTerritory, diceAmount):
        # checks if the territory can be conquered
        if (self.mapView.canBeAttacked(defendTerritory, self.id) == False or self.mapView.isBorder(attackTerritory, defendTerritory) == False):
            return False
        elif (self.mapView.getTroopCount(attackTerritory) < 2):
            # checks if the attacking terrsitory has enough troops to attacks
            return False
        else:
            self.battleSequence(attackTerritory, defendTerritory, diceAmount)
            return True

    # once a player wins a battle they may conquer
    def conquer(self, attackTerritory, defendTerritory, amountOfTroopsToMove):
        attackTerritoryTroopCount = self.mapView.getTroopCount(attackTerritory)
        if (amountOfTroopsToMove > attackTerritoryTroopCount):
            return False
        elif attackTerritoryTroopCount - amountOfTroopsToMove < 1:
            return False
        elif self.mapView.listOfTerritories.get(defendTerritory)[1] != 0:
            return False

        self.setTroops(attackTerritory,
                       (attackTerritoryTroopCount - amountOfTroopsToMove))
        self.conquerTerritory(defendTerritory, amountOfTroopsToMove)
        return True

    # this will receive a newMap
    def receiveNewMap(self, newMap: Map):
        self.mapView = newMap

    # this will send a deepcopy of this players mapView
    def sendMap(self):
        return copy.deepcopy(self.mapView)

    # dice roll
    def diceRoll(self):
        return random.randint(1, 6)

    # this method plays through only one battle sequence
    # returns an array where the first value is attacker's troops after battle
    # and the 2nd array value is the defender's troop after battle
    def battleSequence(self, attackTerritory, defendTerritory, diceRollAmount):

        attackTroopCount = self.mapView.getTroopCount(attackTerritory)
        defentTroopCount = self.mapView.getTroopCount(defendTerritory)

        # the amount of diceRolls permited, per player
        attackDiceRoll = diceRollAmount
        defenseDiceRoll = 2 if defentTroopCount > 2 else 1

        # the number of attacks phases is based on the amount of defence and attack Troops
        amountOfAttacks = 2 if defentTroopCount == 2 and attackTroopCount > 2 else 1

        # ther arrays contain the dice values
        attackDiceArray = [None] * attackDiceRoll
        defensekDiceArray = [None] * defenseDiceRoll

        # dice is rolled and the values are placed in the dice arrays
        for i in range(attackDiceRoll):
            attackDiceArray[i] = int(self.diceRoll())

        for i in range(defenseDiceRoll):
            defensekDiceArray[i] = int(self.diceRoll())

        # dice are rted
        attackDiceArray.sort(reverse=True)
        defensekDiceArray.sort(reverse=True)

        # attack phase is done, basically comapres the highest 1st and 2nd dice
        # to see if Troops will be lost
        for i in range(amountOfAttacks):
            if attackDiceArray[i] > defensekDiceArray[i]:
                defentTroopCount = defentTroopCount - 1
            else:
                attackTroopCount = attackTroopCount - 1

        self.setTroops(attackTerritory, attackTroopCount)
        self.mapView.listOfTerritories[defendTerritory] = [self.mapView.listOfTerritories[defendTerritory][0], defentTroopCount]

   # sets troops on territory
    def setTroops(self, territoryName, amountOfTroops):
        if self.mapView.listOfTerritories.get(territoryName)[0] == self.id:
            newTerritoryStat = [self.id, amountOfTroops]
            self.mapView.listOfTerritories[territoryName] = newTerritoryStat
            return True
        return False

    # get certain territory stats
    def printTerritroyStats(self, territoryName):
        terrStat = self.mapView.listOfTerritories.get(territoryName)
        print(f'{territoryName} is owned by Player {terrStat[0]}, it has {terrStat[1]} troops')
    
    # adds troops to a territory
    def addTroops(self, territoryName, amountOfTroops):
        return self.setTroops(territoryName, self.mapView.getTroopCount(territoryName) + amountOfTroops)

     # conqueres territory per player
    def conquerTerritory(self, territoryName, numberOfTroops):
        newTerritoryStats = [self.id, numberOfTroops]
        self.mapView.listOfTerritories[territoryName] = newTerritoryStats
