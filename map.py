# Based on a RISK game map
# I used this map as a refrence
# https://risk-global-domination.fandom.com/wiki/Simple_World_Map

# the map allows for the conquering of territories
# keeps track of which players, and how many troops per peice of territory is conquered
# checks if a territory CAN be conquered, by checking borders

import random


class Map:

    def __init__(self, playerCount):
        # each variable acts like a pair
        # the first index is the name of territory, the second is an array, index 0 is the player number
        # index 1 is the amount of troopes per territory
        self.listOfTerritories = {
            'Canada': [0, 0],
            'Greenland': [0, 0],
            'United States of America': [0, 0],
            'Mexico': [0, 0],
            'Upper South America': [0, 0],
            'Lower South America': [0, 0],
            'Brazil': [0, 0],
            'United Kingdom': [0, 0],
            'Northern Europe': [0, 0],
            'Mainland Europe': [0, 0],
            'North Africa': [0, 0],
            'Central Africa': [0, 0],
            'South Africa': [0, 0],
            'Middle East': [0, 0],
            'Russia': [0, 0],
            'Central Asia': [0, 0],
            'Southeast Asia': [0, 0],
            'Right Australia': [0, 0],
            'Left Australia': [0, 0]
        }

        # map (in the form of a dic) of map paths/borders
        self.gameMap = {
            'Canada': ["Greenland", 'Russia', 'United States of America'],
            'United States of America': ["Canada", 'Mexico'],
            'Mexico': ['United States of America', 'Upper South America'],
            'Upper South America': ['Mexico', 'Brazil', 'Lower South America'],
            'Lower South America': ['Upper South America', 'Brazil', 'Right Australia'],
            'Brazil': ['Upper South America', 'Lower South America', 'North Africa'],
            'Greenland': ['Canada', 'Northern Europe'],
            'Northern Europe': ['Greenland', 'United Kingdom', 'Russia', 'Mainland Europe'],
            'United Kingdom': ['Northern Europe', 'Mainland Europe'],
            'Mainland Europe': ['United Kingdom', 'Northern Europe', 'Russia', 'Central Asia', 'Middle East'],
            'Middle East': ['Mainland Europe', 'Central Asia', 'SouthEast Asia', 'North Africa', 'Central Africa'],
            'North Africa': ['Brazil', 'Middle East', 'Central Africa', 'Mainland Europe'],
            'Central Africa': ['North Africa', 'Middle East', 'South Africa'],
            'South Africa': ['Central Africa', 'Left Australia'],
            'Russia': ['Northern Europe',  'Mainland Europe', 'Central Asia', 'Canada'],
            'Central Asia': ['Russia', 'Mainland Europe', 'Middle East', 'SouthEast Asia'],
            'SouthEast Asia': ['Central Asia', 'Middle East', 'Right Australia', 'Left Australia'],
            'Right Australia': ['SouthEast Asia', 'Lower South America', 'Left Australia'],
            'Left Australia': ['Right Australia', 'South Africa', 'SouthEast Asia']
        }
        
        # defines the amount of players
        self.playerCount = playerCount

        35 - 5
    


    # itializes a peice of territory
    def intializeMap(self):
        # amount of territory to be aloted per player
        territoryPerPlayer = 19 // self.playerCount

        for i in range(self.playerCount):
            tempTPP = territoryPerPlayer

            # iterates through the listOfCountries
            for key in self.listOfTerritories:
                # gets the player# and the number of troops on the territory
                territoryStats = self.listOfTerritories.get(key)
                playerNumber = territoryStats[0]
                if playerNumber == 0 and tempTPP > 0:
                    playerNumber = i + 1
                    tempTPP = tempTPP - 1
                    territoryStats[0] = playerNumber
                    # updates the player associated with the terrirtory
                    self.listOfTerritories[key] = territoryStats

        # if there is remaining territory it goes to plyaer 1
        for key in self.listOfTerritories:
            if self.listOfTerritories.get(key)[0] == 0:
                self.listOfTerritories.update({key: [1, 0]})

    # conqueres territory per player
    def conquerTerritory(self, territoryName, playerNumber, numberOfTroops):
        newTerritoryStats = [playerNumber, numberOfTroops]
        self.listOfTerritories[territoryName] = newTerritoryStats

    # checks if territory can be conquered per player
    def canBeConquered(self, territoryName, playerNumber):
        tempTerritoryList = self.getPlayerTerritoryList(playerNumber)

        # iterates through the player's countries
        for territory in tempTerritoryList:
            # if a territory the player owns, borders the territroy that is wanted
            if (self.gameMap.get(territory).count(territoryName)):
                return True
        return False

    # returns a list of all countries conquered by player
    def getPlayerTerritoryList(self, playerNumber):
        # iterates through the listOfCountries
        tempterritoryList = []
        for key in self.listOfTerritories:
            tempPlayerNumber = self.listOfTerritories.get(key)[0]
            # if the playernumber with territory is assocated w/ the player number it's added to the list
            if (tempPlayerNumber == playerNumber):
                tempterritoryList.append(key)
        return tempterritoryList

    # returns a list of a players countries w/ solider count
    def getPlayerSoldierList(self, playerNumber):
        # iterates through the listOfCountries
        tempterritoryList = []
        for key in self.listOfTerritories:
            tempPlayerNumber = self.listOfTerritories.get(key)[0]
            # if the playernumber with territory is assocated w/ the player number it's added to the list
            if (tempPlayerNumber == playerNumber):
                territoryName = key
                soldierCount = self.listOfTerritories.get(key)[1]
                territoryInfo = [territoryName, soldierCount]
                tempterritoryList.append(territoryInfo)
        return tempterritoryList

    # returns a matrix, where each row is the territory, the player who has that territory, and
    # the amount of soliders on that territory
    def getMap(self):
        entireMap = []
        for key in self.listOfTerritories:
            territoryName = key
            playerNumer = self.listOfTerritories.get(key)[0]
            amountOfSolider = self.listOfTerritories.get(key)[1]
            territory = [territoryName, playerNumer, amountOfSolider]
            entireMap.append(territory)
        return entireMap

    # returns the amount of soliders on a territory
    def getCountySoliderCount(self, territory):
        if (territory in self.listOfTerritories):
            territoryInfo = self.listOfTerritories.get(territory)
            return territoryInfo[1]
        else:
            return -1

    # get's all the territory that isn't owned by a player

    def getNoneTerritoryList(self, playerNumber):
        # iterates through the listOfCountries
        tempterritoryList = []
        for key in self.listOfTerritories:
            tempPlayerNumber = self.listOfTerritories.get(key)
            # if the playernumber with territory is assocated w/ the player number it's added to the list
            if (tempPlayerNumber != playerNumber):
                tempterritoryList.append(key)
        return tempterritoryList

    # place troops on territory
    def placeTroops(self, territoryName, playerNumber, amountOfTroops):
        if self.listOfTerritories.get(territoryName)[0] == playerNumber:
            newTerritoryStat = [playerNumber, amountOfTroops]
            self.listOfTerritories[territoryName] = newTerritoryStat
            return True
        return False

    # checks if one player controls all the territories
    def oneWinner(self):
        # iterates throughout the playerCount
        for unPlayerNum in range(self.playerCount):
            playerNum = unPlayerNum + 1

            win = True

            # iterates through the list of countries seeing if a playerNumber is
            # not equal to the player who owns that territory
            for key in self.listOfTerritories:
                tempPlayerNumber = self.listOfTerritories.get(key)[0]
                if playerNum != tempPlayerNumber:
                    win = False

            if win:
                return True

        return False

