from tkinter import *
from tkinter import messagebox
from bot import *
from copy import deepcopy


class Field(Frame):

    field = [[0,3,0,3,0,3,0,3],
            [3,0,3,0,3,0,3,0],
            [0,3,0,3,0,3,0,3],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0]]

    player = True#val = 1 -> plr1; val = 0 -> plr2(comp) 

    __gameMode = 0#0 - PVP, 1 - PVB

    def __init__(self, parent = None):          
        Frame.__init__(self, parent)
        self.parent = parent

        self.__intro = Label(self, text = 'Choose game mode')
        self.__intro.pack()

        self.widget1 = Button(self, text='PvsP mode', command = self.pvpMode)
        self.widget1.pack(side='right', expand='yes', fill = BOTH)

        self.widget2 = Button(self, text='PvsBot mode', command = self.pvbMode)
        self.widget2.pack(side='left', expand='yes', fill = BOTH)

        self.pack()#!
    
    def pvpMode(self):
        Field.__gameMode = 0
        self.plr1 = Player()
        self.plr2 = Player()

        self.__setUI()
        self._drawField(-1,-1,-1,-1)

    def pvbMode(self):
        Field.__gameMode = 1
        self.plr1 = Player()

        self.__setUI()
        self._drawField(-1,-1,-1,-1)

    def __setUI(self):

        self.__intro.destroy()
        self.widget1.destroy()#pack_forget()
        self.widget2.destroy()
        self.parent.geometry("820x840")

        self.w = PhotoImage(file="/home/damir/projects/PythonCheckers/checkers/pic/w.gif")#plr1
        self.W = PhotoImage(file="/home/damir/projects/PythonCheckers/checkers/pic/wq.gif")
        self.b = PhotoImage(file="/home/damir/projects/PythonCheckers/checkers/pic/b.gif")#plr2
        self.B = PhotoImage(file="/home/damir/projects/PythonCheckers/checkers/pic/bq.gif")

        self.checkers = [0,self.w, self.W, self.b, self.B]
        #self.checkers = {'w':self.w , 'W':self.W, 'b':self.b, 'B':self.B}

        #создание холста для шашек
        self.canv = Canvas(self, width = 800, height = 800, bg="white")
        self.canv.pack()

        if Field.__gameMode == 0:
            self.canv.bind("<Button-1>", self.__run)
        elif Field.__gameMode == 1:
            self.canv.bind("<Button-1>", self.__runBot)

        widget = Button(self, text='Quit', command = self.__quit)
        widget.pack(side='right', expand='yes', fill = BOTH)

    def __quit(self):
        ans = messagebox.askokcancel('Verify exit', "Do you really want exit?")
        if ans: 
            Frame.quit(self)

    def __run(self, event):

        x, y = (event.x)//100, (event.y)//100
        if Field.player:
            if Field.field[y][x]==1 or Field.field[y][x]==2:
                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr1.x1, self.plr1.y1 = x, y
                
            elif Field.field[y][x] == 0 and self.plr1.x1 != -1 and self.plr1.x2 == -1:
                self.plr1.x2, self.plr1.y2 = x, y
                if self.plr1._checkMove_player():

                    if self.plr1._makeMove():
                        Field.player = False#передача хода

                    self._drawField(self.plr1.x1, self.plr1.y1, self.plr1.x2, self.plr1.y2)
                    self.plr1.x1 = self.plr1.y1 = self.plr1.x2 = self.plr1.y2 = -1
                self.plr1.x2, self.plr1.y2 = -1, -1

        elif not(Field.player):
            if Field.field[y][x]==3 or Field.field[y][x]==4:

                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr2.x1, self.plr2.y1 = x, y
                
            elif Field.field[y][x] == 0 and self.plr2.x1 != -1 and self.plr2.x2 == -1:
                self.plr2.x2, self.plr2.y2 = x, y

                if self.plr2._checkMove_player():

                    if self.plr2._makeMove():
                        Field.player = True#pass the move

                    self._drawField(self.plr2.x1, self.plr2.y1, self.plr2.x2, self.plr2.y2)
                    self.plr2.x1 = self.plr2.y1 = self.plr2.x2 = self.plr2.y2 = -1
                self.plr2.x2, self.plr2.y2 = -1, -1

    def __runBot(self, event):
        #checker coordinates calculation
        x, y = (event.x)//100, (event.y)//100
        
        if Field.player:
            if Field.field[y][x]==1 or Field.field[y][x]==2:
                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr1.x1, self.plr1.y1 = x, y
                
            elif Field.field[y][x] == 0 and self.plr1.x1 != -1 and self.plr1.x2 == -1:
                self.plr1.x2, self.plr1.y2 = x, y
                if self.plr1._checkMove_player():

                    if self.plr1._makeMove():
                        Field.player = False#передача хода

                    self._drawField(self.plr1.x1, self.plr1.y1, self.plr1.x2, self.plr1.y2)
                    self.plr1.x1 = self.plr1.y1 = self.plr1.x2 = self.plr1.y2 = -1
                self.plr1.x2, self.plr1.y2 = -1, -1

        if not(Field.player):
            fieldCopy = deepcopy(Field.field)

            for x in range(8):
                for y in range(8):
                    if fieldCopy[x][y] == 0:
                        fieldCopy[x][y] = '_'
                    elif fieldCopy[x][y] == 1:
                        fieldCopy[x][y] = 'w'
                    elif fieldCopy[x][y] == 2:
                        fieldCopy[x][y] = 'W'
                    elif fieldCopy[x][y] == 3:
                        fieldCopy[x][y] = 'b'
                    elif fieldCopy[x][y] == 4:
                        fieldCopy[x][y] = 'B'

            state = CheckersState(fieldCopy, True, [])
            move = iterativeDeepeningAlphaBeta(state, piecesCount)
            
            if self._makeMove_bot(move):
                Field.player = True#передача хода

            self._drawField(move[0][1], move[0][0], move[1][1], move[1][0])
                     
    def _makeMove_bot(self, move):
        
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
                    if self._lookMove([],x2, y2):#возвращаем список доступных ходов
                        return False
                    else:
                        return True
            return True

    def _lookMove(self, move_list, x, y):
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

    def _drawField(self, x1, y1, x2, y2):
        k = 100
        
        self.canv.delete('all')
        
        #подсветка шашки
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
        self.canv.update()

        
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

    def _checkMove_player(self):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2

        move_list = self._mustMove()#необходимые шаги
        
        if not(move_list):    
            move_list = self._remainingMove()#остальные ходы

        if move_list:
            if ((x1, y1),(x2, y2)) in move_list:#движение совпадают с правилами игры
                return True
            else:
                return False
        return False

    def _mustMove(self):#проверка наличия обязательных ходов
        move_list = []#список ходов
        for y in range(8):#сканируем всё поле
            for x in range(8):
                move_list = self._lookMove(move_list, x, y)
        return move_list

    def _lookMove(self, move_list, x, y):
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

    def _remainingMove(self):#проверка наличия остальных ходов для игрока
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

    def _makeMove(self):
        
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2

        if Field.player:
            val1, val2 = 1, 2
            val_q = 0

        elif not(Field.player):
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
                    if self._lookMove([],x2, y2):#возвращаем список доступных ходов
                        return False
                    else:
                        return True
            return True

    