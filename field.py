from tkinter import *
from tkinter import messagebox
from bot import *
import time
from copy import deepcopy


class Field(Frame):

    #make a battlefield
    field = [[0,3,0,3,0,3,0,3],
            [3,0,3,0,3,0,3,0],
            [0,3,0,3,0,3,0,3],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0]]

    player = True##val = 1 -> plr1; val = 0 -> plr2(comp) 

    def __init__(self, bot, parent=None):          
        Frame.__init__(self, parent)

        self.__bot = bot
        self.pack()
        self.setUI()

        #create 2 players
        self.plr1 = Player()
        #self.plr2 = CheckersState() if self.__bot else Player()
        self.plr2 = Player()

        self.draw_field(0,0,0,0)



    def setUI(self):

        #load pictures for checkers
        self.ch1 = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/w.gif")#plr1
        self.q1 = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/wq.gif")
        self.ch2 = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/b.gif")#plr2
        self.q2 = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/bq.gif")
        self.checkers = [0,self.ch1, self.q1, self.ch2, self.q2]

        #create field for checkers
        self.canv = Canvas(self, width = 800, height = 800, bg="white")
        self.canv.pack()
    
        if self.__bot:
            self.canv.bind("<Button-1>", self.run_with_bot)
        else:
            self.canv.bind("<Button-1>", self.run)

        widget1 = Button(self, text='Quit', command = self.quit)
        widget1.pack(side='right', expand='yes', fill = BOTH)


    def run(self, event):

        #checker coordinates calculation
        x, y = (event.x)//100, (event.y)//100

        if Field.player:
            if Field.field[y][x] == 1 or Field.field[y][x] == 2:
                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr1.x1, self.plr1.y1 = x, y
                
            elif Field.field[y][x] == 0 and self.plr1.x1 != -1 and self.plr1.x2 == -1:
                self.plr1.x2, self.plr1.y2 = x, y
                if self.plr1.check_move_player():

                    if self.plr1.make_move():
                        Field.player = False#передача хода

                    self.draw_field(self.plr1.x1, self.plr1.y1, self.plr1.x2, self.plr1.y2)
                    self.plr1.x1 = self.plr1.y1 = self.plr1.x2 = self.plr1.y2 = -1
                self.plr1.x2, self.plr1.y2 = -1, -1

        elif not(Field.player):
            if Field.field[y][x]==3 or Field.field[y][x]==4:

                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr2.x1, self.plr2.y1 = x, y
                
            elif Field.field[y][x] == 0 and self.plr2.x1 != -1 and self.plr2.x2 == -1:
                self.plr2.x2, self.plr2.y2 = x, y

                if self.plr2.check_move_player():

                    if self.plr2.make_move():
                        Field.player = True#pass the move

                    self.draw_field(self.plr2.x1, self.plr2.y1, self.plr2.x2, self.plr2.y2)
                    self.plr2.x1 = self.plr2.y1 = self.plr2.x2 = self.plr2.y2 = -1
                self.plr2.x2, self.plr2.y2 = -1, -1

    def quit(self):
        ans = messagebox.askokcancel('Verify exit', "Do you really want exit?")
        if ans: 
            Frame.quit(self)

    def run_with_bot(self, event):
        #checker coordinates calculation
        x, y = (event.x)//100, (event.y)//100
        
        if Field.player:
            if Field.field[y][x]==1 or Field.field[y][x]==2:
                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr1.x1, self.plr1.y1 = x, y
                
            elif Field.field[y][x] == 0 and self.plr1.x1 != -1 and self.plr1.x2 == -1:
                self.plr1.x2, self.plr1.y2 = x, y
                if self.plr1.check_move_player():

                    if self.plr1.make_move():
                        Field.player = False#передача хода

                    self.draw_field(self.plr1.x1, self.plr1.y1, self.plr1.x2, self.plr1.y2)
                    self.plr1.x1 = self.plr1.y1 = self.plr1.x2 = self.plr1.y2 = -1
                self.plr1.x2, self.plr1.y2 = -1, -1

        if not(Field.player):
            
            grid, s = [], ''
            for row in Field.field:
                for el in row:
                    if el == 0:
                        s += '_'
                    elif el == 1:
                        s += 'w'
                    elif el == 2:
                        s += 'W'
                    elif el == 3:
                        s += 'b'
                    elif el == 4:
                        s += 'B'
                grid.append(s)
                s =''

            #print(grid)

            state = CheckersState([list(row.rstrip()) for row in grid], True, [])
            move = iterativeDeepeningAlphaBeta(state, piecesCount)
            
            #print(move)
            if self.make_move_bot(move):
                Field.player = True#передача хода

            self.draw_field(move[0][1], move[0][0], move[1][1], move[1][0])
                    
        
    def make_move_bot(self, move):
        
        x1, y1, x2, y2 = move[0][1], move[0][0], move[1][1], move[1][0]

        val1, val2 = 3, 4
        val_q = 7

        #превращение
        if y2 == val_q and Field.field[y1][x1] == val1:
            Field.field[y1][x1] = val2

        #делаем ход           
        Field.field[y2][x2] = Field.field[y1][x1]
        Field.field[y1][x1] = 0
    
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
            if Field.field[y_pos][x_pos] != 0:
                Field.field[y_pos][x_pos] = 0 

                #проверяем ход той же пешкой...
                if Field.field[y2][x2] == val1 or Field.field[y2][x2] == val2:
                    if self.look_move([],x2, y2):#возвращаем список доступных ходов
                        return False
                    else:
                        return True
            return True

    def look_move(self, move_list, x, y):
        if Field.player:
            val1, val2, val3, val4 = 1, 2, 3, 4

        elif not(Field.player):
            val1, val2, val3, val4 = 3, 4, 1, 2

        if Field.field[y][x] == val1:#шашка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                if 0 <= y+iy+iy <= 7 and 0 <= x+ix+ix <= 7:
                    if Field.field[y+iy][x+ix] == val3 or Field.field[y+iy][x+ix] == val4:
                        if Field.field[y+iy+iy][x+ix+ix] == 0:
                            move_list.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка

        elif Field.field[y][x] == val2:#дамка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                osh=0#определение правильности хода
                for i in range(1,8):
                    if 0 <= y+iy*i <= 7 and 0 <= x+ix*i <= 7:
                        if osh == 1:
                            move_list.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                        if Field.field[y+iy*i][x+ix*i] == val3 or Field.field[y+iy*i][x+ix*i] == val4:
                            osh+=1
                        if Field.field[y+iy*i][x+ix*i] == val1 or Field.field[y+iy*i][x+ix*i] == val2 or osh==2:
                            if osh>0:
                                move_list.pop()#удаление хода из списка
                            break
                            
        return move_list

    def draw_field(self, x1, y1, x2, y2):
        k = 100
        
        self.canv.delete('all')
        
        #checker's highlighting
        self.red_frame = self.canv.create_rectangle(-5,-5,-5,-5, outline="red",width=5)
        self.canv.coords(self.red_frame, x1*100, y1*100, x1*100+100, y1*100+100)
        x = 0
        while x < 8*k:#рисуем доску
            y=1*k
            while y<8*k:
                self.canv.create_rectangle(x, y, x+k, y+k,fill="black")
                self.canv.create_rectangle(x+1*k, y-1*k, x+2*k, y,fill="black")
                y+=2*k
            x+=2*k

        for y in range(8):#рисуем стоячие пешки
            for x in range(8):
                z = Field.field[y][x]
                if z:  
                    if (x1, y1) != (x,y):#стоячие пешки?
                        self.canv.create_image(x*k,y*k, anchor=NW, image = self.checkers[z])

        #рисуем активную пешку         
        z = Field.field[y1][x1]
        if z:
            self.canv.create_image(x1*k, y1*k, anchor=NW, image=self.checkers[z],tag='ani')

        #вычисление коэф. для анимации
        kx = 1 if x1 < x2 else -1
        ky = 1 if y1 < y2 else -1
        for i in range(abs(x1 - x2)):#анимация перемещения пешки
            for ii in range(33):
                self.canv.move('ani',0.03*k*kx,0.03*k*ky)
                self.canv.update()#обновление
                time.sleep(0.01)
        
