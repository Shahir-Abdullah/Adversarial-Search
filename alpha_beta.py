from time import time 
import tkinter as tk 
import time as time_to_sleep
from functools import partial # for calling button functions with arguments https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter

MIN = -1000
MAX = 1000
a2 = 0
turn = True 
clicked = False 
random_moves = 5
agent1 = None 
agent2 = None 
i = 0
#colors
clicked_bar_color_human = "#0DA6AB"
clicked_bar_color_ai = "#566573"
unclicked_bar_color = "#1EE0E6"
box_complete_color_by_AI = "#566573"
box_complete_color_by_Human = "#0DA6AB"
box_color = "#FDFEFE"
enter_btn_color = "#17B974"
label_color="#FFFFFF"
frame_color = "#2471A3"

window = tk.Tk()
#title of the window
window.title("Dot Box Game")
#resizable and responsive window
window.rowconfigure([0,1], minsize=5, weight=1) #weight 0 means non resizable #Take a look at line 6 more closely. The minsize parameter of .rowconfigure() is set to 800 and weight is set to 1. The first argument is 0, which sets the height of the first row to 800 pixels and makes sure that the height of the row grows proportionally to the height of the window. There’s only one row in the application layout, so these settings apply to the entire window.
window.columnconfigure(1, minsize=2, weight=1) #Here, you use .columnconfigure() to set the width and weight attributes of the column with index 1 to 800 and 1, respectively:. Remember, row and column indices are zero-based, so these settings apply only to the second column. By configuring just the second column, the text box will expand and contract naturally when the window is resized, while the column containing the buttons will remain at a fixed width.
#border effects
border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

#taskbar frame
frame_taskbar = tk.Frame(
    master=window,
    relief=tk.GROOVE,
    bg = frame_color,
    borderwidth=2
)
#entry section frame
entry_frame = tk.Frame(
    master=frame_taskbar,
    relief = tk.SUNKEN,
    borderwidth=2
)

#label for AI name entry
lbl_ai = tk.Label(master=entry_frame, text="Enter AI's name : ")
#entry for AI
ent_ai = tk.Entry(master=entry_frame, width=10)
#label for human name entry
lbl_human = tk.Label(master=entry_frame, text="Enter your name : ")
#entry for human name
ent_human = tk.Entry(master=entry_frame, width=10)
#button for agent's name input
enter_button = tk.Button(
    master = entry_frame,
    text="Start",
    bg = enter_btn_color,
    fg = "white"
)
#geometry manager to set up entry frame
lbl_ai.grid(row=0, column=0, sticky="nwse", padx=5, pady=5)
ent_ai.grid(row=0, column=1, sticky="nwse", padx=5, pady=5)
lbl_human.grid(row=1, column=0, sticky="nwse", padx=5, pady=5)
ent_human.grid(row=1, column=1, sticky="nwse", padx=5, pady=5)
enter_button.grid(row=2, column=1, sticky="sw", padx=5, pady=5)
#labels for taskbar
lbl_game_name=tk.Label(master=frame_taskbar, text="Dot Box")
lbl_player1=tk.Label(master=frame_taskbar, text="Player 1 :")
lbl_player1_name=tk.Label(master=frame_taskbar, text="AI")
lbl_points_player1=tk.Label(master=frame_taskbar, text="Points :")
lbl_point_table_player1=tk.Label(master=frame_taskbar, text="0")
lbl_player2=tk.Label(master=frame_taskbar, text="Player 2 :")
lbl_player2_name=tk.Label(master=frame_taskbar, text="Human")
lbl_points_player2=tk.Label(master=frame_taskbar, text="Points :")
lbl_point_table_player2=tk.Label(master=frame_taskbar, text="0")
lbl_game_result=tk.Label(master=frame_taskbar, text="   ")

