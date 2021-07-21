# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

import random
from AI import AI
from Action import Action
from collections import Counter


class Tile():

    def __init__(self, location: tuple = (None, None), hint: int = '.', mine: bool = False, isCovered: bool = True, isFlagged: bool = False):
        self.mine = mine
        self.isCovered = isCovered
        self.isFlagged = isFlagged
        self.hint = hint
        self.location = location

    def getHint(self) -> int:
        return self.hint

    def setHint(self, num: int):
        self.hint = num
    
    def uncoverTile(self):
        self.isCovered = False


class Equation:
    def __init__(self, variables = list(), number = 0):
        self.variables = variables
        self.number = number

    def __eq__(self, other):
        def compare(x, y): 
            return Counter(x) == Counter(y)

        if compare(self.variables, other.variables) and self.number == other.number:
            return True
        else:
            return False

    def compare(self, other_eq):
        eq = Equation()

        eq1 = self
        eq2 = other_eq

        if set(eq1.variables).isSubset(set(eq2.variables)):
            eq.variables = list(set(eq2.variables) - set(eq1.variables))
            eq.number = eq2.number - eq1.number

        return eq

class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.exploredTiles = list()       # Already explored tiles
        self.unexploredTiles = list()     # Not yet explored
        self.safeTiles = list()           # Hint = 0
        self.flaggedTiles = list()        # Suspected Mines
        self.curTile = Tile()             
        self.tiles = list()               # A list contains all tiles

        for row in reversed(range(rowDimension)):
            tileRow = list()
            for col in range(colDimension):
                tileRow.append(Tile(location = (col, row)))
            self.tiles.append(tileRow)

        for row in self.tiles:
            for tile in row:
                self.unexploredTiles.append(tile)

        # The first tile starts at the given position. The tile is safe. It gets a number of 0
        self.startTile = Tile(location = (startX, startY), hint = 0, isCovered = False)
        self.tiles[self.rowDimension - 1 -
                     startY][startX] = self.startTile
        self.curTile = self.startTile
        self.exploreTile(self.curTile)

    def getAction(self, number: int) -> "Action Object":
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
        self.curTile.setHint(number)
        self.findSafeTiles(self.curTile)

        # Uncover all the safe tiles
        if self.safeTiles:
            self.curTile = self.safeTiles.pop()
            self.exploreTile(self.curTile)

            return Action(AI.Action.UNCOVER, self.curTile.location[0], self.curTile.location[1])

        elif self.flaggedTiles:
            self.curTile = self.flaggedTiles.pop()
            self.exploreTile(self.curTile)
            self.curTile.flag = True

            return Action(AI.Action.FLAG, self.curTile.location[0], self.curTile.location[1])

        # If no more safe tiles
        else:
            for tile in self.exploredTiles:
                if tile.getHint() > 0:
                    coveredTiles = self.getCoveredTiles(tile)
                    flaggedTiles = self.getFlaggedTiles(tile)

                    if tile.getHint() == len(coveredTiles) + len(flaggedTiles) and len(coveredTiles) != 0:

                        self.curTile = coveredTiles.pop()
                        self.exploreTile(self.curTile)
                        self.curTile.flag = True

                        return Action(AI.Action.FLAG, self.curTile.location[0], self.curTile.location[1])

                    else:

                        if tile.getHint() == len(flaggedTiles) and len(coveredTiles) != 0:
                            self.safeTiles.extend(coveredTiles)
                            self.curTile = self.safeTiles.pop()
                            self.exploreTile(self.curTile)

                            return Action(AI.Action.UNCOVER, self.curTile.location[0], self.curTile.location[1])

        eqs = list()

        for tile in self.exploredTiles:
            frontier = False
            flagCount = 0
            neighbours = self.getNeighbours(tile)
            variables = list()

            for neighbour in neighbours:
                if neighbour.getHint() == '.':
                    frontier = True
                    variables.append(neighbour)

                if neighbour.getHint() == -1:
                    flagCount += 1

            if frontier and tile.getHint() != -1:
                eq = Equation(variables, tile.getHint() - flagCount)
                eqs.append(eq)

        eqs = self.solveConstrain(eqs)
        extracted = self.extractEqs(eqs)

        for eq in extracted:
            if eq.number == 1:
                self.flaggedTiles.extend(eq.variables)

            elif eq.number == 0:
                self.safeTiles.extend(eq.variables)

        if self.safeTiles:
            self.curTile = self.safeTiles.pop()
            self.exploreTile(self.curTile)

            return Action(AI.Action.UNCOVER, self.curTile.location[0], self.curTile.location[1])

        if self.areYouWinning():
            return Action(AI.Action.LEAVE)

        # Best Guess
        if not self.safeTiles:
            min_p = 10
            for x in [z for z in self.exploredTiles if z.number > 0]:
                for t in self.getNeighbours(x):
                    if t.isCovered and not t.isFlagged:
                        coveredNeighbours = [c for c in self.getNeighbours(x) if c.isCovered]
                        if coveredNeighbours:
                            cur_p = int(x.number) / len(coveredNeighbours)
                            if cur_p < min_p:
                                min_p = cur_p
                                self.curTile = t
            self.exploreTile(self.curTile)
            return Action(AI.Action.UNCOVER, self.curTile.location[0], self.curTile.location[1])

        return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

    # returns neighbours' locations
    def getNeighbours(self, tile) -> list:

        cur_x = tile.location[0]
        cur_y = tile.location[1]
        neighbours = list()

        if cur_x != None and cur_y != None:
            for x in range(cur_x - 1, cur_x + 2):
                for y in range(cur_y - 1, cur_y + 2):
                    if -1 < x < self.colDimension and -1 < y < self.rowDimension and not (x == cur_x and y == cur_y):
                        neighbours.append(
                            self.tiles[self.rowDimension - 1 - y][x])

        return neighbours

    def getCoveredTiles(self, tile):
        filtered = list()
        neighbours = self.getNeighbours(tile)

        for tile in neighbours:
            if tile.getHint() == '.':
                filtered.append(tile)

        return filtered

    def getFlaggedTiles(self, tile):
        filtered = list()
        neighbours = self.getNeighbours(tile)

        for tile in neighbours:
            if tile.getHint() == -1:
                filtered.append(tile)

        return filtered

    def areYouWinning(self):
        mineCount = 0
        for row in self.tiles:
            for tile in row:
                if tile.getHint() == -1:
                    mineCount += 1

        return mineCount == self.totalMines

    def findSafeTiles(self, tile):

        if tile.getHint() == 0:
            self.safeTiles.extend(tile for tile in self.getNeighbours(
                tile) if tile not in self.safeTiles and tile not in self.exploredTiles)

        # Update tile info
        tile.uncoverTile()
        self.tiles[self.rowDimension - 1 - tile.location[1]][tile.location[0]] = tile

    def exploreTile(self, tile):
        try:
            self.exploredTiles.append(tile)
            self.unexploredTiles.remove(tile)

        except ValueError:
            pass

    def solveConstrain(self, eqs):

        for eq1 in eqs:
            for eq2 in eqs:

                eq = eq1.compare(eq2)

                if eq not in eqs and eq.variables:
                    eqs.append(eq)

                if len(eq.variables) == eq.number:
                    for i in range(len(eq.variables)):
                        eq_new = Equation([eq.variables[i]], 1)
                        if eq_new not in eqs and eq_new.variables:
                            eqs.append(eq_new)

                if len(eq.variables) > 0 and eq.number == 0:
                    for i in range(len(eq.variables)):
                        eq_new = Equation([eq.variables[i]], 0)
                        if eq_new not in eqs and eq_new.variables:
                            eqs.append(eq_new)

        return eqs

    def extractEqs(self, eqs):
        extracted = list()
        for eq in eqs:
            if len(eq.variables) == 1:
                extracted.append(eq)

        return extracted
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################