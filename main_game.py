import pygame, asyncio
# from pygame.locals import *
import sys, os, math
from miniMax_agent import *
from logic import *
from alpha_beta_agent import *
import time

#### GLOBAL GAMEBOARD MATRIX VARIABLE TO DRAW THE INITIAL BOARD ####
GAMEBOARD = [[1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2]]

class BreakthroughGame:
    def __init__(self):
        pygame.init()
        self.sizeofcell = 75
        self.height = len(GAMEBOARD)*self.sizeofcell
        self.width = (len(GAMEBOARD[0])*self.sizeofcell) + (self.sizeofcell*4)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([0, 0, 0])

        # ATTRIBUTES FOR PLAYER GAME PIECES

        self.light_square = 0
        self.dark_square = 0
        self.greenAlien = 0
        self.blueAlien = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0
        self.sim_one_move = None

        # turn 1: black 2: white
        """
        The player_state variable determines the state of the current piece
        state = 0: starting position for the piece
        state = 1: it is the current player's turn and there are available moves
        state = 2: end of current player's turn
        state = 3: player has won the game
        """
        self.player_state = 0
        self.turn = 1

        # VARIABLES FOR TRACKING PIECE POSITION
        self.init_x = 0
        self.init_y = 0
        self.x_move = 0
        self.y_move = 0 

        # matrix for position of chess, 0 - empty, 1 - black, 2 - white
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        self.total_nodes_1 = 0
        self.total_nodes_2 = 0
        self.total_time_1 = 0
        self.total_time_2 = 0
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece = 0
        # Caption
        pygame.display.set_caption("Breakthrough Galactic!")

        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initgraphics()

    def run(self):
        self.clock.tick(60)

        # clear the screen
        self.screen.fill([0, 0, 0])
        self.screen.blit(self.moon, (0, 0))


        if self.player_state == 5:
            # Black
            if self.turn == 1:
                start = time.process_time()
                self.ai_move(2, 2)
                self.total_time_1 += (time.process_time() - start)
                self.total_step_1 += 1
                print('total_step_1 = ', self.total_step_1,
                      'total_nodes_1 = ', self.total_nodes_1,
                      'node_per_move_1 = ', self.total_nodes_1 / self.total_step_1,
                      'time_per_move_1 = ', self.total_time_1 / self.total_step_1,
                      'have_eaten = ', self.eat_piece)
            elif self.turn == 2:
                start = time.process_time()
                self.ai_move(2, 2)
                self.total_time_2 += (time.process_time() - start)
                self.total_step_2 += 1
                print('total_step_2 = ', self.total_step_2,
                      'total_nodes_2 = ', self.total_nodes_2,
                      'node_per_move_2 = ', self.total_nodes_2 / self.total_step_2,
                      'time_per_move_2 = ', self.total_time_2 / self.total_step_2,
                      'have_eaten: ', self.eat_piece)

        # EVENT LISTENERS
                """
                Due to the way the event listeners are set up for this game, the game 
                needs to check and see if any of the buttons were pressed before checking 
                to see if a piece was selected.
                Because a player can only select a piece if it is their turn, we have to 
                monitor the state of the piece. And because there are only three playable 
                states, if the game reads a state and then sees the MOUSEBUTTONDOWN event
                in a location other than a piece, it will cause an error.
                """
        for event in pygame.event.get():
            # Quit if close the windows
            if event.type == pygame.QUIT:
                exit()

            # CHECK TO SEE IF THE RESET BUTTON WAS PRESSED
            elif event.type == pygame.MOUSEBUTTONDOWN and self.reset_pressed(event.pos):
                self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1, 1, 1, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 0],
                                    [2, 2, 2, 2, 2, 2, 2, 2],
                                    [2, 2, 2, 2, 2, 2, 2, 2]]
                self.turn = 1
                self.player_state = 0
            # CHECK TO SEE IF MOVE ONCE BUTTON WAS PRESSED
            elif event.type == pygame.MOUSEBUTTONDOWN and self.move_once_pressed(event.pos):
                self.alpha_beta_eval(1)
                # self.minmax_eval()

            elif event.type == pygame.MOUSEBUTTONDOWN and self.simulate_pressed(event.pos):
                self.player_state = 5

            # SELECT PIECE
            elif event.type == pygame.MOUSEBUTTONDOWN and self.player_state == 0:
                x, y = event.pos
                coor_y = math.floor(x / self.sizeofcell)
                coor_x = math.floor(y / self.sizeofcell)
                if self.boardmatrix[coor_x][coor_y] == self.turn:
                    self.player_state = 1
                    self.init_y = math.floor(x / self.sizeofcell)
                    self.init_x = math.floor(y / self.sizeofcell)

            # check whether the selected chess can move, otherwise select other chess
            elif event.type == pygame.MOUSEBUTTONDOWN and self.player_state == 1:
                x, y = event.pos
                self.y_move = math.floor(x / self.sizeofcell)
                self.x_move = math.floor(y / self.sizeofcell)
                if self.available_moves():
                    self.move_piece()
                    if (self.x_move == 7 and self.boardmatrix[self.x_move][self.y_move] == 1) \
                        or (self.x_move == 0 and self.boardmatrix[self.x_move][self.y_move] == 2):
                        self.player_state = 3
                elif self.boardmatrix[self.x_move][self.y_move] == self.boardmatrix[self.init_x][self.init_y]:
                    self.init_x = self.x_move
                    self.init_y = self.y_move
            
                    # display the board and chess
        self.display()
        # update the screen
        pygame.display.flip()

        #print(self.reset)

    # load the graphics and rescale them
    def initgraphics(self):
        self.moon = pygame.image.load_extended(os.path.join('assets', 'Moon.jpg'))
        self.moon = pygame.transform.scale(self.moon, (self.width, self.height))

        self.dark_square = pygame.image.load_extended(os.path.join('assets', 'SpaceDark.png'))
        self.dark_square = pygame.transform.scale(self.dark_square, (self.sizeofcell, self.sizeofcell))
        self.light_square = pygame.image.load_extended(os.path.join('assets', 'SpaceLight.png'))
        self.light_square = pygame.transform.scale(self.light_square, (self.sizeofcell, self.sizeofcell))

        self.greenAlien = pygame.image.load_extended(os.path.join('assets', 'alien2.png'))
        self.greenAlien = pygame.transform.scale(self.greenAlien, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.blueAlien = pygame.image.load_extended(os.path.join('assets', 'alien1.png'))
        self.blueAlien = pygame.transform.scale(self.blueAlien, (self.sizeofcell - 20, self.sizeofcell - 20))

        self.outline = pygame.image.load_extended(os.path.join('assets', 'square-outline.png'))
        self.outline = pygame.transform.scale(self.outline, (self.sizeofcell, self.sizeofcell))

        self.reset = pygame.image.load_extended(os.path.join('assets', 'resetbutton.png'))
        self.reset = pygame.transform.scale(self.reset, (200, 150))

        self.sim_one_move = pygame.image.load_extended(os.path.join('assets', 'robot.png'))
        self.sim_one_move = pygame.transform.scale(self.sim_one_move, (150, 150))

        self.auto = pygame.image.load_extended(os.path.join('assets', 'playbutton.png'))
        self.auto = pygame.transform.scale(self.auto, (130, 130))

        self.winner = pygame.image.load_extended(os.path.join('assets', 'trophy.png'))
        self.winner = pygame.transform.scale(self.winner, (250, 250))

    # display the graphics in the window
    def display(self):

        ##### INITIALIZE FONTS #####
        PIXEL_FONT = pygame.font.Font(os.path.join('assets', 'pixelfont.ttf'), 20)

        ##### CREATE FONT OBJECTS TO DESCRIBE EACH BUTTON AND RECTS FOR EACH OBJECT #####
        rst_label = PIXEL_FONT.render(f"Reset Board", 1, (255, 255, 255))
        rst_label_rect = rst_label.get_rect()
        rst_label_rect.center = ((self.screen.get_width()) - (rst_label.get_width())*.85, (self.height*.33)-45)
        ai_move = PIXEL_FONT.render(f"Simulate 1 Move", 1, (255, 255, 255))
        ai_move_rect = ai_move.get_rect()
        ai_move_rect.center = ((self.screen.get_width()) - (rst_label.get_width())*.85, (self.screen.get_height()*.66)-35)
        auto_play = PIXEL_FONT.render(f"Simulate Game", 1, (255, 255, 255))
        auto_play_rect = auto_play.get_rect()
        auto_play_rect.center = ((self.screen.get_width()) - (rst_label.get_width())*.85, (self.screen.get_height()*.99)-35)

        #### DISPLAY THE RECTS ####
        self.screen.blit(rst_label, rst_label_rect)
        self.screen.blit(ai_move, ai_move_rect)
        self.screen.blit(auto_play, auto_play_rect)
        
        self.draw_game_board()

        #### DRAW THE BUTTONS ####
        self.screen.blit(self.reset, (math.floor((self.width) - 200*.85)-90, math.floor((self.height*.18)-93)))
        self.screen.blit(self.sim_one_move, (math.floor((self.width) - 200*.85)-60, math.floor((self.height*.48)-85)))
        self.screen.blit(self.auto, (math.floor((self.width) - 200*.85)-50, math.floor((self.height*.75)-40)))

        for i in range(8):
            for j in range(8):
                if self.boardmatrix[i][j] == 1:
                    self.screen.blit(self.greenAlien, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
                elif self.boardmatrix[i][j] == 2:
                    self.screen.blit(self.blueAlien, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
        if self.player_state == 1:
            # only downward is acceptable
            if self.boardmatrix[self.init_x][self.init_y] == 1:
                x1 = self.init_x + 1
                y1 = self.init_y - 1
                x2 = self.init_x + 1
                y2 = self.init_y + 1
                x3 = self.init_x + 1
                y3 = self.init_y
                # left down
                if y1 >= 0 and self.boardmatrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # right down
                if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # down
                if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

            if self.boardmatrix[self.init_x][self.init_y] == 2:
                x1 = self.init_x - 1
                y1 = self.init_y - 1
                x2 = self.init_x - 1
                y2 = self.init_y + 1
                x3 = self.init_x - 1
                y3 = self.init_y
                # left up
                if y1 >= 0 and self.boardmatrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # right up
                if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # up
                if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))
        if self.player_state == 3:
            self.screen.blit(self.winner, (100, 100))

#####   FUNCTION TO DRAW THE GAMEBOARD ONTO THE SCREEN  #####
    def draw_game_board(self):
        """
        Iterate over the gameboard matrix and draw either light of dark images 
        based on if the position in the matrix is odd or even.
        """
        for y in range(0, len(GAMEBOARD)):
            for x in range(0, len(GAMEBOARD[0])):
                if (x+y) % 2 == 0:
                    self.screen.blit(self.light_square, (x * self.sizeofcell, y * self.sizeofcell))
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * self.sizeofcell, y * self.sizeofcell, self.sizeofcell, self.sizeofcell), 1)
                    
                else:
                    self.screen.blit(self.dark_square, (x * self.sizeofcell, y * self.sizeofcell))
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * self.sizeofcell, y * self.sizeofcell, self.sizeofcell, self.sizeofcell), 1)