#geometry manager to set up the taskbar frame 
lbl_game_name.grid(row=0, column=0, sticky="wnes", padx=5, pady=5)
lbl_player1.grid(row=1, column=0, sticky="w", padx=5, pady=5)
lbl_player1_name.grid(row=1, column=1, sticky="e", padx=5, pady=5)
lbl_points_player1.grid(row=2, column=0, sticky="w", padx=5, pady=5)
lbl_point_table_player1.grid(row=2, column=1, sticky="we", padx=5, pady=5)
lbl_player2.grid(row=3, column=0, sticky="w", padx=5, pady=5)
lbl_player2_name.grid(row=3, column=1, sticky="e", padx=5, pady=5)
lbl_points_player2.grid(row=4, column=0, sticky="w", padx=5, pady=5)
lbl_point_table_player2.grid(row=4, column=1, sticky="we", padx=5, pady=5)
lbl_game_result.grid(row=5, column=0, sticky="wens", padx=5, pady=5)

#game frame
box_container = tk.Frame(
    master=window,
    relief=tk.SUNKEN,
    borderwidth=2
)
#gui bars list
gui_bars = []
#box dictornary
gui_box = {}
# game frame 
def enter_row_column():
    r = 5
    c = 5
    '''
    n = r*c  
    if n >= 2:
        n = (n*4) - (((n-2)/2)*3) - (n%2) - 1
    else:
        n = 4 
    '''
    bar_id = 1
    total_bars = 60 
    r = r + (r + 1)
    c = c + (c + 1)
    box_id = 1
    for i in range(0, r):
        for j in range(0, c):
            if i%2 == 0 and j%2 == 1:
                #horizontal bar
                b_i = str(bar_id)
                click_funct_with_id = partial(bar_click_human, b_i)
                horizontal_bar = tk.Button(
                    master=box_container,
                    text=b_i,
                    fg= unclicked_bar_color,
                    bg= "white",
                    width="8",
                    height="1",
                    command=click_funct_with_id
                )
                bar_id += 1
                gui_bars.append(horizontal_bar)
                horizontal_bar.grid(row=i, column=j, sticky="nw", pady=1)
                total_bars -= 1
            elif i%2 == 1 and j%2 == 0:
                b_i = str(bar_id)
                #vertical bar 
                click_funct_with_id = partial(bar_click_human, b_i)
                vertical_bar = tk.Button(
                    master=box_container,
                    text=b_i,
                    fg= unclicked_bar_color,
                    bg= "white",
                    width="1",
                    height="4",
                    command=click_funct_with_id
                )
                
                gui_bars.append(vertical_bar)
                vertical_bar.grid(row=i, column=j, sticky="w", padx=2)
                bar_id += 1
                
            elif i%2==1 and j%2==1:
                #box
                box = tk.Label(master=box_container, bg=box_color, fg="white")
                gui_box[box_id] = box 
                box_id += 1
                box.grid(row=i, column=j, sticky="wnes", padx=1)

# the initial window for taking player's names 
def name_entry():
    frame_taskbar.grid(row=0, column=0, sticky="enws", padx=5, pady=5)
    entry_frame.grid(row=6, column=0, sticky="ws", padx=5, pady=5)
# this function will put the game frame into window board   
def draw_GUI():
    global agent1
    global agent2
    agent1_name = ent_ai.get()
    agent2_name = ent_human.get()
    agent1 = Agent(agent1_name)
    agent2 = Agent(agent2_name)
    lbl_player1_name["text"] = agent1.name 
    lbl_player2_name["text"] = agent2.name 

    frame_taskbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    enter_row_column()
    box_container.grid(row=0, column=1, sticky="w", padx=5, pady=5)

class Agent(object):
    def __init__(self, name):
        self.name = name 
        self.moves = []
        self.score = 0
    def agent_moves(self, moves): #the moves the agent took. not needed now but may in the future 
        self.moves = moves 
    def total_score(self, board): #returns the total score when the board is given as parameter
        score = 0
        for box_list in board:
            for box in box_list:
                truth, bar = box.is_box_complete()
                if truth == True and bar.clicked_by == self.name:
                    score += 1
        self.score = score 
        return self.score
    def set_score(self, score): # set method 
        self.score = score 

