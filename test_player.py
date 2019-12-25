from tkinter import *
import time

PLAYER = True #1 - plr1, 0 - plr2(comp)

class Player():

    field = [['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
            ['b', '_', 'b', '_', 'b', '_', 'b', '_'],
            ['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '_'],
            ['w', '_', 'w', '_', 'w', '_', 'w', '_'],
            ['_', 'w', '_', 'w', '_', 'w', '_', 'w'],
            ['w', '_', 'w', '_', 'w', '_', 'w', '_']]

    

    def __init__(self):

        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1    

    def check_move_player(self):
        
        move_list = self.obligatory_move()#necessary move
        if not(move_list):    
            move_list = self.remaining_move()#check another moves

        if move_list:
            if ((self.x1, self.y1),(self.x2, self.y2)) in move_list:#the move complies with the rules
                return True
            else:
                return False
        return False

    def obligatory_move(self):#проверка наличия обязательных ходов
        for y in range(8):#сканируем всё поле
            for x in range(8):
                move_list = self.look_move([], x, y)
        return move_list

    def look_move(self, move_list, x, y):
        global PLAYER
        if PLAYER:
            val1, val2, val3, val4 = 'w', 'W', 'b', 'B'

        elif not PLAYER:
            val1, val2, val3, val4 = 'b', 'B', 'w', 'W'

        if Player.field[y][x] == val1:#шашка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                if 0 <= y+iy+iy <= 7 and 0 <= x+ix+ix <= 7:
                    if Player.field[y+iy][x+ix] == val3 or Player.field[y+iy][x+ix] == val4:
                        if Player.field[y+iy+iy][x+ix+ix] == 0:
                            move_list.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка

        elif Player.field[y][x] == val2:#дамка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                osh=0#определение правильности хода
                for i in range(1,8):
                    if 0 <= y+iy*i <= 7 and 0 <= x+ix*i <= 7:
                        if osh == 1:
                            move_list.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                        if Player.field[y+iy*i][x+ix*i] == val3 or Player.field[y+iy*i][x+ix*i] == val4:
                            osh+=1
                        if Player.field[y+iy*i][x+ix*i] == val1 or Player.field[y+iy*i][x+ix*i] == val2 or osh==2:
                            if osh>0:
                                move_list.pop()#удаление хода из списка
                            break
                            
        return move_list

    def remaining_move(self):#проверка наличия остальных ходов для игрока
        global PLAYER
        if PLAYER:
            val1, val2, val3, val4, val = 'w', 'W', 'b', 'B', -1

        elif not PLAYER:
            val1, val2, val3, val4, val = 'b', 'B', 'w', 'W', 1

        move_list = []
        for y in range(8):#сканируем всё поле
            for x in range(8):

                if Player.field[y][x] == val1:#шашка
                    for ix,iy in (-1,val),(1,val):
                        if 0<=y+iy<=7 and 0<=x+ix<=7:
                            if Player.field[y+iy][x+ix]=='_':
                                move_list.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                            if Player.field[y+iy][x+ix] == val3 or Player.field[y+iy][x+ix] == val4:

                                if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                    if Player.field[y+iy*2][x+ix*2] == '_':
                                        move_list.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
                
                if Player.field[y][x] == val2:#дамка
                    for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                        osh=0#определение правильности хода
                        for i in range(1,8):
                            if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                                if Player.field[y+iy*i][x+ix*i] == '_':
                                    move_list.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                                if Player.field[y+iy*i][x+ix*i] == val3 or Player.field[y+iy*i][x+ix*i] == val4:
                                    osh+=1
                                if Player.field[y+iy*i][x+ix*i] == val1 or Player.field[y+iy*i][x+ix*i] == val2 or osh==2:
                                    break
        return move_list

    def make_move(self):
        global PLAYER
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        
        if PLAYER:
            val1, val2 = 'w', 'W'
            val_q = 0

        elif not PLAYER:
            val1, val2 = 'b', 'B'
            val_q = 7

        #превращение
        if y2 == val_q and Player.field[y1][x1] == val1:
            Player.field[y1][x1].upper()

        #делаем ход           
        Player.field[y2][x2] = Player.field[y1][x1]
        Player.field[y1][x1] = '_'
    
        #рубим пешку игрока
        kx = ky = 1
        if x1 < x2:
            kx =- 1

        if y1 < y2:
            ky =- 1

        x_pos, y_pos = x2, y2

        while (x1 != x_pos) or (y1!=y_pos):
            x_pos += kx
            y_pos += ky
            
            #!h
            if Player.field[y_pos][x_pos] != '_':
                Player.field[y_pos][x_pos] = '_' 

                #проверяем ход той же пешкой...
                if Player.field[y2][x2] == val1 or Player.field[y2][x2] == val2:
                    if self.look_move([],x2, y2):#возвращаем список доступных ходов
                        return False
                    else:
                        return True
            return True
