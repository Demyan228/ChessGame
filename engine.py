from typing import List


class ChessGameEngine:
    def __init__(self):
        pass

    def is_game_over(self) -> bool:
        pass

    def get_state(self) -> List[List[int]]:
        pass

    def get_places(self, pos: List[int, int]) -> List[List[int, int]]:
        pass

    def make_turn(self, pos1: List[int, int], pos2: List[int, int]) -> None:
        pass