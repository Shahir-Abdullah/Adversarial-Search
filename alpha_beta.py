from time import time 

MIN = -1000
MAX = 1000
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
        Bar(12)
    ]
# 4 boxes of the board
b1 = Box(1, bars[0], bars[1], bars[2], bars[3])
b2 = Box(2, bars[2], bars[4], bars[5], bars[6])
b3 = Box(3, bars[7], bars[3], bars[8],bars[9])
b4 = Box(4, bars[6], bars[8], bars[10], bars[11])

#board 
board = ([
    [b1, b2],
    [b3, b4]
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
the famous minimax alpha beta prunin. 
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
                        print("-------> clicked by ", box.bar_a.clicked_by)
                    else:
                        print("Bar Already clicked")
                if box.bar_b.id == bar_id:
                    if box.bar_b.click_status == 0:
                        box.bar_b.clicked(agent)
                        print("-------> clicked by ", box.bar_b.clicked_by)
                    else:
                        print("Bar Already clicked")
                if box.bar_c.id == bar_id:
                    if box.bar_c.click_status == 0:
                        box.bar_c.clicked(agent)
                        print("-------> clicked by ", box.bar_c.clicked_by)
                    else:
                        print("Bar Already clicked")
                if box.bar_d.id == bar_id:
                    if box.bar_d.click_status == 0:
                        box.bar_d.clicked(agent)
                        print("-------> clicked by ", box.bar_d.clicked_by)
                    else:
                        print("Bar Already clicked")
                
                t, win_bar = box.is_box_complete() # tells if a box has been completed with the agent name 
                if t == True:
                    print("=============> One point by ", win_bar.clicked_by, " box id ", box.box_id)

                    t = False
                    
        
        return self, self.board
# main function, here the input is performed each turn and after the moves it compiles the result
if __name__ == "__main__":

    s = State(board, bars)
    agent1 = Agent(input("player 1 : "))
    agent2 = Agent(input("player 2 : "))
    turn = True 
    while True:

        if turn == True: # turn value tells whose turn it is. normally it will flip each time except when a player gets a box complete and then he can again make a move. that's when turn bool doesn't get flipped and lets the agent take a move again
            a1 = findBestMove(board, agent1, agent2) # maximizer which here is the AI 
            a1 = int(a1)
            print(a1)
            agent_prev_score = agent1.total_score(board)
            s, board = s.next_state(a1, agent1)
            agent_current_score = agent1.total_score(board)
            if agent_current_score == agent_prev_score: # finds out if the agent got a point by comparing the prev and current score, if changes that means the turn bool won't flip 
                turn = False 
            print("moves left ======> ", moves_left(board))
             
        else:
            a2 = input(str(agent2.name + "'s move : ")) # minimizer or the human 
            a2 = int(a2)
            agent_prev_score = agent2.total_score(board)
            s, board = s.next_state(a2, agent2)
            agent_current_score = agent2.total_score(board)
            if agent_current_score == agent_prev_score:
                turn = True
            print("moves left ======> ", moves_left(board))
            

        if moves_left(board) == 0: # compilation of the game result. 
            print("GAME OVER...")
            print(agent1.name, "'s score : ", agent1.total_score(board))
            print(agent2.name, "'s score : ", agent2.total_score(board))
            break


        
            