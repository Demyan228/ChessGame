from chess_typing import Position, State
from typing import Tuple
from itertools import product
from copy import deepcopy


def is_valid(x, y):
    if x < 0 or y < 0 or x > 7 or y > 7:
        return False
    return True



class ChessGameEngine:
    figures = {1: "pawn", 2: "bishop", 3: "knight", 4: "rook", 5: "queen", 6: "king"}
    start_board = """
    43256234
    11111111
    00000000
    00000000
    00000000
    00000000
    11111111
    43256234
    """
    start_board = start_board.strip().replace(" ", "")
    start_board = start_board.split("\n")

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = self._create_board()
        self._last_step = None
        self._is_white_king_stay = True
        self._is_black_king_stay = True
        self._is_game_over = False

    def is_game_over(self) -> bool:
        return self._is_game_over

    def get_state(self) -> State:
        return deepcopy(self.board)

    def get_figure(self, pos : Position) -> int:
        return self.board[pos[1]][pos[0]]

    def make_turn(self, pos1: Position, pos2: Position) -> None:
        f0 = self.board[pos1[1]][pos1[0]] * 1
        if f0 == 6:
            self._is_white_king_stay = False
        if f0 == -6:
            self._is_black_king_stay = False
        self._last_step = [*pos1, *pos2, self.board[pos1[1]][pos1[0]]]
        self.board[pos1[1]][pos1[0]],\
        self.board[pos2[1]][pos2[0]] = 0, self.board[pos1[1]][pos1[0]]
        if f0 < 0 and ChessSteper.is_mat(self.board, self._last_step, self._is_white_king_stay, -1):
            self._is_game_over = True
        if f0 > 0 and ChessSteper.is_mat(self.board, self._last_step, self._is_black_king_stay, 1):
            self._is_game_over = True

    def get_places(self, pos: Position) -> Tuple[Position]:
        king_stay = self._is_black_king_stay
        if self.board[pos[1]][pos[0]] > 0:
            king_stay = self._is_white_king_stay
        return ChessSteper.get_places(self.board, pos[0], pos[1], self._last_step, king_stay)

    def _create_board(self):
        board = []
        for i in range(8):
            line = []
            for j in range(8):
                f = int(ChessGameEngine.start_board[i][j])
                if i <=1:
                    f *= -1
                line.append(f)
            board.append(line)
        return board


