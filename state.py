import numpy as np
from itertools import zip_longest
from string import ascii_lowercase
from utils import not2pos


EMPTY_CELL = 0
PLAYER_1 = 1
PLAYER_2 = 2


class State():
    def __init__(self, board_size=9, fen=" /  / e1 e9 / 10 10 / 1") -> None:
        self.board_size = board_size
        self.vwalls = np.full((self.board_size - 1, self.board_size), False)
        self.hwalls = np.full((self.board_size, self.board_size - 1), False)

        hwalls, vwalls, pawn_positions, fences_left, active_player = fen.split(
            " / ")

        self._place_walls(hwalls, "h")
        self._place_walls(vwalls, "v")
        self.pawn_positions = [not2pos(p) for p in pawn_positions.split(" ")]
        self.active_player = int(active_player)
        self.fences_left = [int(w) for w in fences_left.split(" ")]

    def _place_walls(self, walls, orient="h"):
        # retrieves the list wall move coordinates
        # a wall move is denoted by the closest square to a1
        wall_moves = [walls[i: i + 2] for i in range(0, len(walls), 2)]

        for wall_move in wall_moves:
            row, col = not2pos(wall_move)

            if orient == "h":
                self.hwalls[col, row] = True
                self.hwalls[col + 1, row] = True
            else:  # otherwise orient == "v"
                self.vwalls[col, row] = True
                self.vwalls[col, row + 1] = True

    def __repr__(self) -> str:
        mapping_cells = {EMPTY_CELL: "   ", PLAYER_1: " X ", PLAYER_2: " 0 "}
        mapping_vwalls = {True: "#", False: "|"}
        mapping_hwalls = {True: "###", False: "―――"}
        WALL_INTERSECTION = 'o'
        board_repr = ""

        cells = np.full((self.board_size, self.board_size), EMPTY_CELL)
        for player_idx, (row, col) in enumerate(self.pawn_positions):
            cells[col, row] = player_idx + 1

        def _pick_items_alternatively(lst1, lst2):
            return "".join(
                i for pair in zip_longest(lst1, lst2, fillvalue=None)
                for i in pair if i is not None
            )

        for row_idx in range(self.board_size):
            cells_vwalls = _pick_items_alternatively(
                [mapping_cells[c] for c in cells[:, row_idx]],
                [mapping_vwalls[w] for w in self.vwalls[:, row_idx]]
            )

            if row_idx == (self.board_size // 2):
                info = f"ACTIVE PLAYER: {mapping_cells[self.active_player]}"
            elif row_idx == (self.board_size - 1):
                info = f"PLAYER 2: {self.fences_left[1]} WALLS"
            elif row_idx == 0:
                info = f"PLAYER 1: {self.fences_left[0]} WALLS"
            else:
                info = ""

            board_repr = f"\n{row_idx + 1} {cells_vwalls}    {info}{board_repr}"

            if row_idx == (self.board_size - 1):
                continue

            hwalls = _pick_items_alternatively(
                [mapping_hwalls[w] for w in self.hwalls[:, row_idx]],
                (self.board_size - 1) * [WALL_INTERSECTION]
            )
            board_repr = f"\n  {hwalls}{board_repr}"

        letters = " ".join(
            [f" {ascii_lowercase[i]} " for i in range(self.board_size)]
        )
        board_repr += f"\n  {letters}"

        return board_repr
