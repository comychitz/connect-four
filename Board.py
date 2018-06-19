import os, sys, time, copy
from random import randint
from MiniMax import *
from Node import *


class Board:
	def __init__(self):
		self.C = 7	# number of columns on the board
		self.R = 6	# number of rows on the board
		self.WIN = 4 	# number to get in a row to win the game
		self.board = [['-' for x in xrange(self.C)] for x in xrange(self.C)]
		self.previous_move = None	# holds the column # of the previous move
		self.previous_symbol = None	# holds the symbol of the previous move
		self.game_over = False
		self.random_start()

	def random_start(self):
		# function to find out who starts first in the game
		symbols = ['R', 'B'] # red for computer, blue for player
		self.previous_symbol = symbols[randint(0,1)]

	def display_board(self):
		# simply prints out the board
		print "\n"
		for i in range(self.R):
			print str(i) + " " + str(self.board[i])
		numbers = [str(x) for x in range(self.C)]
		print "  -----------------------------------"
		print "  " + str(numbers)
		print "\n"
	
	def play_turn(self):
		os.system("clear")
		if self.previous_symbol == "B":	player = "Computer"
		else:	player = "Player"
		print "--- " + player + "'s Move ---"
		self.display_board()
		if player == "Player":
			while True:
				column = raw_input("\nEnter the column number to place piece: ")
				if not any(c.isalpha() for c in column) and column and int(column) < self.C and int(column) >= 0:
					column = int(column)
					if self.place_piece(column, "B"):
						break
					else:
						print "\nColumn is full, try again."
				else:
					print "\nNot a valid input. Try again."
		else:
			print "\nComputer is thinking..."
			node = Node(copy.deepcopy(self))
			nodes = []
			scores = []
			get_children(node)
			for child in node.children:
				nodes.append(child)
				scores.append(alpha_beta(copy.deepcopy(child), float('-inf'), float('inf'),  4, False))
				#scores.append(minimax(copy.deepcopy(child), 3, False))
			print scores
			self.place_piece(nodes[scores.index(max(scores))].board.previous_move, "R")
			print "\n...Done thinking!"
			time.sleep(1)
	
	def play_c_vs_c(self, l1 = 1, l2 = 1):
		os.system("clear")
		if self.previous_symbol == "B":	player = "Computer1"
		else:	player = "Computer2"
		print "--- " + player + "'s Move ---"
		self.display_board()
		if player == "Computer2":
			print "\nComputer2 is thinking..."
			node = Node(copy.deepcopy(self))
			nodes = []
			scores = []
			get_children(node)
			for child in node.children:
				nodes.append(child)
				scores.append(alpha_beta(copy.deepcopy(child), float('-inf'), float('inf'),  l1, False, True))
				#scores.append(minimax(copy.deepcopy(child), 3, False, True))
			print scores
			self.place_piece(nodes[scores.index(max(scores))].board.previous_move, "B")
			print "\n...Done thinking!"
		else:
			print "\nComputer1 is thinking..."
			node = Node(copy.deepcopy(self))
			nodes = []
			scores = []
			get_children(node)
			for child in node.children:
				nodes.append(child)
				scores.append(alpha_beta(copy.deepcopy(child), float('-inf'), float('inf'),  l2, False))
				#scores.append(minimax(copy.deepcopy(child), 3, False))
			print scores
			self.place_piece(nodes[scores.index(max(scores))].board.previous_move, "R")
			print "\n...Done thinking!"


	def place_piece(self, column, symbol):
		# places piece from top down, based on the column chosen
		r = self.R - 1
		while True:
			if r < 0:
				return False
			elif self.board[r][column] == "-":
				self.board[r][column] = symbol
				break
			r -= 1
		self.previous_move = column
		self.previous_symbol = symbol
		return True

	def check_if_full(self):
		# checks if the board is completely filled
		for i in range(self.C):
			if self.board[0][i] == "-":
				self.game_over = False
				return False
			else:
				self.game_over = True
		return True

	def check_winner(self, column):
		# checks if the last play caused that player to win
		# need to check three scenarios:
		#	1. winning horizontally
		#	2. winning vertically
		#	3. winning diagonally
		# 	this is kind of a brute-force method, may revise and improve later
		row = 0
		while True:
			if row == self.R - 1:
				break
			elif self.board[row][column] != "-":
				break
			row += 1
		last_move = self.board[row][column]
		number_in_a_row = 0
		r = row
		# 1. checking horizontally
		for i in range(self.C):
			if self.board[r][i] == last_move:
				number_in_a_row += 1
			else:
				number_in_a_row = 0
			if number_in_a_row == self.WIN:
				return True
		number_in_a_row = 0
		# 2. checking vertically
		for j in range(self.R):
			if self.board[j][column] == last_move:
				number_in_a_row += 1
			else:
				number_in_a_row = 0
			if number_in_a_row == self.WIN:
				return True
		number_in_a_row = 0
		# 3. check diagonally
		# positive sloped diagonal
		r = row
		c = column
		for i in range(self.R):
			if r + i >= self.R or c - i < 0:
				r = r + i - 1
				c = c - i + 1
				break
		for j in range(self.R):
			if (r - j >= 0 and c + j < self.C) and self.board[r - j][c + j] == last_move:
				number_in_a_row += 1
			else:
				number_in_a_row = 0
			if number_in_a_row == self.WIN:
				return True
		number_in_a_row = 0
		# negative sloped diagonal
		r = row
		c = column
		for i in range(self.R):
			if r + i >= self.R or c + i >= self.C:
				r = r + i - 1
				c = c + i - 1
				break
		for j in range(self.R):
			if (r - j >= 0 and c - j >= 0) and self.board[r - j][c - j] == last_move:
				number_in_a_row += 1
			else:
				number_in_a_row = 0
			if number_in_a_row == self.WIN:
				return True
		self.check_if_full()
		return False