#bar class, a board is made of list of box class object. a box class is made of 4 bar objects 
class Bar(object):
    def __init__(self, id):
        self.id = id 
        self.click_status = 0 # if 0 means not clicked yet, 1 means clicked 
        self.clicked_by = None # the agent who clicked 
        self.click_moment = 0 # it keeps the time in float value which is needed to know the last bar selected from the completed box

    def clicked(self, agent): # click method that sets the object attributes 
        if self.click_status == 0:
            self.clicked_by = agent.name 
            self.click_status = 1
            self.click_moment = time() # time method that returs a float value
    
    def unclicked(self): # this method is not for the game, it is for minimax algorithm that needs to undo the bars that were clicked in utility calculation 
        if self.click_status == 1:
            self.clicked_by = None 
            self.click_status = 0
            self.click_moment = 0
    

#Box class
class Box(object):
    def __init__(self, box_id, bar_a, bar_b, bar_c, bar_d):

        self.bar_a = bar_a # has 4 Bar objects
        self.bar_b = bar_b 
        self.bar_c = bar_c 
        self.bar_d = bar_d
        self.bar_list = [self.bar_a, self.bar_b, self.bar_c, self.bar_d] # this is silly, only made to use it when a common task needed to be done on all of it like in the minimax algorithm you will see later
        self.box_id = box_id # box id if needed 
        self.completed_by = None # the agent's name who got the point of completing the box
 
    def update_bars(self, bar_a=None, bar_b=None, bar_c=None, bar_d=None): # not using right at this moment
        if bar_a != None:
            self.bar_a = bar_a
        if bar_b != None:
            self.bar_b = bar_b 
        if bar_c != None:
            self.bar_c = bar_c 
        if bar_d != None:
            self.bar_d = bar_d

    def is_box_complete(self): # method which checks if all the bars have been clicked, if yes then returns True and the last bar to make the box complete
        
        if self.bar_a.click_status == 1 and self.bar_b.click_status == 1 and self.bar_c.click_status == 1 and self.bar_d.click_status == 1:

            if self.bar_a.click_moment == max(self.bar_a.click_moment, self.bar_b.click_moment, self.bar_c.click_moment, self.bar_d.click_moment): # the time of clicking the bar is used to find out the last bar clicked 
                self.completed_by = self.bar_a.clicked_by 
                return True, self.bar_a 
            elif self.bar_b.click_moment == max(self.bar_a.click_moment, self.bar_b.click_moment, self.bar_c.click_moment, self.bar_d.click_moment):
                self.completed_by = self.bar_b.clicked_by 
                return True, self.bar_b
            elif self.bar_c.click_moment == max(self.bar_a.click_moment, self.bar_b.click_moment, self.bar_c.click_moment, self.bar_d.click_moment):
                self.completed_by = self.bar_c.clicked_by 
                return True, self.bar_c
            elif self.bar_d.click_moment == max(self.bar_a.click_moment, self.bar_b.click_moment, self.bar_c.click_moment, self.bar_d.click_moment):
                self.completed_by = self.bar_d.clicked_by 
                return True, self.bar_d
        else:
            return False, None 
            
    def undo_box_completer(self): # not needed right now, clears the box data
        self.completed_by = None   
    
    


# list of bars 
bars = [
        Bar(1),
        Bar(2), 
        Bar(3),
        Bar(4),
        Bar(5),
        Bar(6),
        Bar(7),
        Bar(8),
        Bar(9),
        Bar(10),
        Bar(11),
        Bar(12),
        Bar(13),
        Bar(14),
        Bar(15),
        Bar(16), 
        Bar(17),
        Bar(18),
        Bar(19),
        Bar(20),
        Bar(21),
        Bar(22),
        Bar(23),
        Bar(24),
        Bar(25),
        Bar(26),
        Bar(27),
        Bar(28),
        Bar(29),
        Bar(30), 
        Bar(31),
        Bar(32),
        Bar(33),
        Bar(34),
        Bar(35),
        Bar(36),
        Bar(37),
        Bar(38),
        Bar(39),
        Bar(40),
        Bar(41),
        Bar(42),
        Bar(43),
        Bar(44),
        Bar(45),
        Bar(46),
        Bar(47),
        Bar(48),
        Bar(49),
        Bar(50),
        Bar(51),
        Bar(52),
        Bar(53),
        Bar(54),
        Bar(55),
        Bar(56),
        Bar(57),
        Bar(58),
        Bar(59),
        Bar(60)

    ]
