# this file is solely for observing the behavior of computer vs computer 
# with changing depths

import os, sys, time
from Board import *

# instantiate board object
b = Board()

# computer 1 is red
# computer 2 is blue
# to run this file do the following (on a Unix/Linux machine):
#	python test.py 'depth_for_blue' 'depth_for_red'
# example runs:
#	python test.py 1 2
#	python test.py 3 4
# 	python test.py 2 6
#	i think you get the idea...

while not b.game_over:
	b.play_c_vs_c(int(sys.argv[1]),int(sys.argv[2]))	# first int is depth for blue computer, second int is depth for red computer
	if b.check_winner(b.previous_move):
		os.system("clear")
		b.display_board()
		print "\n\nGAME OVER\n\n"
		break
	elif b.check_if_full():
		print "\n\nGAME OVER\n\n"