'''
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
PLAYER
'''

class Player(Field): 

    def __init__(self):

        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1    

    def check_move_player(self):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2

        move_list = self.obligatory_move()#necessary move
        
        if not(move_list):    
            move_list = self.remaining_move()#check another moves
        if move_list:
            if ((x1, y1),(x2, y2)) in move_list:#the move complies with the rules
                return True
            else:
                return False
        return False

    def obligatory_move(self):#проверка наличия обязательных ходов
        move_list = []#список ходов
        for y in range(8):#сканируем всё поле
            for x in range(8):
                move_list = self.look_move(move_list, x, y)
        return move_list

    def look_move(self, move_list, x, y):
        if Field.player:
            val1, val2, val3, val4 = 1, 2, 3, 4

        elif not(Field.player):
            val1, val2, val3, val4 = 3, 4, 1, 2

        if Field.field[y][x] == val1:#шашка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                if 0 <= y+iy+iy <= 7 and 0 <= x+ix+ix <= 7:
                    if Field.field[y+iy][x+ix] == val3 or Field.field[y+iy][x+ix] == val4:
                        if Field.field[y+iy+iy][x+ix+ix] == 0:
                            move_list.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка

        elif Field.field[y][x] == val2:#дамка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                osh=0#определение правильности хода
                for i in range(1,8):
                    if 0 <= y+iy*i <= 7 and 0 <= x+ix*i <= 7:
                        if osh == 1:
                            move_list.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                        if Field.field[y+iy*i][x+ix*i] == val3 or Field.field[y+iy*i][x+ix*i] == val4:
                            osh+=1
                        if Field.field[y+iy*i][x+ix*i] == val1 or Field.field[y+iy*i][x+ix*i] == val2 or osh==2:
                            if osh>0:
                                move_list.pop()#удаление хода из списка
                            break
                            
        return move_list

    def remaining_move(self):#проверка наличия остальных ходов для игрока
        if Field.player:
            val1, val2, val3, val4, val = 1, 2, 3, 4, -1

        elif not(Field.player):
            val1, val2, val3, val4, val = 3, 4, 1, 2, 1

        move_list = []
        for y in range(8):#сканируем всё поле
            for x in range(8):

                if Field.field[y][x] == val1:#шашка
                    for ix,iy in (-1,val),(1,val):
                        if 0<=y+iy<=7 and 0<=x+ix<=7:
                            if Field.field[y+iy][x+ix]==0:
                                move_list.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                            if Field.field[y+iy][x+ix] == val3 or Field.field[y+iy][x+ix] == val4:

                                if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                    if Field.field[y+iy*2][x+ix*2] == 0:
                                        move_list.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
                
                if Field.field[y][x] == val2:#дамка
                    for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                        osh=0#определение правильности хода
                        for i in range(1,8):
                            if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                                if Field.field[y+iy*i][x+ix*i] == 0:
                                    move_list.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                                if Field.field[y+iy*i][x+ix*i] == val3 or Field.field[y+iy*i][x+ix*i] == val4:
                                    osh+=1
                                if Field.field[y+iy*i][x+ix*i] == val1 or Field.field[y+iy*i][x+ix*i] == val2 or osh==2:
                                    break
        return move_list

    def make_move(self):
        
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2

        if Field.player:
            val1, val2 = 1, 2
            val_q = 0

        elif not(Field.player):
            val1, val2 = 3, 4
            val_q = 7

        '''#сохранение предыдущего шага
        Field.prev_field = Field.field[:]
        for el in Field.field:
            print(el)
        print('\n')
        '''
        #превращение
        if y2 == val_q and Field.field[y1][x1] == val1:
            Field.field[y1][x1] = val2

        #делаем ход           
        Field.field[y2][x2] = Field.field[y1][x1]
        Field.field[y1][x1] = 0
    
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
            if Field.field[y_pos][x_pos] != 0:
                Field.field[y_pos][x_pos] = 0 

                #проверяем ход той же пешкой...
                if Field.field[y2][x2] == val1 or Field.field[y2][x2] == val2:
                    if self.look_move([],x2, y2):#возвращаем список доступных ходов
                        return False
                    else:
                        return True
            return True



    '''
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    BOT
    '''
    