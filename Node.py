import os, sys, time
import Board 
import copy


class Node:
	def __init__(self, board_config = None):	# board config is an instance of the board class
		self.board = Board.Board()
		self.board = board_config
		self.value = 0
		self.is_terminal = False
		self.find_if_terminal()
		self.children = []
	
	
	def find_if_terminal(self):
		if not self.board.previous_move:
			self.is_terminal = False
			return
		if self.board.check_winner(self.board.previous_move):
			self.is_terminal = True
			return
		if self.board.check_if_full():
			self.is_terminal = True


def get_children(node):
	if node.board.previous_symbol == "B":	symbol = "R"
	else:	symbol = "B"
	for i in [3,2,4,5,1,6,0]:
		temp = Node(copy.deepcopy(node.board))
		if temp.board.place_piece(i, symbol):
			node.children.append(temp)


if __name__ == "__main__":
	b = Board.Board()
	n = Node(b)
	get_children(n)
	for child in n.children:
		child.board.display_board()
