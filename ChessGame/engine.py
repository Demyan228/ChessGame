from ChessGame.chess_typing import Position, State
from typing import Tuple
from ChessGame.chess_steper import ChessSteper, is_valid
from copy import deepcopy



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
        if not is_valid(*pos1) and self.board[pos1[1]][pos1[0]] == 0:
            raise ValueError(f"вы передали pos1: {pos1}, это не верно езначение")
        if not is_valid(*pos2):
            raise ValueError(f"вы передали pos2: {pos2}, это не верно езначение")
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
        if not is_valid(*pos):
            raise ValueError(f"вы передали pos: {pos}, это за пределами")
        if self.board[pos[1]][pos[0]] == 0:
            raise ValueError(f"вы передали pos: {pos}, это пустая клетка, ухади")
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




if __name__ == "__main__":
    engine = ChessGameEngine()
    engine.make_turn((5, 6), (5, 5))
    engine.make_turn((2, 0), (7, 4))
    print(*engine.get_state(), sep="\n")
    print(engine.is_game_over())