# 25 boxes of the board
b1 = Box(1, bars[0], bars[5], bars[6], bars[11])
b2 = Box(2, bars[1], bars[6], bars[7], bars[12])
b3 = Box(3, bars[2], bars[7], bars[8],bars[13])
b4 = Box(4, bars[3], bars[8], bars[9], bars[14])
b5 = Box(5, bars[4], bars[9], bars[10], bars[15])

b6 = Box(6, bars[11], bars[16], bars[17], bars[22])
b7 = Box(7, bars[12], bars[17], bars[18], bars[23])
b8 = Box(8, bars[13], bars[18], bars[19], bars[24])
b9 = Box(9, bars[14], bars[19], bars[20], bars[25])
b10 = Box(10, bars[15], bars[20], bars[21], bars[26])

b11 = Box(11, bars[22], bars[27], bars[28], bars[33])
b12 = Box(12, bars[23], bars[28], bars[29], bars[34])
b13 = Box(13, bars[24], bars[29], bars[30], bars[35])
b14 = Box(14, bars[25], bars[30], bars[31], bars[36])
b15 = Box(15, bars[26], bars[31], bars[32], bars[37])

b16 = Box(16, bars[33], bars[38], bars[39], bars[44])
b17 = Box(17, bars[34], bars[39], bars[40], bars[45])
b18 = Box(18, bars[35], bars[40], bars[41], bars[46])
b19 = Box(19, bars[36], bars[41], bars[42], bars[47])
b20 = Box(20, bars[37], bars[42], bars[43], bars[48])

b21 = Box(21, bars[44], bars[49], bars[50], bars[55])
b22 = Box(22, bars[45], bars[50], bars[51], bars[56])
b23 = Box(23, bars[46], bars[51], bars[52], bars[57])
b24 = Box(24, bars[47], bars[52], bars[53], bars[58])
b25 = Box(25, bars[48], bars[53], bars[54], bars[59])



#board 
board = ([
    [b1, b2, b3, b4, b5],
    [b6, b7, b8, b9, b10],
    [b11, b12, b13, b14, b15],
    [b16, b17, b18, b19, b20],
    [b21, b22, b23, b24, b25]
])
# function that calculate how many moves are left 
def moves_left(board):
        
        moves = 0
        
        for box_list in board:
            for box in box_list:

                if box.bar_a.click_status == 0:
                    moves += 1
                if box.bar_b.click_status == 0:
                    moves += 1
                if box.bar_c.click_status == 0:
                    moves += 1
                if box.bar_d.click_status == 0:
                    moves += 1
                
        return moves 
    


#evaluation function 
def board_evaluation(board, player, opponent):
    if player.total_score(board) > opponent.total_score(board): # win
        return 10
    elif player.total_score(board) == opponent.total_score(board): # draw
        return 0
    elif player.total_score(board) < opponent.total_score(board): # lose
        return -10
    else:
        return None # still game is going on


