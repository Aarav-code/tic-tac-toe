import pygame
import sys
import time
from copy import deepcopy

white = (255,255,255)
black = (0,0,0)

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.display = pygame.display.set_mode((500,500))
        self.font = pygame.font.Font('freesansbold.ttf', 150)
        pygame.display.set_caption('Tic Tac Toe')
        self.display.fill(black)
        pygame.display.update()
        self.lines = [(167,0,10,500), (334,0,10,500), (0,167,500,10), (0,334,500,10)]
        self.boxes = [(0, 0, 150, 150), (177, 0, 150, 150),(345, 0, 150, 150),
                    (0, 177, 150, 150), (177, 177, 150, 150),(345, 177, 150, 150),
                    (0, 345, 150, 150), (177, 345, 150, 150),(345, 345, 150, 150)]

    def main(self):
        x_turn = True
        o_turn = False
        turns = 0 
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if x_turn:
                        for coord in self.boxes:
                            if coord != "X" and coord != "O": button = pygame.draw.rect(self.display,black,coord)
                            if button.collidepoint(mouse_pos):
                                print("button clicked at {0}".format(mouse_pos))
                                print(button)
                                self.x_chance(button)
                                pygame.display.update()
                                self.update_board(button, "x_turn")
                                x_turn = False
                                o_turn = True
                                turns+=1
                                break
                    else:   
                        self.o_chance(best_box)
                        pygame.display.update()
                        self.update_board(best_box, "o_turn")     
                        x_turn = True
                        o_turn = False
                        turns += 1
                        break
                    current_board = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
    ]
                    best_value = (self.minimax(current_board, True, 0)[1])
                    print(best_value)
                    for n , i in enumerate(self.boxes):
                        if n + 1 == best_value:
                            best_box = i
                            break
                    print(best_box)
            if self.has_won("X"):
                time.sleep(3)
                break
            if self.has_won("O"):
                time.sleep(3)
                break
            if self.draw(turns):
                pygame.display.update()
                time.sleep(3)
                break
            self.make_board()
        pygame.quit()
        quit()
    
    def update_board(self, button, turn):
        a, b, c, d = button
        for n, i in enumerate(self.boxes):
            if i == (a, b, c, d):
                if turn == "x_turn":
                    self.boxes[n] = "X"
                    break
                elif turn == "o_turn":
                    self.boxes[n] = "O"
                    break

    def make_board(self):
        for line in self.lines:
            pygame.draw.rect(self.display,white,line)
        for box in self.boxes:
            if box == "O" or box == "X": continue
            pygame.draw.rect(self.display,black,box)
        pygame.display.update()

    def x_chance(self, box):
        text = self.font.render("X", True, white, black)
        a, b, c, d = box
        textrect = text.get_rect()
        textrect.center = (a + 70, b + 80)
        self.display.blit(text, textrect)
    
    def o_chance(self, box):
        text = self.font.render("O", True, white, black)
        a, b, c, d = box
        textrect = text.get_rect()
        textrect.center = (a + 70, b + 80)
        self.display.blit(text, textrect)
    
    def has_won(self, player):
        for i in range(0, 8, 3):
            if self.boxes[i] == self.boxes[i + 1] == self.boxes[i + 2]:
                self.winner(player)
                pygame.display.update()
                return True

        for i in range(3):
            if self.boxes[i] == self.boxes[i + 3] and self.boxes[i + 3] == self.boxes[i + 6]:
                if self.boxes[i] == "X":
                    self.winner("X")
                    pygame.display.update()
                else:
                    self.winner("O")
                    pygame.display.update()
                return True
                
        if self.boxes[0] == self.boxes[4] and self.boxes[4] == self.boxes[8] or self.boxes[2] == self.boxes[4] and self.boxes[4] == self.boxes[6]:
            if self.boxes[4] == "X":
                self.winner("X")
                pygame.display.update()
            else:
                self.winner("O")
                pygame.display.update()
            return True


    def has_won1(self, board, player):
        for row in board:
            if row.count(player) == 3:
                return True
        for i in range(3):
            if board[0][i] == player and board[1][i] == player and board[2][i] == player:
                return True
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True
        return False

    def winner(self, letter):
        font = pygame.font.Font('freesansbold.ttf', 56)
        text = font.render("{0} won".format(letter), True, black, white)
        textrect = text.get_rect()
        textrect.center = (250, 250)
        self.display.blit(text, textrect)

    def select_space(self,board, move, turn):
        if move not in range(1,10):
            return False
        row = int((move-1)/3)
        col = (move-1)%3
        if board[row][col] != "X" and board[row][col] != "O":
            board[row][col] = turn
            return True
        else:
            return False

    def available_moves(self, board):
        moves = []
        for row in board:
            for col in row:
                if col != "X" and col != "O":
                    moves.append(int(col))
        return moves
    
    def game_is_over(self, board):
        return self.has_won("X") or self.has_won("O") or len(self.available_moves(board)) == 0
    
    def evaluate_board(self, board):
        if self.has_won1(board, "O"):
            return 1
        elif self.has_won1(board,"X"):
            return -1
        else:
            return 0
    
    def minimax(self,current_board, is_maximizing, i):
        if i == 0:
            x_moves = []
            o_moves = []
            z = 0
            for n,i in enumerate(self.boxes):
                z += 1
                if i == "X":
                    x_moves.append(str(z))
                elif i == "O":
                    o_moves.append(str(z))

            for move in x_moves:
                for n, row in enumerate(current_board):
                    for y, col in enumerate(row):
                        if col == move:
                            current_board[n][y] = "X"
            
            for move in o_moves:
                for n, row in enumerate(current_board):
                    for y, col in enumerate(row):
                        if col == move:
                            current_board[n][y] = "O"
        

        if self.game_is_over(current_board):
            return [self.evaluate_board(current_board), ""]
        # The maximizing player
        if is_maximizing:
            best_value = -float("Inf")
            best_move = ""
            for move in self.available_moves(current_board):
                new_board = deepcopy(current_board)
                self.select_space(new_board, move, "O")
                hypothetical_value = self.minimax(new_board, False, 1)[0]
                if hypothetical_value > best_value:
                    best_value = hypothetical_value
                    best_move = move
            return [best_value, best_move]
        # The minimizing player
        else:
            best_value = float("Inf")
            best_move = ""
            for move in self.available_moves(current_board):
                new_board = deepcopy(current_board)
                self.select_space( new_board, move, "X")
                hypothetical_value = self.minimax(new_board, True, 1)[0]
                if hypothetical_value < best_value:
                    best_value = hypothetical_value
                    best_move = move
            return [best_value, best_move]

    def draw(self, num):
        if num == 9:
            font = pygame.font.Font('freesansbold.ttf', 130)
            text = font.render("DRAW".format(num), True, black, white)
            textrect = text.get_rect()
            textrect.center = (250, 250)
            self.display.blit(text, textrect)
            return True
        else:
            return False

    
a = Game()
a.main()