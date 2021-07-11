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

import re

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

		self.previousX = 0
		self.previousY = 0

		self.whenToLeaveCounter = rowDimension * colDimension - totalMines

		self.firstStep = True

		# Uncovered Tiles
		self.safeTiles = list() # Hint = 0
		self.hintTiles = list() # Hint != 0
		# Covered Tiles
		self.unexploredTiles = list() 
		self.flaggedTiles = list() # Suspected Mines

		self.needUncover = list()
		self.tilesCoveredAroundCurrent = list()

		for i in range(0, rowDimension):
			for j in range(0, colDimension):
				self.unexploredTiles.append([i,j])

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
			self.previousX = self.startX
			self.previousY = self.startY
			print ([self.startX, self.startY])
			print ("Finish first time")
			self.whenToLeaveCounter -= 1
			return Action(AI.Action.UNCOVER, self.startX, self.startY)

		if (number == 0):
			# Append uncovered tiles to list
			self.safeTiles.append([self.previousX, self.previousY])

			# Remove the tiles from unexplored tiles list
			self.unexploredTiles.remove([self.previousX, self.previousY])

			# Uncover all tiles around safe tile
			self.needUncover.append([self.previousX, self.previousY + 1])
			self.needUncover.append([self.previousX, self.previousY - 1])
			self.needUncover.append([self.previousX + 1, self.previousY])
			self.needUncover.append([self.previousX + 1, self.previousY + 1])
			self.needUncover.append([self.previousX + 1, self.previousY - 1])
			self.needUncover.append([self.previousX - 1, self.previousY])
			self.needUncover.append([self.previousX - 1, self.previousY + 1])
			self.needUncover.append([self.previousX - 1, self.previousY - 1])

			# Ensure action in bound
			for e in self.needUncover:
				f = e + [1]
				if e[0] < 0 or e[0] > self.rowDimension or e[1] < 0 or e[1] > self.colDimension or e in self.safeTiles or f in self.hintTiles:
					self.needUncover.remove(e)
				
		elif (number >= 1):
			self.hintTiles.append([self.previousX, self.previousY, number])

			# Remove the tiles from unexplored tiles list
			self.unexploredTiles.remove([self.previousX, self.previousY])


		# Uncover every tiles that are able to click
		if (len(self.needUncover) != 0):
			self.previousX = self.needUncover[0][0]
			self.previousY = self.needUncover[0][1]
			print ([self.previousX, self.previousY])
			print (self.needUncover)
			print (self.safeTiles)
			print (self.hintTiles)
			self.needUncover.pop(0)
			self.whenToLeaveCounter -= 1
			return Action(AI.Action.UNCOVER, self.previousX, self.previousY)

		for i in self.hintTiles:
			Neighbour = self.findNeighbour(i[0], i[1])
			if len(Neighbour) == i[2]:
				self.unexploredTiles.remove([i[0], i[1]])
				self.flaggedTiles.append([i[0], i[1]])
				self.needUncover = [] + self.unexploredTiles
				return Action(AI.Action.FLAG, i[0], i[1])
				
		
	# Helper Function: Return a list that contains the coordinate which is covered around (x,y)
	def findNeighbour (self, x, y):
		tileCovered = re.search([x, y], self.unexploredTiles)
		if (tileCovered == True):
			self.tilesCoveredAroundCurrent.append([x, y])
		return tileCovered
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################