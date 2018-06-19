# ConnectFour
This program was written as a class project for a graduate Introduction to AI
course at University of California, Irvine. It consists of two contributers. The
main objective is to create a computer program that plays the popular board game
known as Connect Four. See the page http://en.wikipedia.org/wiki/Connect_Four
for rules and history of the game. 

The project was written completely in Python and uses game playing techniques in
the realm of AI known as Minimax with Alpha-beta pruning (which is used to
lessen the search space). Further optimizations are planned to be added in the
near future (mainly multithreading capabilities & better heuristics).

## To Run Using GUI
`python GUI.py`

## To Run on Command Line
`python ConnectFour.py`

### Other Notes
* If running the GUI on a machine that is not windows based, the GUI may not
 look correct due to platform defaults of the Tkinter package.
* To test computer vs computer playing use the test.py file via the command
 line. This cannot be run using an IDE. For example, "python test.py 2 3" will
 play two computers against each other one with depth 2 and one with depth 3 in
 the Minimax algorithm.
