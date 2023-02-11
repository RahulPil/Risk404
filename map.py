# Based on a RISK game map
# I used this map as a refrence
# https://risk-global-domination.fandom.com/wiki/Simple_World_Map

# the map allows for the conquering of territories
# keeps track of which players, and how many troops per peice of territory is conquered
# checks if a territory CAN be conquered, by checking borders

import random


class Map:
    # each variable acts like a pair
    # the first index is the name of territory, the second is an array, index 0 is the player number
    # index 1 is the amount of troopes per territory
    listOfCountries = {
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
    gameMap = {
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

    def __init__(self):
        self.playerCount = 2

    def __init__(self, playerCount):
        self.playerCount = playerCount

    # itializes a peice of territory
    def intializeMap(self):
        # amount of territory to be aloted per player
        territoryPerPlayer = 19 // self.playerCount

        for i in self.playerCount:
            tempTPP = territoryPerPlayer

            # iterates through the listOfCountries
            for key in self.listOfCountries:
                # gets the player# and the number of troops on the territory
                territoryStats = self.listOfCountries.get(key)
                playerNumber = territoryStats[0]

                if playerNumber == 0:
                    playerNumber = i + 1
                    tempTPP = tempTPP - 1
                    territoryStats[0] = playerNumber
                    # updates the player associated with the terrirtory
                    self.listOfCountries.update(key, territoryStats)

    # conqueres territory per player
    def conquerTerritory(self, territoryName, playerNumber, numberOfTroops):
        newTerritoryStats = [playerNumber, numberOfTroops]
        self.listOfCountries.update(territoryName, newTerritoryStats)

    # checks if territory can be conquered per player
    def canBeConquered(self, territoryName, playerNumber):
        tempCountryList = self.getCountryList(playerNumber)

        # iterates through the player's countries
        for country in tempCountryList:
            # if a country the player owns, borders the territroy that is wanted
            if (self.gameMap.get(country).count(territoryName)):
                return True
        return False

    # get's all the territory owned by a player
    def getCountryList(self, playerNumber):
        # iterates through the listOfCountries
        tempCountryList = []
        for key in self.listOfCountries:
            tempPlayerNumber = self.listOfCountries.get(key)
            # if the playernumber with territory is assocated w/ the player number it's added to the list
            if (tempPlayerNumber == playerNumber):
                tempCountryList.insert(key)
        return tempCountryList

    # get's all the territory that isn't owned by a player
    def getCountryList(self, playerNumber):
        # iterates through the listOfCountries
        tempCountryList = []
        for key in self.listOfCountries:
            tempPlayerNumber = self.listOfCountries.get(key)
            # if the playernumber with territory is assocated w/ the player number it's added to the list
            if (tempPlayerNumber != playerNumber):
                tempCountryList.insert(key)
        return tempCountryList

    # place troops on territory
    def placeTroops(self, territoryName, playerNumber, amountOfTroops):
        newTerritoryStat = [playerNumber, amountOfTroops]
        self.listOfCountries.update(territoryName, newTerritoryStat)
