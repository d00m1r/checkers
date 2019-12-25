from copy import deepcopy
import time

# Global Constants
inf = 1000000
IsPlayerBlack = False
availableTime = 3
maxDepth = 100

class CheckersState:
    def __init__(self, field, botIsBlack, moves):

        self.field = field
        #self._printField()
        self.botIsBlack = botIsBlack#True
        self.moves = moves

    def _printField(self):
        s = ''
        for row in self.field:
            for cell in row:
                s += cell
            print(s)
            s = ''
        print('\n')

    #получить наследников
    def getSuccessors(self):

        def _getSteps(cell):
            #если дамка то добавляются оба направления
            #иначе добавляются направления для соответствующей шашки
            #на выходе список доступных направлений

            whiteSteps = [(-1, -1), (-1, 1)]
            blackSteps = [(1, -1), (1, 1)]

            steps = []
            if cell != 'b': 
                steps.extend(whiteSteps)

            if cell != 'w': 
                steps.extend(blackSteps)

            return steps

        def _generateMoves(board, i, j, successors):

            for step in _getSteps(board[i][j]):
                x, y = i + step[0], j + step[1]

                if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == '_':

                    boardCopy = deepcopy(board)
                    #шаг шашкой на пустое место
                    boardCopy[x][y], boardCopy[i][j] = boardCopy[i][j], '_' 

                    #эволюция шашки в дамку, если стукнулась о край
                    if (x == 7 and self.botIsBlack) or (x == 0 and not self.botIsBlack):
                        boardCopy[x][y] = boardCopy[x][y].upper()
                    
                    #передача шага оппоненту
                    #передаётся совершенный ход
                    #массив объектов
                    successors.append(CheckersState(boardCopy, not self.botIsBlack, [(i, j), (x, y)]))

        def _generateJumps(board, i, j, moves, successors):

            jumpEnd = True

            for step in _getSteps(board[i][j]):
                x, y = i + step[0], j + step[1]

                if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] != '_' and board[i][j].lower() != board[x][y].lower():
                    #попытка перелететь через вражескую шашку
                    xp, yp = x + step[0], y + step[1]

                    if xp >= 0 and xp < 8 and yp >= 0 and yp < 8 and board[xp][yp] == '_':
                        #перелетели через вражескую шашку
                        #save сохраняем значение срубленной шашки
                        board[xp][yp], save = board[i][j], board[x][y]
                        board[i][j] = board[x][y] = '_'

                        #previous сохраняем значение рубящей шашки
                        previous = board[xp][yp]

                        #эволюция шашки в дамку, если стукнулась о край
                        if (xp == 7 and self.botIsBlack) or (xp == 0 and not self.botIsBlack):
                            board[xp][yp] = board[xp][yp].upper()

                        moves.append((xp, yp))

                        #возможен ли следующий прыжок?
                        _generateJumps(board, xp, yp, moves, successors)
                        moves.pop()

                        #завершение прыжка
                        #возвращение состояния
                        board[i][j], board[x][y], board[xp][yp] = previous, save, '_'
                        jumpEnd = False


            if jumpEnd and len(moves) > 1:
                successors.append(CheckersState(deepcopy(board), not self.botIsBlack, deepcopy(moves)))

        player = 'b' if self.botIsBlack else 'w'
        successors = []

        for i in range(8):
            for j in range(8):
                if self.field[i][j].lower() == player:
                    _generateJumps(self.field, i, j, [(i, j)], successors)
        if len(successors) > 0: return successors


        for i in range(8):
            for j in range(8):
                if self.field[i][j].lower() == player:
                    _generateMoves(self.field, i, j, successors)

        return successors

#эвристическая функция
def piecesCount(state):
    # 1 for a normal piece, 1.5 for a king
    black, white = 0, 0

    for row in state.field:
        for cell in row:

            if cell == 'b': black += 1.0
            elif cell == 'B': black += 1.5
            elif cell == 'w': white += 1.0
            elif cell == 'W': white += 1.5

    return black - white if IsPlayerBlack else white - black

def iterativeDeepeningAlphaBeta(state, heuristicFunc):
    startTime = time.time()

    def alphaBetaSearch(state, alpha, beta, depth):

        def _maxValue(state, alpha, beta, depth):
            val = -inf

            for successor in state.getSuccessors():
                val = max(val, alphaBetaSearch(successor, alpha, beta, depth))
                if val >= beta: 
                    return val

                alpha = max(alpha, val)
            return val

        def _minValue(state, alpha, beta, depth):
            val = inf

            for successor in state.getSuccessors():
                val = min(val, alphaBetaSearch(successor, alpha, beta, depth - 1))
                if val <= alpha: 
                    return val

                beta = min(beta, val)
            return val

        #ограничение по времени и глубине
        if depth <= 0 or time.time() - startTime > availableTime:
            return heuristicFunc(state)

        if state.botIsBlack == IsPlayerBlack:
            return _maxValue(state, alpha, beta, depth)
        else:
            return _minValue(state, alpha, beta, depth)

    bestMove = None

    for depth in range(1, maxDepth):

        #ограничение по времени
        if time.time() - startTime > availableTime:
            break

        val = -inf
    
        for successor in state.getSuccessors():

            score = alphaBetaSearch(successor, -inf, inf, depth)
            if score > val:
                val, bestMove = score, successor.moves
                
    return bestMove

if __name__ == '__main__':

    player = input()
    field = ['_b_b_b_b',
            'b_b_b_b_',
            '_b_b_b_b',
            '________',
            '_______w',
            'w_w_w___',
            '_w_w_w_w',
            'w_w_w_w_']
    IsPlayerBlack = player[0] == 'b'

    t = [list(row.rstrip()) for row in field]
    print(t)
    state = CheckersState([list(row.rstrip()) for row in field], IsPlayerBlack, [])
    move = iterativeDeepeningAlphaBeta(state, piecesCount)

    for step in move:
        print (step[0], step[1])