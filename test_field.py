from tkinter import *
from tkinter import messagebox
from bot import *
#from test_player import *
import time
from copy import deepcopy

PLAYER = True #1 - plr1, 0 - plr2(comp)

class Field(Frame):

    t = ['_b_b_b_b',
        'b_b_b_b_',
        '_b_b_b_b',
        '________',
        '________',
        'w_w_w_w_',
        '_w_w_w_w',
        'w_w_w_w_']

    field = [list(row.rstrip()) for row in t]
    
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

        self.setUI()
        self.drawField(-1,-1,-1,-1)

    def pvbMode(self):
        Field.__gameMode = 1
        self.plr1 = Player()

        self.setUI()
        self.drawField(-1,-1,-1,-1)

    def setUI(self):

        self.__intro.destroy()
        self.widget1.destroy()#pack_forget()
        self.widget2.destroy()
        self.parent.geometry("820x840")

        #load pictures for checkers
        self.w = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/w.gif")#plr1
        self.W = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/wq.gif")
        self.b = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/b.gif")#plr2
        self.B = PhotoImage(file="/home/damir//projects/PythonCheckers/checkers/pic/bq.gif")

        self.checkers = {'w':self.w , 'W':self.W, 'b':self.b, 'B':self.B}

        #create field for checkers
        self.canv = Canvas(self, width = 800, height = 800, bg="white")
        self.canv.pack()

        if Field.__gameMode == 0:
            self.canv.bind("<Button-1>", self.click)
        elif Field.__gameMode == 1:
            self.canv.bind("<Button-1>", self.clickWithBot)

        widget = Button(self, text='Quit', command = self.quit)
        widget.pack(side='right', expand='yes', fill = BOTH)

    def quit(self):
        ans = messagebox.askokcancel('Verify exit', "Do you really want exit?")
        if ans: 
            Frame.quit(self)

    def drawField(self, x1, y1, x2, y2):
        k = 100
        
        self.canv.delete('all')
        
        #checker's highlighting
        self.red_frame = self.canv.create_rectangle(-5,-5,-5,-5, outline="red",width = 5)
        self.canv.coords(self.red_frame, x1*100, y1*100, x1*100+100, y1*100+100)
        self.updateField()

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
                if z != '_':  
                    if (x1, y1) != (x,y):#стоячие пешки?
                        img = self.checkers[z]
                        self.canv.create_image(x*k, y*k, anchor=NW, image = img)

        #рисуем активную пешку         
        z = Field.field[y1][x1]
        if z != '_':
            img = self.checkers[z]
            self.canv.create_image(x1*k, y1*k, anchor=NW, image=self.checkers[z],tag='ani')

        #вычисление коэф. для анимации
        kx = 1 if x1 < x2 else -1
        ky = 1 if y1 < y2 else -1
        for i in range(abs(x1 - x2)):#анимация перемещения пешки
            for ii in range(33):
                self.canv.move('ani',0.03*k*kx,0.03*k*ky)
                self.canv.update()#обновление
                time.sleep(0.01)
        
    def updateField(self):
        Field.field = deepcopy(Player.field)
        

    def click(self, event):
        global PLAYER
        #checker coordinates calculation
        x, y = (event.x)//100, (event.y)//100
        
        if PLAYER:
            
            if Player.field[y][x].lower() == 'w':
                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr1.x1, self.plr1.y1 = x, y

            elif Player.field[y][x] == '_' and self.plr1.x1 != -1 and self.plr1.x2 == -1:
                self.plr1.x2, self.plr1.y2 = x, y
                if self.plr1.check_move_player():

                    if self.plr1.make_move():
                        PLAYER = False#передача хода
                    
                    self.drawField(self.plr1.x1, self.plr1.y1, self.plr1.x2, self.plr1.y2)
                    self.plr1.x1 = self.plr1.y1 = self.plr1.x2 = self.plr1.y2 = -1
                self.plr1.x2, self.plr1.y2 = -1, -1

        elif not PLAYER:
            if Player.field[y][x].lower() == 'b':
                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr2.x1, self.plr2.y1 = x, y

            elif Player.field[y][x] == '_' and self.plr2.x1 != -1 and self.plr2.x2 == -1:
                self.plr2.x2, self.plr2.y2 = x, y
                if self.plr2.check_move_player():
                    
                    if self.plr2.make_move():
                        PLAYER = True#pass the move

                    self.drawField(self.plr2.x1, self.plr2.y1, self.plr2.x2, self.plr2.y2)
                    self.plr2.x1 = self.plr2.y1 = self.plr2.x2 = self.plr2.y2 = -1
                self.plr2.x2, self.plr2.y2 = -1, -1

    def clickWithBot(self, event):
        #checker coordinates calculation
        x, y = (event.x)//100, (event.y)//100
        global PLAYER
        if PLAYER:
            if Player.field[y][x].lower() == 'w':
                self.canv.coords(self.red_frame, x*100, y*100, x*100+100, y*100+100)
                self.plr1.x1, self.plr1.y1 = x, y
                
            elif Player.field[y][x] == '_' and self.plr1.x1 != -1 and self.plr1.x2 == -1:
                self.plr1.x2, self.plr1.y2 = x, y
                if self.plr1.check_move_player():

                    if self.plr1.make_move():
                        PLAYER = False#передача хода

                    self.drawField(self.plr1.x1, self.plr1.y1, self.plr1.x2, self.plr1.y2)
                    self.plr1.x1 = self.plr1.y1 = self.plr1.x2 = self.plr1.y2 = -1
                self.plr1.x2, self.plr1.y2 = -1, -1

        if not PLAYER:
            
            state = CheckersState(Field.field, True, [])
            move = iterativeDeepeningAlphaBeta(state, piecesCount)
            
            
            if self.make_move_bot(move):
                PLAYER = True#передача хода

            self.drawField(move[0][1], move[0][0], move[1][1], move[1][0])

    def make_move_bot(self, move):
        
        x1, y1, x2, y2 = move[0][1], move[0][0], move[1][1], move[1][0]

        val1, val2 = 'b', 'B'
        val_q = 7

        #превращение
        if y2 == val_q and Field.field[y1][x1] == val1:
            Field.field[y1][x1] = val2

        #делаем ход           
        Field.field[y2][x2] = Field.field[y1][x1]
        Field.field[y1][x1] = '_'
    
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
        global PLAYER
        if PLAYER:
            val1, val2, val3, val4 = 'w', 'W', 'b', 'B'

        elif not PLAYER:
            val1, val2, val3, val4 = 'b', 'B', 'w', 'W'

        if Field.field[y][x] == val1:#шашка
            for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                if 0 <= y+iy+iy <= 7 and 0 <= x+ix+ix <= 7:
                    if Field.field[y+iy][x+ix] == val3 or Field.field[y+iy][x+ix] == val4:
                        if Field.field[y+iy+iy][x+ix+ix] == '_':
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
        print(move_list)
        if not(move_list):    
            move_list = self.remaining_move()#check another moves

        if move_list:
            if ((self.x1, self.y1),(self.x2, self.y2)) in move_list:#the move complies with the rules
                return True
            else:
                return False
        return False

    def obligatory_move(self):#проверка наличия обязательных ходов
        move_list = []
        for y in range(8):#сканируем всё поле
            for x in range(8):
                move_list = self.look_move(move_list, x, y)
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
    
if __name__ == '__main__':
    root = Tk()
    root.title("Checkers")
    app = Field(root)
    app.pack()
    root.mainloop()