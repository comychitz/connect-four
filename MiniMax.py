import os, sys, time, copy
from Board import *
from Node import *
import random

def minimax(node, depth, maximize, c2 = False):	# maximize is a boolean value
	if not node.is_terminal:
		get_children(node)
	if depth == 0 or node.is_terminal:
		return utility(node, maximize, c2)
	if maximize:
		best_value = float('-inf')
		for child in node.children:
			value = minimax(copy.deepcopy(child), depth - 1, False, c2)
			best_value = max(best_value, value)
		return best_value
	else:
		best_value = float('inf')
		for child in node.children:
			value = minimax(copy.deepcopy(child), depth - 1, True, c2)
			best_value = min(best_value, value)
		return best_value

  
def alpha_beta(node, alpha, beta, depth, maximize, c2 = False):
    if not node.is_terminal:
        get_children(node)
    if depth == 0 or node.is_terminal:
		return utility(node, maximize, c2)
    if maximize:
		for child in node.children:
			alpha = max(alpha, alpha_beta(copy.deepcopy(child), alpha, beta, depth - 1, False, c2 ))
			if beta <= alpha:
				break
		return alpha
    else:
		for child in node.children:
			beta = min(beta, alpha_beta(copy.deepcopy(child), alpha, beta, depth - 1, True, c2 ))
			if beta <= alpha:
				break
		return beta
        
def utility(node, maximize, c2 = False):
	return heuristic(node.board, maximize, c2) - heuristic(node.board, not(maximize), c2)


def heuristic(board, maximize, c2 = False):
	# scores list are constants for assigning score values
	# for 1 in a row, 2 in a row and 3 in a row, respectively
	scores = [0, 5, 30, float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]
	score = 0
	if c2:	
		maximize = not maximize
	if maximize:	
		looking_for = "R"
		not_looking_for = "B"
	else:	
		looking_for = "B"
		not_looking_for = "R"
	# check rows
	for i in reversed(range(board.R)):
		if not row_is_empty(board, i):
			number_in_a_row = 0
			for j in range(board.C):
				if board.board[i][j] == looking_for:
					number_in_a_row += 1
				else:
					if number_in_a_row > 1:
						#print number_in_a_row
						score += scores[number_in_a_row - 1]
					number_in_a_row = 0
				if j == board.C - 1:
					if number_in_a_row > 1:
						score += scores[number_in_a_row - 1]
	# check columns
	for i in range(board.C):
		if not column_is_empty(board, i):
			number_in_a_row = 0
			for j in reversed(range(board.R)):
				if board.board[j][i] == looking_for:
					number_in_a_row += 1
				elif board.board[j][i] == not_looking_for:
					if number_in_a_row > 1:
						score += scores[number_in_a_row - 1]
					number_in_a_row = 0
				else:
					if number_in_a_row > 1:
						score += scores[number_in_a_row - 1]
					number_in_a_row = 0
				if j == 0:
					if number_in_a_row > 1:
						score += scores[number_in_a_row - 1]

	# check diagonals
	# positively sloped diagonals
	for i in range(3):
		start_c = 6
		start_r = i
		number_in_a_row = 0
		while start_c >= 0 and start_r < board.R:
			if board.board[start_r][start_c] == looking_for:
				number_in_a_row += 1
			else:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
				number_in_a_row = 0
			if start_c == 0 or start_r == board.R - 1:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
			start_c -= 1
			start_r += 1
	for i in range(3):
		start_c = 3 + i
		start_r = 0
		number_in_a_row = 0
		while start_c >= 0 and start_r < board.R:
			if board.board[start_r][start_c] == looking_for:
				number_in_a_row += 1
			else:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
				number_in_a_row = 0
			if start_c == 0 or start_r == board.R - 1:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
			start_c -= 1
			start_r += 1
	# negatively sloped diagonals
	for i in range(3):
		start_c = 0
		start_r = i
		number_in_a_row = 0
		while start_c < board.C and start_r < board.R:
			if board.board[start_r][start_c] == looking_for:
				number_in_a_row += 1
			else:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
				number_in_a_row = 0
			if start_c == board.C - 1 or start_r == board.R - 1:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
			start_c += 1
			start_r += 1
	for i in range(3):
		start_c = i
		start_r = 0
		number_in_a_row = 0
		while start_c < board.C and start_r < board.R:
			if board.board[start_r][start_c] == looking_for:
				number_in_a_row += 1
			else:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
				number_in_a_row = 0
			if start_c == board.C - 1 or start_r == board.R - 1:
				if number_in_a_row > 1:
					score += scores[number_in_a_row - 1]
			start_c += 1
			start_r += 1

	return score

def row_is_empty(board, row):
	# function that checks if there has been a piece played 
	# in that respective row
	for i in range(board.C):
		if board.board[row][i] != "-":
			return False
	return True

def column_is_empty(board, column):
	# function that checks if there has been a piece played
	# in that respective row
	for i in reversed(range(board.R)):
		if board.board[i][column] != "-":
			return False
	return True





if __name__ == "__main__":
	os.system("clear")
	b = Board.Board()
	b.place_piece(3,"B")
	b.place_piece(3,"R")
	b.place_piece(4,"B")
	b.place_piece(2,"R")
	b.place_piece(5,"B")
	b.display_board()
	n = Node(b)
	
	print heuristic(b,True)
	
	'''
	get_children(n)
	n.board.display_board()
	print "----------------------------------------"
	for child in n.children:
		child.board.display_board()
		#print utility(child, False)
		print alpha_beta(copy.deepcopy(child), float('-inf'), float('inf'),  1, False)
	
	'''
