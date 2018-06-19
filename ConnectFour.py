import os, sys, time
from Board import *

# instantiate board object
b = Board()

os.system("clear")
while True:
	c = raw_input("Enter 1 to play against computer, or 0 to see computer vs computer:")
	if c == "1" or c == "0":
		break

if c == "1":
	c = 1
else:
	c = 0

# start main loop of playing
if c == 1:
	while not b.game_over:
		b.play_turn()
		if b.check_winner(b.previous_move):
			os.system("clear")
			b.display_board()
			print "\n\nGAME OVER\n\n"
			break
		elif b.check_if_full():
			print "\n\nGAME OVER\n\n"
else:
	while not b.game_over:
		b.play_c_vs_c(3,3)	# first int is depth for blue computer, second int is depth for red computer
		if b.check_winner(b.previous_move):
			os.system("clear")
			b.display_board()
			print "\n\nGAME OVER\n\n"
			break
		elif b.check_if_full():
			print "\n\nGAME OVER\n\n"