##### FUNCTION TO CHECK IF THE SELECTED PIECE HAS ANY AVAILABLE MOVES #####
    def available_moves(self):
        if (self.boardmatrix[self.init_x][self.init_y] == 1
            and self.boardmatrix[self.x_move][self.y_move] != 1
            and self.x_move - self.init_x == 1
            and self.init_y - 1 <= self.y_move <= self.init_y + 1
            and not (self.init_y == self.y_move and self.boardmatrix[self.x_move][self.y_move] == 2)) \
            or (self.boardmatrix[self.init_x][self.init_y] == 2
                and self.boardmatrix[self.x_move][self.y_move] != 2
                and self.init_x - self.x_move == 1
                and self.init_y - 1 <= self.y_move <= self.init_y + 1
                and not (self.init_y == self.y_move and self.boardmatrix[self.x_move][self.y_move] == 1)):
            return 1
        return 0

    def move_piece(self):
        self.boardmatrix[self.x_move][self.y_move] = self.boardmatrix[self.init_x][self.init_y]
        self.boardmatrix[self.init_x][self.init_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.player_state = 0

##### FUNCTION TO CHECK IF THE THE GAME HAS BEEN WON #####
    def check_win(self, base=0):
        if base == 0:
            if 2 in self.boardmatrix[0] or 1 in self.boardmatrix[7]:
                return True
            else:
                for line in self.boardmatrix:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.boardmatrix[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.boardmatrix[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.boardmatrix:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False

##### SETS THE ACCEPTABLE RANGE FOR WHICH THE PLAYER CAN CLICK AND ACTIVATE THE RESET BUTTON #####
    def reset_pressed(self, pos):
        x, y = pos
        if 815 >= x >= 660 and 75 <= y <= 138:
            return True
        return False

##### SETS THE ACCEPTABLE RANGE FOR WHICH THE PLAYER CAN CLICK AND ACTIVATE THE BUTTON TO HAVE THE COMPUTER MAKE ONE MOVE #####
    def move_once_pressed(self, pos):
        x, y = pos
        if 683 <= x <= 799 and 210 <= y <= 336:
            return True
        return False

##### SETS THE ACCEPTABLE RANGE FOR WHICH THE PLAYER CAN CLICK AND ACTIVATE THE BUTTON TO SIMULATE ENTIRE GAME #####
    def simulate_pressed(self, pos):
        x, y = pos
        if 676 <= x <= 810 and 412 <= y <= 535:
            return True
        return False


##### FUNCTION TO CHOOSE IF THE PLAYER WILL USE MINIMAX OR ALPHA BETA #####
    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.minmax_eval(evaluation)
        elif searchtype == 2:
            return self.alpha_beta_eval(evaluation)

##### FUNCTION TO GET INFORMATION FROM THE MINIMAX AGENT #####
    def minmax_eval(self, function_type):
        board, nodes, piece = MinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_move_choice()
        self.boardmatrix = board.get_board()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.check_win():
            self.player_state = 3
            #print(self.boardmatrix)

##### FUNCTION TO GET INFORMATION FROM THE ALPHA BETA AGENT #####
    def alpha_beta_eval(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 4, function_type).alpha_beta_decision()
        self.boardmatrix = board.get_board()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.check_win():
            self.player_state = 3


async def main():
    game = BreakthroughGame()
    while 1:
        game.run()
        await asyncio.sleep(0)

if __name__ == '__main__':
    main()

asyncio.run(main())

