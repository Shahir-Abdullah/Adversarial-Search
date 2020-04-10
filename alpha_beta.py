from time import time 

MIN = -1000
MAX = 1000
class Agent(object):
    def __init__(self, name):
        self.name = name 
        self.moves = []
        self.score = 0
    def agent_moves(self, moves):
        self.moves = moves 
    def total_score(self, board):
        score = 0
        for box_list in board:
            for box in box_list:
                truth, bar = box.is_box_complete()
                if truth == True and bar.clicked_by == self.name:
                    score += 1
        self.score = score 
        return self.score
    def set_score(self, score):
        self.score = score 


class Bar(object):
    def __init__(self, id):
        self.id = id 
        self.click_status = 0
        self.clicked_by = None 
        self.click_moment = 0

    def clicked(self, agent):
        if self.click_status == 0:
            self.clicked_by = agent.name 
            self.click_status = 1
            self.click_moment = time()
    
    def unclicked(self):
        if self.click_status == 1:
            self.clicked_by = None 
            self.click_status = 0
            self.click_moment = 0
    

    
class Box(object):
    def __init__(self, box_id, bar_a, bar_b, bar_c, bar_d):

        self.bar_a = bar_a
        self.bar_b = bar_b 
        self.bar_c = bar_c 
        self.bar_d = bar_d
        self.bar_list = [self.bar_a, self.bar_b, self.bar_c, self.bar_d] 
        self.box_id = box_id 
        self.completed_by = None 
 
    def update_bars(self, bar_a=None, bar_b=None, bar_c=None, bar_d=None):
        if bar_a != None:
            self.bar_a = bar_a
        if bar_b != None:
            self.bar_b = bar_b 
        if bar_c != None:
            self.bar_c = bar_c 
        if bar_d != None:
            self.bar_d = bar_d

    def is_box_complete(self):
        
        if self.bar_a.click_status == 1 and self.bar_b.click_status == 1 and self.bar_c.click_status == 1 and self.bar_d.click_status == 1:

            if self.bar_a.click_moment == max(self.bar_a.click_moment, self.bar_b.click_moment, self.bar_c.click_moment, self.bar_d.click_moment):
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
            
    def undo_box_completer(self):
        self.completed_by = None  
    
    



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

b1 = Box(1, bars[0], bars[1], bars[2], bars[3])
b2 = Box(2, bars[2], bars[4], bars[5], bars[6])
b3 = Box(3, bars[7], bars[3], bars[8],bars[9])
b4 = Box(4, bars[6], bars[8], bars[10], bars[11])


board = ([
    [b1, b2],
    [b3, b4]
])

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
    if player.total_score(board) > opponent.total_score(board):
        return 10
    elif player.total_score(board) == opponent.total_score(board):
        return 0
    elif player.total_score(board) < opponent.total_score(board):
        return -10
    else:
        return None

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
                        bar.clicked(player)
                        best = max(best, minimax(board, player, opponent, depth+1, not isMax, alpha, beta))
                        alpha = max(alpha, best)
                        bar.unclicked()
                        if beta <= alpha:
                            return best 
                            
                        
        return best 
    else:
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
def findBestMove(board, player, opponent):
    bestVal = MIN
    bestBar = None 
    for box_list in board:
        for box in box_list:
            for bar in box.bar_list:
                if bar.click_status == 0:
                    bar.clicked(player)
                    moveVal = minimax(board, player, opponent, 0, False, MIN, MAX)
                    bar.unclicked()
                    if moveVal > bestVal:
                        bestVal = moveVal
                        bestBar = bar
    

    return bestBar.id
                        
    
    

class State(object):
    def __init__(self, board, bars):
        self.board = board
        self.total_box = len(board) * len(board[0])
        self.total_sides = len(bars)
        self.bars = bars 

    def next_state(self, bar_id, agent):
        
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
                
                t, win_bar = box.is_box_complete()
                if t == True:
                    print("=============> One point by ", win_bar.clicked_by, " box id ", box.box_id)

                    t = False
                    
        
        return self, self.board

if __name__ == "__main__":

    s = State(board, bars)
    agent1 = Agent(input("player 1 : "))
    agent2 = Agent(input("player 2 : "))
    turn = True 
    while True:

        if turn == True:
            a1 = findBestMove(board, agent1, agent2)
            a1 = int(a1)
            print(a1)
            agent_prev_score = agent1.total_score(board)
            s, board = s.next_state(a1, agent1)
            agent_current_score = agent1.total_score(board)
            if agent_current_score == agent_prev_score:
                turn = False 
            print("moves left ======> ", moves_left(board))
             
        else:
            a2 = input(str(agent2.name + "'s move : "))
            a2 = int(a2)
            agent_prev_score = agent2.total_score(board)
            s, board = s.next_state(a2, agent2)
            agent_current_score = agent2.total_score(board)
            if agent_current_score == agent_prev_score:
                turn = True
            print("moves left ======> ", moves_left(board))
            

        if moves_left(board) == 0:
            print("GAME OVER...")
            print(agent1.name, "'s score : ", agent1.total_score(board))
            print(agent2.name, "'s score : ", agent2.total_score(board))
            break


        
            