class ChessSteper:
    @staticmethod
    def get_places(board, x, y, last_step=None, is_king_stay=None):
        func = ChessSteper.get_func(board, x, y)
        c = -1 if board[y][x] > 0 else 1
        if func == ChessSteper.pawn:
            res = func(board, last_step, x, y, c)
        elif func == ChessSteper.king:
            res = func(board, is_king_stay, x, y, c)
        else:
            res = func(board, x, y, c)
        if ChessSteper.is_check(board, c):
            return ChessSteper.steps_in_check(x, y, res, board, c)
        return tuple(res)


    @staticmethod
    def steps_in_check(x0, y0, cords1, board, c):
        res_cords1 = []
        #print(*board, sep="\n")
        for x2, y2 in cords1:
            bc = deepcopy(board)
            bc[y2][x2], bc[y0][x0] = bc[y0][x0], 0
            #print(board[y0][x0], x2, y2)
            if not ChessSteper.is_check(bc, c):
                res_cords1.append(tuple([x2, y2]))
        return tuple(res_cords1)

    @staticmethod
    def is_mat(board, last_step, is_king_stay, c):
        for x in range(8):
            for y in range(8):
                if board[y][x] * c < 0:
                    if ChessSteper.get_places(board, x, y, last_step, is_king_stay):
                        return False
        return True

    @staticmethod
    def pawn(board, last_step, x, y, c):
        res = []
        if board[y + c][x] == 0:
            res.append(tuple([x, y + c]))
            if (y == 6 or y == 1) and is_valid(x, y + c * 2) and board[y + c * 2][x] == 0:
                res.append(tuple([x, y + c * 2]))
        if last_step:
            fl1 = [last_step[2], last_step[3]] in [[x + 1, y], [x - 1, y]] # пришла ли она туда куда нам надо
            fl2 = [last_step[0], last_step[1]] in [[x + 1, y - 2], [x - 1, y - 2]] # пришла ли она окуда нам надо
            if last_step[4] == c and fl1 and fl2:
                res.append(tuple([last_step[0], y + c]))
        if is_valid(y + c, x + 1) and (board[y + c][x + 1] * c > 0):
            res.append(tuple([x + 1, y + c]))
        if is_valid(y + c, x - 1) and (board[y + c][x - 1] * c > 0):
            res.append(tuple([x - 1, y + c]))
        return tuple(res)

    @staticmethod
    def bishop(board, x, y, c):
        res = []
        for j in product([1, -1], repeat=2):
            for i in range(1, 8):
                nx, ny = x + i * j[0], y + i * j[1]
                if not is_valid(nx, ny) or board[ny][nx] * c < 0:
                    break
                res.append(tuple([nx, ny]))
                if board[ny][nx] != 0:
                    break
        return tuple(res)

    @staticmethod
    def knight(board, x, y, c):
        res = []
        for j in [[2, 1], [2, -1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [1, -2], [-1, -2]]:
            if is_valid(x + j[0], y + j[1]) and (board[y + j[1]][x + j[0]] * c >= 0):
                res.append(tuple([x + j[0], y + j[1]]))
        return tuple(res)

    @staticmethod
    def rook(board, x, y, c):
        res = []
        for j in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            for i in range(1, 8):
                nx, ny = x + i * j[0], y + i * j[1]
                if not is_valid(nx, ny) or board[ny][nx] * c < 0:
                    break
                res.append(tuple([nx, ny]))
                if board[ny][nx] != 0:
                    break
        return tuple(res)

    @staticmethod
    def queen(board, x, y, c):
        return ChessSteper.bishop(board, x, y, c) + ChessSteper.rook(board, x, y, c)

    @staticmethod
    def king(board, is_king_stay, x, y, c):
        res = []
        beats = ChessSteper.get_all_beats(board, c)
        for i in ChessSteper.king_beats(x, y):
            if board[i[1]][i[0]] * c >= 0 and i not in beats:
                res.append(i)
        if is_king_stay:
            r = ChessSteper.check_castling(board, beats, x, y, c)
            res += r
        return tuple(res)

    @staticmethod
    def is_check(board, c):
        b = ChessSteper.get_all_beats(board, c)
        for x in range(8):
            for y in range(8):
                if board[y][x] == -6 * c:
                    return tuple([x, y]) in b

    @staticmethod
    def check_castling(board, beats, x, y, c):
        res = []
        f = False
        for i in range(1, 3):
            if board[y][x + i] == 0 and tuple(board[y][x + i]) not in beats:
                f = True
        if board[y][x + 3] == -4 * c and f:
            res.append(tuple([x + 2, y]))
        f = False
        for i in range(1, 4):
            if board[y][x - i] == 0 and tuple(board[y][x - i]) not in beats:
                f = True
        if board[y][x - 4] == -4 * c and f:
            res.append(tuple([x - 4, y]))
        return res

    @staticmethod
    def king_beats(x, y):
        res = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if is_valid(x + i, y + j) and not (i == 0 and j == 0):
                    res.append(tuple([x + i, y + j]))
        return res

    @staticmethod
    def get_func(board, x, y):
        figures_steps = {1: ChessSteper.pawn, 2: ChessSteper.bishop, 3: ChessSteper.knight,
                         4: ChessSteper.rook, 5: ChessSteper.queen, 6: ChessSteper.king}
        f = board[y][x]
        func = figures_steps[abs(f)]
        return func


    @staticmethod
    def get_all_beats(board, c):
        res = []
        for x in range(len(board[0])):
            for y in range(len(board)):
                f = board[y][x]
                if f * c <= 0:
                    continue
                if abs(f) == 6:
                    res += ChessSteper.king_beats(x, y)
                elif abs(f) == 1:
                    res += [tuple([x + 1, y + c]), tuple([x - 1, y + c])]
                else:
                    res += ChessSteper.get_func(board, x, y)(board, x, y, c * -1)
        return res


if __name__ == "__main__":
    engine = ChessGameEngine()
    engine.make_turn((5, 6), (5, 5))
    engine.make_turn((2, 0), (7, 4))
    print(*engine.get_state(), sep="\n")
    print(engine.is_game_over())