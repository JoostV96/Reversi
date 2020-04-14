import numpy as np
import pygame

WIDTH = 450
HEIGHT = 450
TOTAL_HEIGHT = 550  # including the score

DIM_WIDTH = 8
DIM_HEIGHT = 8

CELL_WIDTH = WIDTH//DIM_WIDTH
RADIUS = CELL_WIDTH - 10

PLAYER_1 = 1
PLAYER_2 = 2

BLACK = (0,0,0)
WHITE = (52, 130, 56)
BLUE = (0,0,255)
RED = (255,0,0)
GREY = (211,211,211)
GREEN = (0, 255, 0)


class Reverse:
    
    def __init__(self):
        self.board = np.zeros((DIM_HEIGHT, DIM_WIDTH))
        width_mid = DIM_WIDTH//2-1
        height_mid = DIM_HEIGHT//2-1
        self.board[height_mid, width_mid] = PLAYER_2
        self.board[height_mid+1, width_mid+1] = PLAYER_2
        self.board[height_mid+1, width_mid] = PLAYER_1
        self.board[height_mid, width_mid+1] = PLAYER_1
        self.turn = PLAYER_1
        self.last_played = (-1, -1)
        
    def insert_move(self, row, col, player):
        self.board[row, col] = player
        self.last_played = (row, col)
        self.reverse_board(row, col, player)
        self.turn = self.turn%2+1        
 
    def check_valid_move(self, row, col, player):
        big_board = np.zeros((DIM_WIDTH+4, DIM_HEIGHT+4))
        big_board[2:DIM_WIDTH+2, 2:DIM_HEIGHT+2] = self.board   
        row += 2
        col += 2        
        
        opponent = player%2+1
        
        if big_board[row, col] != 0:
            return False
        # North
        if big_board[row-1, col] == opponent:
            r = row - 2
            while r >= 0 and big_board[r, col] == opponent:
                r -= 1
            if big_board[r, col] == player:
                return True
        # North-East
        if big_board[row-1, col+1] == opponent:
            r = row - 2
            c = col + 2
            while r >= 0 and c <= DIM_WIDTH and big_board[r, c] == opponent:
                r -= 1
                c += 1
            if big_board[r, c] == player:
                return True
        # East
        if big_board[row, col+1] == opponent:
            c = col + 2
            while c <= DIM_WIDTH and big_board[row, c] == opponent:
                c += 1
            if big_board[row, c] == player:
                return True
        # South-East
        if big_board[row+1, col+1] == opponent:
            r = row + 2
            c = col + 2
            while r <= DIM_HEIGHT and c <= DIM_WIDTH and big_board[r, c] == opponent:
                r += 1
                c += 1
            if big_board[r, c] == player:
                return True
        # South 
        if big_board[row+1, col] == opponent:
            r = row + 2
            while r <= DIM_WIDTH and big_board[r, col] == opponent:
                r += 1
            if big_board[r, col] == player:
                return True
        # South-West
        if big_board[row+1, col-1] == opponent:
            r = row + 2
            c = col - 2
            while r <= DIM_HEIGHT and c >= 0 and big_board[r, c] == opponent:
                r += 1
                c -= 1
            if big_board[r, c] == player:
                return True
        # West 
        if big_board[row, col-1] == opponent:
            c = col - 2
            while c >= 0 and big_board[row, c] == opponent:
                c -= 1
            if big_board[row, c] == player:
                return True
        # North-West
        if big_board[row-1, col-1] == opponent:
            r = row - 2
            c = col - 2
            while r >= 0 and c >= 0 and big_board[r, c] == opponent:
                r -= 1
                c -= 1
            if big_board[r, c] == player:
                return True
        return False

    def avail_moves(self):
        moves = []
        for r in range(DIM_HEIGHT):
            for c in range(DIM_WIDTH):
                if self.check_valid_move(r, c, self.turn):
                    moves.append((r,c))
        return moves
            
    def reverse_board(self, row, col, player):
        big_board = np.zeros((DIM_WIDTH+4, DIM_HEIGHT+4))
        big_board[2:DIM_WIDTH+2, 2:DIM_HEIGHT+2] = self.board   
        row += 2
        col += 2        
        
        opponent = player%2+1
        # North
        if big_board[row-1, col] == opponent:
            r = row - 2
            while r >= 0 and big_board[r, col] == opponent:
                r -= 1
            if big_board[r, col] == player:
                for i in range(row-r):
                    big_board[row-i, col] = player
        # North-East
        if big_board[row-1, col+1] == opponent:
            r = row - 2
            c = col + 2
            while r >= 0 and c <= DIM_WIDTH and big_board[r, c] == opponent:
                r -= 1
                c += 1
            if big_board[r, c] == player:
                for i in range(c-col):
                    big_board[row-i, col+i] = player
        # East
        if big_board[row, col+1] == opponent:
            c = col + 2
            while c <= DIM_WIDTH and big_board[row, c] == opponent:
                c += 1
            if big_board[row, c] == player:
                for i in range(c-col):
                    big_board[row, col+i] = player
        # South-East
        if big_board[row+1, col+1] == opponent:
            r = row + 2
            c = col + 2
            while r <= DIM_HEIGHT and c <= DIM_WIDTH and big_board[r, c] == opponent:
                r += 1
                c += 1
            if big_board[r, c] == player:
                for i in range(c-col):
                    big_board[row+i, col+i] = player
        # South 
        if big_board[row+1, col] == opponent:
            r = row + 2
            while r <= DIM_WIDTH and big_board[r, col] == opponent:
                r += 1
            if big_board[r, col] == player:
                for i in range(r-row):
                    big_board[row+i, col] = player
        # South-West
        if big_board[row+1, col-1] == opponent:
            r = row + 2
            c = col - 2
            while r <= DIM_HEIGHT and c >= 0 and big_board[r, c] == opponent:
                r += 1
                c -= 1
            if big_board[r, c] == player:
                for i in range(r-row):
                    big_board[row+i, col-i] = player
        # West 
        if big_board[row, col-1] == opponent:
            c = col - 2
            while c >= 0 and big_board[row, c] == opponent:
                c -= 1
            if big_board[row, c] == player:
                for i in range(col-c):
                    big_board[row, col-i] = player
        # North-West
        if big_board[row-1, col-1] == opponent:
            r = row - 2
            c = col - 2
            while r >= 0 and c >= 0 and big_board[r, c] == opponent:
                r -= 1
                c -= 1
            if big_board[r, c] == player:
                for i in range(col-c):
                    big_board[row-i, col-i] = player
        
        self.board = big_board[2:DIM_WIDTH+2, 2:DIM_HEIGHT+2]
    
    def score(self):
        return np.count_nonzero(self.board == PLAYER_1), np.count_nonzero(self.board == PLAYER_2)
    
    
