from copy import deepcopy
from game import *
import time

class Node:
    def __init__(self, state, parent_node, g, h, move):
        self.state = state
        self.parent_node = parent_node
        self.g = g
        self.h = h
        self.move = move
        self.id = 0
        for row in self.state:
            for col in row:
                self.id = self.id*100 + col
    
    def f(self):
        return self.g + self.h


    def getFullPath( self ):
        path = []
        node = self
        while node.parent_node:
            path.insert(0, node.move)
            node = node.parent_node
        return path

    def getNextNodes( self ):
        node = self
        next_nodes = []
        for direction_str in DIRECTIONS :
            direction = DIRECTIONS[direction_str]
            # get empty square coordinates
            emptySquare = findEmptySquare( node.state )
            # get empty square new coordinates
            newEmptySqaure = [ emptySquare[0]+direction[0],
                            emptySquare[1]+direction[1] ]
            # check is legal move
            if 0 <= newEmptySqaure[0] < len(node.state) and 0 <= newEmptySqaure[1] < len(node.state[0]) :
                new_state = deepcopy(node.state)
                # swap empty square oldPos with newPos
                new_state[ newEmptySqaure[0] ][ newEmptySqaure[1] ], new_state[ emptySquare[0] ][emptySquare[1]]\
                    = new_state[ emptySquare[0] ][emptySquare[1]], new_state[ newEmptySqaure[0] ][ newEmptySqaure[1] ]
                # create node from state and add it to the list
                new_node = Node( new_state, node, node.g+1, h( new_state ), direction_str )
                next_nodes.append( new_node )
        return next_nodes


def findElement(element, state):
    for i in range( len(state) ):
        for j in range( len( state[0] ) ):
            if state[i][j] == element:
                return (i, j)

def findEmptySquare(state):
    return findElement(0, state)

# misplaced squares
def h( state, goal_state = GOAL_STATE ):
    score = 0
    for row_index in range( len(state) ):
            for col_index in range( len( state[0] )):
                if state[row_index][col_index] != goal_state[row_index][col_index]:
                    score += 1
    return score

# distance to correct position
def h( state, goal_state = GOAL_STATE ):
    score = 0
    for row_index in range( len(state) ):
            for col_index in range( len( state[0] )):
                x, y = findElement(state[row_index][col_index], goal_state)
                score += abs( row_index-x ) + abs( col_index-y )
    return score

def getLowestCostNode( nodeSet ):
    nodeList = list( nodeSet.values() )
    if nodeList == [] : return

    lowest_cost_node = nodeList[0]
    lowest_cost = lowest_cost_node.f()
    for node in nodeList:
        cost = node.f()
        if cost < lowest_cost:
            lowest_cost = cost
            lowest_cost_node = node

    return lowest_cost_node


def solvePuzzle( puzzle : Puzzle ):
    root_node = Node( puzzle.state, None , 0, h(puzzle.state) , "" )
    openSet = { root_node.id : root_node } 
    closedSet = { }

    while openSet:
        node = getLowestCostNode( openSet )

        if node.state == puzzle.goal_state:
            return  node.getFullPath()

        # add node to visited nodes
        closedSet[ node.id ] = node

        next_nodes = node.getNextNodes()
        for n in next_nodes:
            # check if node in open set
            if n.id in openSet and openSet[n.id].f() < n.f() :
                continue
            
            # check if node in closed set
            if n.id in closedSet :
                if closedSet[n.id].f() < n.f():
                    continue
                # remove node from closed set
                del closedSet[n.id]

            openSet[n.id] = n

        # remove node from open nodes
        del openSet[ node.id ]

def solvePuzzle_BreadthFirstSearch( puzzle : Puzzle ):
    root_node = Node( puzzle.state, None , 0, h(puzzle.state) , "" )
    openSet = { root_node.id : root_node } 
    childSet = { }
    closedSet = { }

    while openSet != {}:
        for nodeId in openSet:
            node = openSet[nodeId]

            if node.state == puzzle.goal_state:
                return  node.getFullPath()

            # add node to visited nodes
            closedSet[ node.id ] = node

            next_nodes = node.getNextNodes()
            for n in next_nodes:
                
                # check if node in closed set to avoid cycles
                # if n.id in closedSet :
                #     continue
                childSet[n.id] = n

        openSet = childSet
        childSet = {}


def main():
    puzzle = Puzzle(INITIAL_STATE, GOAL_STATE)
    path = solvePuzzle(puzzle)
    print( path )
    print( len(path),"moves" )

    puzzle.show()
    
    for dir_str in path:
        print()
        puzzle.move( dir_str )
        puzzle.show()

def main_compare():
    puzzle = Puzzle(INITIAL_STATE, GOAL_STATE)
    
    start = time.time()
    path = solvePuzzle(puzzle)
    
    end = time.time()
    print("A star : " ,(end - start)*1000, "ms")
    print( len(path) )
    print( path )

    start = time.time()
    path = solvePuzzle_BreadthFirstSearch(puzzle)
    print( len(path) )
    print( path )
    
    end = time.time()
    print("BFS : " ,(end - start)*1000, "ms")


if __name__ == "__main__":
    main_compare()