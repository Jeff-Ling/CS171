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

from AI import AI
from Action import Action

#import re

class Tile():
	
	def __init__(self, x:int, y:int, hint:int = "."):
		self.x = x
		self.y = y
		self.hint = hint


	def getHint(self) -> int:
		return self.hint


	def setHint(self, num:int):
		self.hint = num



class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# Edited by Y. Song and J. Ling at 2021.07.10

		self.rowDimension = rowDimension - 1
		self.colDimension = colDimension - 1
		self.totalMines = totalMines
		self.startX = startX
		self.startY = startY

		'''self.previousX = 0
		self.previousY = 0'''
		self.curTile = Tile(startX, startY)

		self.whenToLeaveCounter = rowDimension * colDimension - totalMines

		self.firstStep = True

		# Uncovered Tiles
		self.safeTiles = list() # Hint = 0
		self.hintTiles = list() # Hint != 0
		self.flaggedTiles = list() # Suspected Mines

		# Covered Tiles
		self.unexploredTiles = list()
		self.tiles = list()

		self.needUncover = list()
		self.tilesCoveredAroundCurrent = list()

		'''for row in range(0, rowDimension):
			for col in range(0, colDimension):
				#self.unexploredTiles.append([row, col])
				self.tiles.append(Tile(row, col))
		
		for tile in self.tiles:
			self.unexploredTiles.append(tile)'''
			
		# Reverse the range because the row is counted from the bottom
		for row in reversed(range(rowDimension)):
			tileRow = list()
			for col in range(colDimension):
				tileRow.append(Tile(col, row))
			self.tiles.append(tileRow)

        # Every tile is UNEXPLORED yet
		for row in self.tiles:
			for tile in row:
				self.unexploredTiles.append(tile)

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		# Edited by Y. Song and J. Ling at 2021.07.10
		
		if (self.whenToLeaveCounter == 0):
			return Action(AI.Action.LEAVE)		

		if (self.firstStep == True):
			self.firstStep = False

			self.curTile = self.tiles[self.rowDimension - self.startY][self.startX]
			"""self.previousX = self.startX
			self.previousY = self.startY
			print ([self.startX, self.startY])
			"""
			print ("Finish first time")
			print ("curTile Check: ")
			print (self.curTile.x, self.curTile.y)
			self.whenToLeaveCounter -= 1
			return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

		if (number == 0):
			# Append uncovered tiles to list
			print ("So Far So Good! (l_123)")
			self.curTile.setHint(number)
			self.safeTiles.append(self.curTile)

			# Remove the tiles from unexplored tiles list
			self.unexploredTiles.remove(self.curTile)

			# Uncover all tiles around safe tile
			tilesAroundCurrent = self.findNeighbours(self.curTile.x, self.curTile.y)
			"""
			tilesAroundCurrent = []
			tilesAroundCurrent.append([self.previousX, self.previousY + 1])
			tilesAroundCurrent.append([self.previousX, self.previousY - 1])
			tilesAroundCurrent.append([self.previousX + 1, self.previousY])
			tilesAroundCurrent.append([self.previousX + 1, self.previousY + 1])
			tilesAroundCurrent.append([self.previousX + 1, self.previousY - 1])
			tilesAroundCurrent.append([self.previousX - 1, self.previousY])
			tilesAroundCurrent.append([self.previousX - 1, self.previousY + 1])
			tilesAroundCurrent.append([self.previousX - 1, self.previousY - 1])
			"""

			# Ensure action in bound
			for tile in tilesAroundCurrent:
				#f = e + [1] # 1 is hint
				print ("So Far So Good! (l_147)")
				print (tile.x, tile.y)
				if tile.x >= 0 and tile.x <= self.rowDimension and tile.y >= 0 and tile.y <= self.colDimension and tile not in self.needUncover and tile not in self.hintTiles and tile not in self.safeTiles:
					self.needUncover.append(tile)
				"""
				if e[0] < 0 or e[0] > self.rowDimension or e[1] < 0 or e[1] > self.colDimension or e in self.safeTiles or f in self.hintTiles:
					self.needUncover.remove(e)
				"""
				
		elif (number >= 1):
			self.curTile.setHint(number)
			self.hintTiles.append(self.curTile)

			# Remove the tiles from unexplored tiles list
			self.unexploredTiles.remove(self.curTile)


		# Uncover every tiles that are able to click
		if (len(self.needUncover) != 0):
			self.curTile = self.needUncover.pop()
			"""
			self.previousX = self.needUncover[0][0]
			self.previousY = self.needUncover[0][1]
		
			print ([self.previousX, self.previousY])
			print ("needUncover:")
			print (self.needUncover)
			print ("safeTiles:")
			print (self.safeTiles)
			print ("hintTiles:")
			print (self.hintTiles)
			
			self.needUncover.pop(0)
			"""
			print("So Far So Good! (l_179)")
			self.whenToLeaveCounter -= 1
			return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

        # Flag every tiles that are mines
		#if (len(self.flaggedTiles) != 0):
		#	self.curTile = self.flaggedTiles.pop()
		#	return Action(AI.Action.FLAG, self.curTile.x, self.curTile.y)

		if len(self.hintTiles) != 0:
			for i in self.hintTiles:
				neighbours = self.findNeighbour(i.x, i.y)

				neighbours_covered = list()
				for tile in neighbours:
					if tile in self.unexploredTiles:
						neighbours_covered.append(tile)

				if len(neighbours_covered) == i.getHint():
					for y in neighbours_covered:
						self.unexploredTiles.remove(y)
						self.flaggedTiles.append(y)
					'''self.unexploredTiles.remove([neighbours_covered[0][0], neighbours_covered[0][1]])
					self.flaggedTiles.append([neighbours_covered[0][0], neighbours_covered[0][1]])
					self.needUncover = [] + self.unexploredTiles'''
					return Action(AI.Action.FLAG, y.x, y.y)

		# Flag every tiles that are mines
		if (len(self.flaggedTiles) != 0):
			self.curTile = self.flaggedTiles.pop()
			return Action(AI.Action.FLAG, self.curTile.x, self.curTile.y)	
		
	# Helper Function: Return a list that contains the coordinate which is covered around (x,y)
	def findNeighbours (self, x, y) -> list:
		"""
		tileCovered = re.search([x, y], self.unexploredTiles)
		if (tileCovered == True):
			self.tilesCoveredAroundCurrent.append([x, y])
		return tileCovered
		"""
		"""neighbours = []

		for neighbour_x in range (x - 1, x + 2):
			for neighbour_y in range (y - 1, y + 2):
				if 0 <= neighbour_x <= self.rowDimension and 0 <= y <= self.colDimension and (x != neighbour_x and y != neighbour_y):
					neighbours.append(self.tiles[self.rowDimension - y][x])
				print("So Far So Good! (l_227)")
		
		for tile in neighbours:
			print([tile.x, tile.y])

		"""
		tilesAround = []
		tilesAround.append(self.tiles[self.rowDimension - y - 1][x])
		"""tilesAround.append(self.tiles[self.rowDimension - y + 1][x])
		tilesAround.append(self.tiles[self.rowDimension - y][x + 1])
		tilesAround.append(self.tiles[self.rowDimension - y - 1][x + 1])
		tilesAround.append(self.tiles[self.rowDimension - y + 1][x + 1])
		tilesAround.append(self.tiles[self.rowDimension - y][x - 1])
		tilesAround.append(self.tiles[self.rowDimension - y - 1][x - 1])
		tilesAround.append(self.tiles[self.rowDimension - y + 1][x - 1])"""
		"""tilesAround.append([x, y + 1])
		tilesAround.append([x, y - 1])
		tilesAround.append([x + 1, y])
		tilesAround.append([x + 1, y + 1])
		tilesAround.append([x + 1, y - 1])
		tilesAround.append([x - 1, y])
		tilesAround.append([x - 1, y + 1])
		tilesAround.append([x - 1, y - 1])"""

		"""for e in tilesAround:
			if e in self.unexploredTiles:
				neighbours.append(e)"""
		print([self.rowDimension - y - 1, x])
		for tile in tilesAround:
			print([tile.x, tile.y])

		"""print("tilesAround:")
		print(tilesAround)
		print("tileCovered:")
		print(tileCovered)
		"""

		return tilesAround
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################