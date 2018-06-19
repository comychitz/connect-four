import os, sys, time, copy
from Tkinter import *
from Board import *
import timeit

class GUI:
    def __init__(self):
        self.root = Tk()
        self.board = Board()
        self.root.title = ("Connect Four")
        self.size = 59
        self.rows = 6
        self.cols = 7
        self.ovals = []
        self.player_choice = 88
        self.buttons = []
        #self.root.configure(background='yellow')
        self.label = Label(self.root, text="Connect Four", font=("Cambria", 16), fg = "black")
        self.label.pack()
        self.out = Text(self.root, width= 50, height=4)
        self.out.pack(side = BOTTOM)
        #self.out.insert(END, "output")
        self.start = Button(self.root, text="START", width= 20 , height=2, justify=CENTER, command= lambda: self.play())
        self.start.pack(side= BOTTOM)
        
        self.start = Button(self.root, text="DEMO", width= 20 , height=2, justify=CENTER, command= lambda: self.play_c_c())
        self.start.pack(side= BOTTOM)
        
        self.canvas = Canvas(self.root, width = 410, height= 400) #, fill= "yellow")
        for i in range(7):
            for j in range(6):
                self.canvas.create_oval(i*self.size, j*self.size, i*self.size + self.size , j*self.size + self.size, fill="#000000", outline="#000000" )
        self.canvas.pack(side = BOTTOM)
        
        
        for i in range(7):
            b = Button(self.root, text=i, width= 7 , height=2, justify=CENTER, command= lambda item=i : self.play_2(item) , relief=RIDGE)
            b.pack(side= LEFT)
            self.buttons.append(b)
        
        self.first_round = True
        self.try_again = False

    def player_move(self, y):  
        if self.whose_turn() == "Player":        
            self.player_choice = int(y)
            column = int(self.player_choice)
            if self.place(column, "B", "#48CCCD"):
                pass
            else:
                self.out.delete(1.0, END)
                self.out.insert(END, "\nColumn is full, try again.")  
                self.try_again = True
        else:
            self.out.delete(1.0, END)
            self.out.insert(END, "\nIt's not your turn.")   
             
    def whose_turn(self):
        if self.board.previous_symbol == "B":	
            player = "Computer"
        else:	
            player = "Player"
        return player
    
    def computer_move(self, symbol, color, c2 = False):
        node = Node(copy.deepcopy(self.board))
        nodes = []
        scores = []
        get_children(node)
        for child in node.children:
            nodes.append(child)
            if symbol == "B":
                #print " alpha beta"
                scores.append(alpha_beta(copy.deepcopy(child), float("-inf"), float("inf"), 4, False, c2))
            else: 
                #print "minimax"
                scores.append(alpha_beta(copy.deepcopy(child), float("-inf"), float("inf"), 2, False))
                #scores.append(minimax(copy.deepcopy(child), 1, False))
        #print scores
        self.place(nodes[scores.index(max(scores))].board.previous_move, symbol, color)
        self.out.delete(1.0, END)
        self.out.insert(END, "--- Your Turn ---")
    
    def play_c_c(self):
        time_start = time.time()
        self.remove_all()
        self.disable()
        if self.whose_turn() == "Computer" and self.first_round:
            self.out.delete(1.0, END)
            self.computer_move("R", "#FF2400")
            self.first_round = False
        if self.whose_turn() == "Player" and self.first_round:
            self.first_round = False
        while True:
            if not self.board.game_over:
                self.computer_move("B", "#48CCCD", False)
            if self.board.check_winner(self.board.previous_move):
                self.out.delete(1.0, END)
                self.out.insert(END, "\nGAME OVER \n")
                #self.disable()
                break
            if not self.board.game_over:
                self.computer_move("R", "#FF2400")
            if self.board.check_winner(self.board.previous_move):
                self.out.delete(1.0, END)
                self.out.insert(END, "\nGAME OVER \n")
                #self.disable()
                break
            self.root.update()
        self.root.update()
        print time.time() - time_start
            
        
    def play_2(self, y):
        self.try_again = False           
        if not self.board.game_over:
            self.player_move(int(y))
        if self.board.check_winner(self.board.previous_move):
            self.out.delete(1.0, END)
            self.out.insert(END, "\nGAME OVER \n")
            self.disable()
            return
        elif self.try_again == False:
            self.out.delete(1.0, END)
            self.out.insert(END, "--- Computer's Turn ---")
        else: 
            self.out.delete(1.0, END)
            self.out.insert(END, "--- Try again ---")
        #time.sleep(1)
        self.root.update()
        if self.try_again == False:
            if not self.board.game_over:
                self.computer_move("R", "#FF2400")
            if self.board.check_winner(self.board.previous_move):
                self.out.delete(1.0, END)
                self.out.insert(END, "\nGAME OVER \n")
                self.disable()
                return
            else:
                self.out.delete(1.0, END)
                self.out.insert(END, "--- Your Turn ---")
            self.root.update()
            
        
    def place(self, column, symbol, color):
	# places piece from top down, based on the column chosen
        r = self.board.R - 1
        while True:
            if r < 0:
                return False
            elif self.board.board[r][column] == "-":
                self.board.board[r][column] = symbol
                break
            r -= 1
        self.board.previous_move = column
        self.board.previous_symbol = symbol
        #r = r + 1
        oval = self.canvas.create_oval(column*self.size, r*self.size, column*self.size + self.size , r*self.size + self.size, fill=color, outline=color)
        self.ovals.append(oval)        
        self.canvas.pack()
        self.root.update()
        return True         
    
    def remove_all(self):
        self.out.delete(1.0, END)
        self.first_round = True
        self.board = Board()
        for oval in self.ovals:
            self.canvas.delete(oval)
    
    def disable(self):
        for button in self.buttons:
            button['state'] = 'disabled'
            
    def enable(self):
        for button in self.buttons:
            button['state'] = 'normal'
            
    def play(self):
        self.remove_all()
        self.enable()
        if self.whose_turn() == "Computer" and self.first_round:
            self.out.delete(1.0, END)
            self.out.insert(END, "--- Computer's Turn ---")
            self.computer_move("R", "#FF2400")
            self.first_round = False
        if self.whose_turn() == "Player" and self.first_round:
            self.out.delete(1.0, END)
            self.out.insert(END, "--- Your Turn ---")
            self.first_round = False
        
         
    def mainloop(self):    
        #self.root.after(1000, self.play())
        self.root.mainloop()
        
        
        
        
            
if __name__ == "__main__":
    t = GUI()  
    t.mainloop()  
            