'''
the famous minimax alpha beta pruning. 
maximizer wants to increase the alpha as much as it can without crossing the beta from previous node. 
minimizer wants to decrease the beta as much as it can without going below alpha from previous node. 
'''
def minimax(board, player, opponent, depth, isMax, alpha, beta):
    score = board_evaluation(board, player, opponent)

    if score == 10 or score == -10:
        return score 
    if moves_left(board) == 0:
        return 0

    if isMax == True:
        best = MIN
        for box_list in board:
            for box in box_list:
                for bar in box.bar_list:
                    if bar.click_status == 0: 
                        bar.clicked(player) # clicks an untouched bar and then puts the board into minimax to see what is the end result. does that for every unclicked bar and then selects the best outcome bar
                        best = max(best, minimax(board, player, opponent, depth+1, not isMax, alpha, beta))
                        alpha = max(alpha, best) # alpha is the best value it gets 
                        bar.unclicked() # undo the click status because it was a simulation for calculating the utility it's not a move 
                        if beta <= alpha:
                            '''
                            if the alpha gets over the beta given from the prev min layer 
                            that means that min layer will never choose this alpha cause it won't let maximizer win 
                            and let the game go onto an end result where maximizer tops minimizer level. 
                            that's why the loop aborts cause the best result won't happen
                            so why bother calculating the rest of the nodes in that branch 

                                    min <= 5 // after completing left brach this level knows it will get maximum 5 as it is min level 
                                        / \ 
                                max =  5   max >= 6 // so after knowing that this level will generate at least 6 the upper level won't come here cause it already know if it choses left it will get at best 5. that why it will return from max level getting best result 6 which will be eventually discarded since uper level's beta is 5
                                      / \  /  \ 
                                     3  5  6  (this won't even be counted, even if it was 1, becasue max would never chosse it)
                            
                            
                            '''
                            return best # return value 6 according to the above example 
                           
                        
        return best 
    else: # min level calculation here beta will try to decrease as much as it can without going below the alpha level provide by the upper Max level, cause if if goes below alpha the max level won't come to this branch. 
        best = MAX
        for box_list in board:
            for box in box_list:
                for bar in box.bar_list:
                    if bar.click_status == 0:
                        bar.clicked(player)
                        best = min(best, minimax(board, player, opponent, depth+1, not isMax, alpha, beta))
                        beta = min(beta, best)
                        bar.unclicked()
                        if beta <= alpha:
                            return best 
        return best


#will return the bar id    
# this funciton actually tells the AI what move should it take. 
# it call minmax for every bar and then calculates the value returned by the minmax. the move with the highest score then gets executed             
def findBestMove(board, player, opponent):
    bestVal = MIN
    bestBar = None 
    for box_list in board:
        for box in box_list:
            for bar in box.bar_list:
                if bar.click_status == 0:
                    bar.clicked(player)
                    moveVal = minimax(board, player, opponent, 0, False, MIN, MAX) # starts with false cause it's other persons turn 
                    bar.unclicked()
                    if moveVal > bestVal: # compares  the value returned by min max applied on every empty bar
                        bestVal = moveVal
                        bestBar = bar
    

    return bestBar.id # returns the bar that gives the best optimal move 
                        
def randomMove(board, player, opponent):
    for box_list in board:
        for box in box_list:
            if box.bar_c.click_status == 0:
                return box.bar_c.id    
    
# state class. which has a board, and the next state generation function 
class State(object):
    def __init__(self, board, bars):
        self.board = board
        self.total_box = len(board) * len(board[0]) # keeps the count of boxes in the board 
        self.total_sides = len(bars) # sides or bars 
        self.bars = bars 

    def next_state(self, bar_id, agent): # when an bar id is given, the next_state generates the board with updating the click status of the given bar id and returns the board 
        
        for box_list in self.board:
            for box in box_list:
                
                if box.bar_a.id == bar_id:
                    if box.bar_a.click_status == 0:
                        box.bar_a.clicked(agent)
                        #print("-------> clicked by ", box.bar_a.clicked_by)
                    else:
                        pass 
                        #print("Bar Already clicked")
                if box.bar_b.id == bar_id:
                    if box.bar_b.click_status == 0:
                        box.bar_b.clicked(agent)
                        #print("-------> clicked by ", box.bar_b.clicked_by)
                    else:
                        pass 
                        #print("Bar Already clicked")
                if box.bar_c.id == bar_id:
                    if box.bar_c.click_status == 0:
                        box.bar_c.clicked(agent)
                        #print("-------> clicked by ", box.bar_c.clicked_by)
                    else:
                        pass 
                        #print("Bar Already clicked")
                if box.bar_d.id == bar_id:
                    if box.bar_d.click_status == 0:
                        box.bar_d.clicked(agent)
                        #print("-------> clicked by ", box.bar_d.clicked_by)
                    else:
                        pass 
                        #print("Bar Already clicked")
                
                t, win_bar = box.is_box_complete() # tells if a box has been completed with the agent name 
                if t == True:
                    if win_bar.clicked_by == agent1.name:
                        gui_box[box.box_id]["bg"] = box_complete_color_by_AI
                    elif win_bar.clicked_by == agent2.name:
                        gui_box[box.box_id]["bg"] = box_complete_color_by_Human
                    #print("=============> One point by ", win_bar.clicked_by, " box id ", box.box_id)
                    t = False
                    
        
        return self, self.board