class Drawer:
    
    def __init__(self, screen):
        """Inits the drawer class."""
        self.screen = screen
        
    def draw_board(self, reversi):
        self.draw_lines()
        self.draw_pieces(reversi)
        self.draw_score(reversi)
        pygame.display.update()

    def draw_lines(self):
        """Draws the lines to make the playing field."""
        # vertical lines
        start = (0,0)
        end = (0, HEIGHT)
        for i in range(DIM_WIDTH):
            pygame.draw.line(self.screen, BLACK, start, end, 1)
            start = self.adjust_tuple(start, 0, HEIGHT/DIM_WIDTH)
            end = self.adjust_tuple(end, 0, HEIGHT/DIM_WIDTH)
            
        # horizontal lines
        start = (0,0)
        end = (WIDTH, 0)
        for i in range(DIM_HEIGHT+1):
            pygame.draw.line(self.screen, BLACK, start, end, 1)
            start = self.adjust_tuple(start, 1, WIDTH/DIM_HEIGHT)
            end = self.adjust_tuple(end, 1, WIDTH/DIM_HEIGHT)
     
    def draw_pieces(self, reversi):
        for r in range(len(reversi.board)):
            for c in range(len(reversi.board[r, :])):
                if reversi.board[r, c] == 1:
                    pos_circle = (int((c+0.5)*CELL_WIDTH), int((r+0.5)*CELL_WIDTH))
                    pygame.draw.circle(self.screen, RED, pos_circle, RADIUS//2)
                elif reversi.board[r, c] == 2:                   
                    pos_circle = (int((c+0.5)*CELL_WIDTH), int((r+0.5)*CELL_WIDTH))
                    pygame.draw.circle(self.screen, BLUE, pos_circle, RADIUS//2)
        
        # last played move
        move = reversi.last_played
        r = move[0]
        c = move[1]
        pos_circle = (int((c+0.5)*CELL_WIDTH), int((r+0.5)*CELL_WIDTH))
        pygame.draw.circle(self.screen, BLACK, pos_circle, 5)
        
        avail_moves = reversi.avail_moves()
        for move in avail_moves:
            r = move[0]
            c = move[1]
            pos_circle = (int((c+0.5)*CELL_WIDTH), int((r+0.5)*CELL_WIDTH))
            pygame.draw.circle(self.screen, BLACK, pos_circle, RADIUS//2, 1)
                    
    def draw_score(self, reversi):
        myfont = pygame.font.SysFont(None, 54)
        score = reversi.score()
        textsurface = myfont.render("Player 1: {}, Player 2: {}".format(score[0], score[1]), False, BLACK)
        pos = (0, TOTAL_HEIGHT - (TOTAL_HEIGHT - HEIGHT))  
        self.screen.blit(textsurface, pos)
        
        myfont = pygame.font.SysFont(None, 54)
        if reversi.turn == PLAYER_1:
            color = RED
        else:
            color = BLUE
        textsurface = myfont.render("Turn: Player {}".format(reversi.turn), False, color)
        pos = (0, TOTAL_HEIGHT - ((TOTAL_HEIGHT - HEIGHT)//2))  
        self.screen.blit(textsurface, pos)
    
    @staticmethod    
    def mouse_to_cell(pos_x, pos_y):
        """Static method to convert the mouse position to a position on the board."""
        x = pos_x // CELL_WIDTH
        y = pos_y // CELL_WIDTH
        return int(x), int(y)
               
    @staticmethod
    def adjust_tuple(x, index, increment):
        """Static method to increment a tuple."""
        x = list(x)
        x[index] += increment
        return tuple(x)



def main():
    """Main loop of the program."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,TOTAL_HEIGHT))
    pygame.display.set_caption('Reversi')
    clock = pygame.time.Clock()
    screen.fill(WHITE)
        
    reversi = Reverse()
    drawer = Drawer(screen)

    done = False
    pos_x = pos_y = 0
    x = y = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill(WHITE)
                (pos_x, pos_y) = pygame.mouse.get_pos()   
                x, y = drawer.mouse_to_cell(pos_x, pos_y)
                if reversi.turn == PLAYER_1:  
                    if reversi.check_valid_move(y, x, PLAYER_1):
                        reversi.insert_move(y, x, PLAYER_1)
                    else: 
                        print("Wrong move")
                else:
                    if reversi.check_valid_move(y, x, PLAYER_2):
                        reversi.insert_move(y, x, PLAYER_2)
                    else: 
                        print("Wrong move")
      
        drawer.draw_board(reversi)
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    
if __name__ == '__main__':
    main()
