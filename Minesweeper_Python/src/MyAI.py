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

		self.firstStep = True

		# Uncovered Tiles
		self.safeTiles = list() # Hint = 0
		self.hintTiles = list() # Hint != 0
		# Covered Tiles
		self.unexploredTiles = list() 
		self.flaggedTiles = list() # Suspected Mines
		self.needUncover = list()

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
		if (self.firstStep):
			self.firstStep = False
			self.previousX = self.startX
			self.previousY = self.startY
			print ("Finish first time")
			print([self.rowDimension, self.colDimension])
			return Action(AI.Action.UNCOVER, self.startX, self.startY)

		# Append uncovered tiles to list
		if (number == 0):
			self.safeTiles.append([self.previousX, self.previousY])

			self.needUncover.append([self.previousX - 1, self.previousY])
			self.needUncover.append([self.previousX - 1, self.previousY + 1])
			self.needUncover.append([self.previousX, self.previousY + 1])
			self.needUncover.append([self.previousX + 1, self.previousY + 1])
			self.needUncover.append([self.previousX + 1, self.previousY])
			self.needUncover.append([self.previousX + 1, self.previousY - 1])
			self.needUncover.append([self.previousX, self.previousY - 1])
			self.needUncover.append([self.previousX - 1, self.previousY - 1])

			for e in self.needUncover:
				if e[0] < 0 or e[0] >= self.rowDimension or e[1] < 0 or e[1] >= self.colDimension or e in self.safeTiles or e in self.hintTiles:
					self.needUncover.remove(e)
				
		elif (number >= 1):
			self.hintTiles.append([self.previousX, self.previousY, number])

		self.unexploredTiles.remove([self.previousX, self.previousY])


		if (self.needUncover != list()):
			self.previousX = self.needUncover[0][0]
			self.previousY = self.needUncover[0][1]
			print ([self.previousX, self.previousY])
			print (self.needUncover)
			self.needUncover.pop(0)
			return Action(AI.Action.UNCOVER, self.previousX, self.previousY)
		

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################