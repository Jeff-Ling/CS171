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

class Constrain():

	def __init__(self, suspectTile = [], hint = 0):
		self.suspectTile = suspectTile
		self.hint = hint

	def compare(self, another_constrain):
		new_constrain = Constrain()

		issubset = True

		this_constrain = self

		for variable in set(this_constrain.suspectTile):
			if variable not in set(another_constrain.suspectTile):
				issubset = False
				break

		if issubset:
			new_constrain.suspectTile = list(set(another_constrain.suspectTile) - set(this_constrain.suspectTile))
			new_constrain.hint = another_constrain.hint - this_constrain.hint

		return new_constrain



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

		self.curTile = Tile(startX, startY)

		self.whenToLeaveCounter = rowDimension * colDimension - totalMines
		self.numMines = 0

		self.firstStep = True

		# Uncovered Tiles
		self.safeTiles = list() # Hint = 0
		self.hintTiles = list() # Hint != 0
		self.flaggedTiles = list() # Suspected Mines

		# Covered Tiles
		self.unexploredTiles = list()

		# A list contains all tiles
		self.tiles = list()

		self.needUncover = list()

		"""
		for row in range(0, rowDimension):
			for col in range(0, colDimension):
				#self.unexploredTiles.append([row, col])
				self.tiles.append(Tile(row, col))
		
		for tile in self.tiles:
			self.unexploredTiles.append(tile)
		"""
			
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

		# If we find all mines, then the rest of unexplored tiles are all safe.
		if (self.numMines == self.totalMines):
			self.needUncover += self.unexploredTiles
			self.unexploredTiles.clear()

		if self.firstStep:
			self.firstStep = False

			self.curTile = self.tiles[self.rowDimension - self.startY][self.startX]
			"""
			self.previousX = self.startX
			self.previousY = self.startY
			print ([self.startX, self.startY])
			print ("Finish first time")
			print ("curTile Check: ")
			print (self.curTile.x, self.curTile.y)
			"""
			self.whenToLeaveCounter -= 1
			return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

		self.curTile.setHint(number)

		if (number == 0):
			# Append uncovered tiles to list
			#self.curTile.setHint(number)
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
				if tile.x >= 0 and tile.x <= self.rowDimension and tile.y >= 0 and tile.y <= self.colDimension and tile not in self.needUncover and tile not in self.hintTiles and tile not in self.safeTiles:
					self.needUncover.append(tile)
				"""
				if e[0] < 0 or e[0] > self.rowDimension or e[1] < 0 or e[1] > self.colDimension or e in self.safeTiles or f in self.hintTiles:
					self.needUncover.remove(e)
				"""
				
		elif (number >= 1):
			#self.curTile.setHint(number)
			self.hintTiles.append(self.curTile)

			# Remove the tiles from unexplored tiles list
			self.unexploredTiles.remove(self.curTile)

		'''# Try to solve the situation when hint > 1
		if tile.getNumber() == len(self.flaggedTiles) and len(self.unexploredTiles) != 0:
			self.safeTiles.extend(self.unexploredTiles)
			self.curTile = self.safeTiles.pop()
			self.exploreTile(self.curTile)
			return Action(AI.Action.UNCOVER, self.__curTile.x, self.__curTile.y)'''


		# Uncover every tiles that are able to click
		if (len(self.needUncover) != 0):
			print("Need Uncover Tiles List")
			for tile in self.needUncover:
				print([tile.x+1, tile.y+1])
			self.curTile = self.needUncover.pop()
			self.whenToLeaveCounter -= 1
			return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)
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


        # Flag every tiles that are mines
		#if (len(self.flaggedTiles) != 0):
		#	self.curTile = self.flaggedTiles.pop()
		#	return Action(AI.Action.FLAG, self.curTile.x, self.curTile.y)

		if len(self.hintTiles) != 0:
			for i in self.hintTiles:
				neighbours = self.findNeighbours(i.x, i.y)
				neighbours_covered = list()
				for tile in neighbours:
					if tile in self.unexploredTiles:
						neighbours_covered.append(tile)

				if len(neighbours_covered) == i.getHint():
					for y in neighbours_covered:
						self.unexploredTiles.remove(y)
						self.flaggedTiles.append(y)
					"""
					self.unexploredTiles.remove([neighbours_covered[0][0], neighbours_covered[0][1]])
					self.flaggedTiles.append([neighbours_covered[0][0], neighbours_covered[0][1]])
					self.needUncover = [] + self.unexploredTiles
					"""
					#return Action(AI.Action.FLAG, y.x, y.y)

		# Flag every tiles that are mines
		if (len(self.flaggedTiles) != 0):
			print("Flagged Tiles List")
			for tile in self.flaggedTiles:
				print([tile.x+1, tile.y+1])
			self.curTile = self.flaggedTiles.pop()
			self.numMines += 1
			return Action(AI.Action.FLAG, self.curTile.x, self.curTile.y)

		# CSP Part
		constrains = []

		for tile in self.hintTiles:
			frontier = False
			flagTile_counter = 0
			neighbours = self.findNeighbours(tile.x, tile.y)
			suspectTile = []
			#print("Current Tile" + str([tile.x + 1, tile.y + 1]))

			for neighbor in neighbours:
				print("Neighbor" + str([neighbor.x + 1, neighbor.y + 1]))
				if neighbor.getHint() == ".":
					"""print("Frontier is true")
					print("added neighbor" + str([neighbor.x + 1, neighbor.y + 1]))"""
					frontier = True
					suspectTile.append(neighbor)	
				elif neighbor.getHint() == -1:
					flagTile_counter += 1
				
			if frontier and tile.getHint() != -1:
				constrain = Constrain(suspectTile, tile.getHint() - flagTile_counter)
				constrains.append(constrain)
				#print("New constrain added")

		constrains = self.solveConstrain(constrains)
		extracted = self.extract(constrains)

		for constrain in extracted:
			if constrain.hint == 1:
				self.flaggedTiles.extend(constrain.suspectTile)

			elif constrain.hint == 0:
				self.needUncover.extend(constrain.suspectTile)

		if self.needUncover:
			self.curTile = self.needUncover.pop()
			self.whenToLeaveCounter -= 1
			return Action(AI.Action.UNCOVER, self.curTile.x, self.curTile.y)

		
	# Helper Function: Return a list of tile that contains the coordinate which is covered around (x,y)
	def findNeighbours (self, x, y) -> list:
		
		neighbours = []

		for neighbour_x in range (x - 1, x + 2):
			for neighbour_y in range (y - 1, y + 2):
				if 0 <= neighbour_x <= self.rowDimension and 0 <= neighbour_y <= self.colDimension and not(x == neighbour_x and y == neighbour_y):
					neighbours.append(self.tiles[self.rowDimension - neighbour_y][neighbour_x])
		
		return neighbours


	def solveConstrain(self, constrains):

		for cs1 in constrains:
			"""print("CS1:")
			CS1 = ""
			for tile in cs1.suspectTile:
				CS1 += str([tile.x + 1, tile.y + 1])
			print(CS1)"""

			for cs2 in constrains:

				"""print("CS2:")
				CS2 = ""
				for tile2 in cs2.suspectTile:
					CS2 += str([tile2.x + 1, tile.y + 1])
				print(CS2)"""

				cs = cs1.compare(cs2)

				if cs not in constrains and len(cs.suspectTile) != 0:
					constrains.append(cs)

				if len(cs.suspectTile) == cs.hint:
					for i in range(len(cs.suspectTile)):
						cs_new = Constrain([cs.suspectTile[i], 1])
						if cs_new not in constrains and cs_new.suspectTile:
							constrains.append(cs_new)

					'''for tile in cs.suspectTile:
						self.flaggedTiles.append(tile)'''

				if len(cs.suspectTile) > 0 and cs.hint == 0:
					for i in range(len(cs.suspectTile)):
						cs_new = Constrain([cs.suspectTile[i], 0])
						if cs_new not in constrains and cs_new.suspectTile:
							constrains.append(cs_new)
					'''for tile in cs.suspectTile:
						self.needUncover.append(tile)'''

		return constrains

	def extract(self, constrains):
		extractred = list()
		for constrain in constrains:
			if len(constrain.suspectTile) == 1:
				extractred.append(constrain)
		return extractred
					


		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################