import pygame
import sys
from game import *
import puzzle_solver

pygame.init()

# set screen
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Taquin")

# colors
white = (255,255,255)
gray = ( 100,100,100 )
black = (0,0,0)

# FPS
FPS = 30
clock = pygame.time.Clock()


def write_text(text, position, color, fontSize=None):
    if fontSize:
        font = pygame.font.Font('fonts/tahomabd.ttf', fontSize)
    else:
        font = pygame.font.Font('fonts/tahomabd.ttf', 18)
    text = font.render(text, True, color) 
    textRect = text.get_rect()
    textRect.center = position
    screen.blit(text, textRect)



class Square:
    def __init__(self, num, pos, width, height, screen = screen):
        self.num = num
        self.pos = pos
        self.width = width
        self.height = height
    def show(self):
        if self.num == 0:
            return
        pygame.draw.rect(screen, gray, pygame.Rect( self.pos , [ self.width, self.height ] ) )
        pygame.draw.rect(screen, white, pygame.Rect( self.pos , [ self.width, self.height ] ), 1 )
        write_text(str(self.num), [self.pos[0]+self.width//2, self.pos[1]+self.height//2  ], white)

class Puzzle_GUI:
    padding = 20
    square_width = (WIDTH - padding * 2)//3
    square_height = (HEIGHT - padding * 2)//3
    def __init__(self, puzzle : Puzzle, screen = screen):
        self.puzzle = puzzle
        self.squares = []

        for row_index in range(len( self.puzzle.state )) :
            for col_index in range( len( self.puzzle.state[0] ) ):
                square_pos = [ col_index*self.square_width + self.padding , row_index*self.square_height + self.padding ]
                square_n = self.puzzle.state[row_index][col_index]
                square = Square(square_n, square_pos , self.square_width, self.square_height)
                self.squares.append( square )

    # grid pos are inversed (y, x)
    def screenCoord_toGridCoord( self, pos ):
        pos_x, pos_y = (pos[0]-self.padding)//self.square_width , (pos[1]-self.padding)//self.square_height
        return ( pos_y, pos_x )

    # position clicked in grid  to direction (L R U D)
    def posToDirection( self, pos ):
        if min(pos) < 0 or max(pos) >= len( self.puzzle.state ):
            return ""
        for direction_str in DIRECTIONS:
            new_pos =  ( pos[0] - DIRECTIONS[ direction_str ][0],
                            pos[1] - DIRECTIONS[direction_str][1] )
            if min( new_pos ) < 0 or max( new_pos ) >= len( self.puzzle.state ):
                continue
            if self.puzzle.state[new_pos[0]][new_pos[1]] != 0:
                continue
            return direction_str
        return ""

    def directionToPos( self, direction_str ):
        for row_index in range( len(self.puzzle.state) ):
            for col_index in range( len( self.puzzle.state[0] ) ):
                if self.puzzle.state[row_index][col_index] != 0:
                    continue
                new_empty_pos =  ( row_index + DIRECTIONS[ direction_str ][0],
                    col_index + DIRECTIONS[direction_str][1] )
                if min( new_empty_pos ) < 0 or max( new_empty_pos ) >= len( self.puzzle.state ):
                    return (-1, -1)
                return new_empty_pos

    def move(self, direction_str, grid_pos=None):

        if direction_str not in DIRECTIONS:
            return

        if grid_pos == None :
            grid_pos = self.directionToPos(direction_str)

        for square in self.squares:
            
            if square.num == self.puzzle.state[grid_pos[0]][grid_pos[1]]:
                # !!! don't forgot : grip coord and pos coord are reversed
                square.pos[0] -= DIRECTIONS[ direction_str ][1] *  self.square_width
                square.pos[1] -= DIRECTIONS[ direction_str ][0] *  self.square_width
            if square.num == 0:
                square.pos[0] += DIRECTIONS[ direction_str ][1] *  self.square_width
                square.pos[1] += DIRECTIONS[ direction_str ][0] *  self.square_width

        self.puzzle.move( direction_str )

    def handle_mouse_click(self):
        if pygame.mouse.get_pressed()[0] :
            mouse_pos = pygame.mouse.get_pos()
            grid_pos = self.screenCoord_toGridCoord(mouse_pos)
            direction = self.posToDirection( grid_pos )
            self.move(direction, grid_pos)


    def showPuzzle(self):
        for square in self.squares:
            square.show()



def main_game():
    puzzle_gui = Puzzle_GUI(  Puzzle(INITIAL_STATE, GOAL_STATE)  )

    while not puzzle_gui.puzzle.isGoalState():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                puzzle_gui.handle_mouse_click()

        screen.fill(white)

        puzzle_gui.showPuzzle()

        pygame.display.update()
        clock.tick(FPS)

def main_puzzle_solver():
    puzzle_gui = Puzzle_GUI(  Puzzle(INITIAL_STATE, GOAL_STATE)  )
    path = puzzle_solver.solvePuzzle(puzzle_gui.puzzle)
    
    while not puzzle_gui.puzzle.isGoalState():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                puzzle_gui.move( path[0] )
                del path[0]

        screen.fill(white)

        puzzle_gui.showPuzzle()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main_puzzle_solver()