#initializatoin of state
s = State(board, bars)

#change bar color
def change_color(id, agent):
    for b in gui_bars:
        
        if b["text"] == id and agent.name == agent1.name:
            b["bg"] = clicked_bar_color_ai 
            #print("changing color")
            return
        if b["text"] == id and agent.name == agent2.name:
            b["bg"] = clicked_bar_color_human
            #print("changing color")
            return  
def show_bars(board):
    for box_list in board:
        for box in box_list:
            if box.bar_a.click_status == 1:
                print(box.bar_a.id)
            if box.bar_b.click_status == 1:
                print(box.bar_b.id)
            if box.bar_c.click_status == 1:
                print(box.bar_c.id)
            if box.bar_d.click_status == 1:
                print(box.bar_d.id)

#click function by human
def bar_click_human(id):
    global turn
    global board 
    global s
    global i
    global random_moves 
    a2 = int(id)
    
         
    if turn == True and moves_left(board) > 0:
            
            #a2 = input(str(agent2.name + "'s move : ")) # minimizer or the human 
            #a2 = int(a2)
            #print("human's turn")
            agent_prev_score = agent2.total_score(board)
            s, board = s.next_state(a2, agent2)
            #show_bars(board)
            change_color(id, agent2)
            agent_current_score = agent2.total_score(board)
            
            if agent_current_score == agent_prev_score:
                turn = False 
                lbl_game_result["text"] = "AI's turn" 
            else:
                lbl_game_result["text"] = "Your turn"  
            #print("moves left ======> ", moves_left(board)) 

    if turn == False and moves_left(board) > 0: # turn value tells whose turn it is. normally it will flip each time except when a player gets a box complete and then he can again make a move. that's when turn bool doesn't get flipped and lets the agent take a move again
            #print("ai's turn", i)
            while turn == False and moves_left(board) > 0:
                lbl_game_result["text"] = "AI's turn"
                if i <= random_moves:
                    a1 = randomMove(board, agent1, agent2)
                    
                    a1 = int(a1)
                    i += 1
                    #print("---------------------------------------- i = ", i)
                else:
                    a1 = findBestMove(board, agent1, agent2) # maximizer which here is the AI 
                    
                    a1 = int(a1)
                #print(a1)
                change_color(str(a1), agent1)
                agent_prev_score = agent1.total_score(board)
                s, board = s.next_state(a1, agent1)
                
                #show_bars(board)
                agent_current_score = agent1.total_score(board)
                if agent_current_score == agent_prev_score: # finds out if the agent got a point by comparing the prev and current score, if changes that means the turn bool won't flip 
                    turn = True
                    lbl_game_result["text"] = "Your turn"
                else:
                    lbl_game_result["text"] = "AI's turn" 
               #print("moves left ======> ", moves_left(board)) 
                 
    if moves_left(board) == 0: # compilation of the game result. 
        lbl_game_result["text"] = "GAME OVER"
        time_to_sleep.sleep(2.0)
        if agent1.total_score(board) < agent2.total_score(board):
            lbl_game_result["text"] = "You Win!"
        elif agent1.total_score(board) > agent2.total_score(board):
            lbl_game_result["text"] = "AI Wins!"
        else:
            lbl_game_result["text"] = "It's a Draw"

    
        
    lbl_point_table_player1["text"] = str(agent1.total_score(board))
    lbl_point_table_player2["text"] = str(agent2.total_score(board))
    #print(id, "returned", turn)


# main function
if __name__ == "__main__":
    enter_button["command"] = draw_GUI
    name_entry()
    i = 0
    turn = True 
    #without mainloop, nothing will be shown
    window.mainloop()  

        
 
            

