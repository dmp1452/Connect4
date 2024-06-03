import sys
import pygame
import numpy as np
import random #random.uniform
import copy
from values import *

pygame.init()
screen = pygame.display.set_mode((W,H+TILE_SIZE))
pygame.display.set_caption("Connect 4")
screen.fill(BACKGROUND_COLOR)

class Board:
    def __init__(self):
        self.tiles = np.zeros((ROWS,COLS))
        self.bottom =np.zeros(COLS)
        self.marked_tiles =0
        self.last_move=None
        self.position_ranking =[1,3,4,4,4,3,1]

    def get_row(self,col):
        return self.bottom[col]
    
    def place(self,row,col,player):
        self.last_move = (int(row),int(col))
        self.tiles[int(row)][int(col)]= player
        self.bottom[col]+=1
        self.marked_tiles+=1
    
    def is_full(self):
        return self.marked_tiles ==42
    
    def get_choices(self):
        """
        choice =[]
        for i in range(COLS):
            if self.bottom[i]<6:
                choice.append((int(self.bottom[i]),i))
        return choice"""
        center = COLS // 2
        choices = []

    # Check from center to the left
        for offset in range(center + 1):
            col = center - offset
            if self.bottom[col] < 6:
                choices.append((int(self.bottom[col]), col))
            col = center + offset
            if col < COLS and self.bottom[col] < 6:
                choices.append((int(self.bottom[col]), col))

        return choices

        
    def final_state(self):
        if self.is_full() or self.last_move==None:
            return 0
        
        num =self.check_win()
        if num!=0:
            return num

        player = self.tiles[self.last_move[0]][self.last_move[1]]
        total =0
        for i in range(COLS):
            col_weight=0
            p = int(self.bottom[i])-1
            while p>=0:
                if self.tiles[p][i]==player:
                    col_weight+=1
                    down = p>0
                    left = i>0
                    right =i<COLS-1
                    up = p<ROWS-1
                    #if down and self.tiles[p-1][i]==player:
                     #   col_weight+=2

                    if down and left and self.tiles[p-1][i-1]==player:
                        col_weight +=2
                    elif down and left and self.tiles[p-1][i-1]==0:
                        col_weight +=1

                    if down and right and self.tiles[p-1][i+1]==player:
                        col_weight +=2
                    elif down and right and self.tiles[p-1][i+1]==0:
                        col_weight +=1

                    if left and self.tiles[p][i-1]==player:
                        col_weight +=2
                    elif left and self.tiles[p][i-1]==0:
                        col_weight +=1

                    if right and self.tiles[p][i+1]==player:
                        col_weight +=2
                    elif right and self.tiles[p][i+1]==0:
                        col_weight +=2



                p-=1
            total+=col_weight*self.position_ranking[i]
        eval =total*player
        return eval
                


    def check_win(self):
        row,col = int(self.last_move[0]),int(self.last_move[1])
        player = self.tiles[row][col]

        horizontal =1
        left =col-1
        while left>=0 and self.tiles[row][left]==player:
            horizontal +=1
            left-=1
        right = col+1
        while right < COLS and self.tiles[row][right]==player:
            horizontal+=1
            right +=1
        if horizontal >3:
            return player*100000
        
        vertical =1
        down = row+1
        while down<ROWS and self.tiles[down][col]==player:
            vertical +=1
            down +=1
        up = row-1
        while up>=0 and self.tiles[up][col] == player:
            vertical +=1
            up -=1
        if vertical >3:
            return player*100000
        
        desc_diag =1
        x, y = row-1,col-1
        while x>=0 and y >=0 and self.tiles[x][y]==player:
            desc_diag +=1
            x -=1
            y-=1
        x,y = row+1,col+1
        while x<ROWS and y <COLS and self.tiles[x][y]==player:
            desc_diag +=1
            x +=1
            y +=1
        if desc_diag >3:
            return player*100000
        
        asc_diag =1
        x, y = row+1,col-1
        while x<ROWS and y>=0 and self.tiles[x][y]==player:
            asc_diag +=1
            x+=1
            y-=1
        x, y = row-1,col+1
        while x>=0 and y< COLS and self.tiles[x][y]==player:
            asc_diag +=1
            x-=1
            y+=1
        if asc_diag >3:
            return player*100000
        
        return 0
        

        

        



class ai:
    def __init__(self,player =-1):
        self.player = player

    def eval(self,main_board):

        eval, move = self.minimax(main_board,False, -10,10,0)
        print("Chosen " + str(eval))
        return move
    
    def minimax(self,board, maximizing, alpha,beta, level):
        case = board.final_state()
        if abs(case) == 100000:
            return case, None
        elif board.is_full():
            return 0, None
        elif level ==7:
          return case,None
        choices = board.get_choices()
        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for (row,col) in choices:
                temp_board = copy.deepcopy(board)
                temp_board.place(row,col,1)
                eval = self.minimax(temp_board,False,alpha,beta, level+1)[0]
                if eval >max_eval:
                    max_eval = eval
                    best_move = (row,col)
                alpha = max(alpha,max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        
        elif not maximizing:
            min_eval =float('inf')
            for(row,col) in choices:
                temp_board = copy.deepcopy(board)
                temp_board.place(row,col,self.player)
                eval = self.minimax(temp_board,True,alpha,beta,level+1)[0]
                if eval <min_eval:
                    min_eval =eval
                    best_move =(row,col)
                    beta = min(beta,min_eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move


    
    
class Game:
    def __init__(self,player,gamemode):
        self.ai = ai()
        self.board =Board()
        self.player = player
        self.gamemode = gamemode
        self.lines()
        self.buttons()

    def lines(self):
        for i in range(1,COLS+1):
            pygame.draw.line(screen,LINE_COLOR,(i*TILE_SIZE,TILE_SIZE),(i*TILE_SIZE,H),LINE_WIDTH)
        for i in range(1,ROWS+2):
            pygame.draw.line(screen,LINE_COLOR,(0,i*TILE_SIZE,),(W,i*TILE_SIZE,),LINE_WIDTH)

    def buttons(self):
        pass

    def make_move(self,col):
        row = int(self.board.bottom[col])
        if row >5:
            return
        self.board.place(row,col,self.player)
        self.draw_fig(row,col,self.player)
        self.player*=-1

    def draw_fig(self,row,col,player):
        color=(255,0,0)
        if player==1:
            color =(0,0,255)
        center = (col*TILE_SIZE+TILE_SIZE//2,(ROWS-row-1)*TILE_SIZE+TILE_SIZE//2+TILE_SIZE)
        pygame.draw.circle(screen, color, center, RADIUS, CIRCLE_WIDTH)
    



def main():
    game = Game(1, 'ai')
    board = game.board
    ai = game.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1]<TILE_SIZE:
                    pass
                else:
                    if abs(board.final_state())!=100000:
                        col = int(event.pos[0]//TILE_SIZE)
                        game.make_move(col)
                        if board.final_state() != 0:
                            pygame.display.set_caption("Winner")

            pygame.display.update()

        if game.gamemode =='ai'and game.player == ai.player and abs(board.final_state())!=100000:
            row,col = ai.eval(board)
            game.make_move(col)
            if board.final_state() != 0:
                pygame.display.set_caption("Winner")



                

        pygame.display.update()




main()