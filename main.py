from gui import *

def main_game_with_solver():
    puzzle_gui = Puzzle_GUI(  Puzzle(INITIAL_STATE, GOAL_STATE)  )
    path = puzzle_solver.solvePuzzle(puzzle_gui.puzzle)
    text_pos = ( WIDTH//2, PADDING_TOP//2)
    goal = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                played_move = puzzle_gui.handle_mouse_click()
                if path and played_move == path[0]:
                    del path[0]
                else:
                    path = puzzle_solver.solvePuzzle(puzzle_gui.puzzle)

                    
        screen.fill(white)
        if path:
            write_text(path[0]+f" - Solution in {len(path)} moves", text_pos, black)
        else:
            write_text("Puzzle solved", text_pos, black)

        puzzle_gui.showPuzzle()

        pygame.display.update()
        clock.tick(FPS)

def main_puzzle_solver():
    puzzle_gui = Puzzle_GUI(  Puzzle(INITIAL_STATE, GOAL_STATE)  )
    path = puzzle_solver.solvePuzzle(puzzle_gui.puzzle)
    moves_num = 0
    text_pos = ( WIDTH//2, PADDING_TOP//2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if path != []:
                    puzzle_gui.move( path[0] )
                    moves_num +=1
                    del path[0]

        screen.fill(white)
        write_text(str(moves_num), text_pos, black)

        puzzle_gui.showPuzzle()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main_puzzle_solver()