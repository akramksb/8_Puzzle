from copy import deepcopy
from settings import *

class Puzzle:
    def __init__(self, current_state, goal_state):
        self.state = current_state
        self.goal_state = goal_state

    def findEmptySquare(self):
        for row_index in range( len(self.state)):
            for col_index in range( len( self.state[0] )):
                if self.state[row_index][col_index] == 0:
                    return ( row_index, col_index )

    def isGoalState(self):
        return self.state == self.goal_state

    def move(self, direction_str):
        ''' 0 : not a legal move , 1 : legal move '''
        direction = DIRECTIONS[direction_str]
        # get empty square coordinates
        emptySquare = self.findEmptySquare()
        # get empty square new coordinates
        newEmptySqaure = [ emptySquare[0]+direction[0],
                        emptySquare[1]+direction[1] ]
        # check is legal move
        if 0 <= newEmptySqaure[0] < len(self.state)\
            and 0 <= newEmptySqaure[1] < len(self.state[0]) :
            # swap empty square oldPos with newPos
            self.state[ newEmptySqaure[0] ][ newEmptySqaure[1] ], self.state[ emptySquare[0] ][emptySquare[1]]\
                = self.state[ emptySquare[0] ][emptySquare[1]], self.state[ newEmptySqaure[0] ][ newEmptySqaure[1] ]
            return 1
        return 0
    
    def show(self):
        prefix = ""
        if len(self.state) > 3 :
            prefix = " "
        for row in self.state:
            for square in row:
                if square == 0 : print( prefix+" ", end = " " )
                else : print( square if square>9 else prefix+str(square), end = " " )
            print()

def main():
    input_to_dir = { "a":"LEFT", "s":"DOWN","d":"RIGHT","w":"UP" }
    puzzle = Puzzle(INITIAL_STATE, GOAL_STATE)
    puzzle.show()
    while not puzzle.isGoalState():
        print()
        input_dir = input( ">" )
        print()
        if input_dir not in input_to_dir:
            print("move with w,a,s,d")
            continue
        puzzle.move( input_to_dir[input_dir] )
        puzzle.show()
    
if __name__ == "__main__":
    main()