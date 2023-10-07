import numpy as np
from itertools import zip_longest
from string import ascii_lowercase

EMPTY_CELL = 0
PLAYER_1 = 1
PLAYER_2 = 2

class Board():
    def __init__(self, board_size=9, fen=" /  / e1 e9 / 10 10 / 1") -> None:
        self.board_size = board_size
        self.cells = np.full((self.board_size, self.board_size), EMPTY_CELL)
        self.vwalls = np.full((self.board_size - 1, self.board_size), False)
        self.hwalls = np.full((self.board_size, self.board_size - 1), False)
        self.ply = 1
        self.available_walls = np.array((10, 10))
        self._load_fen(fen)


    def __repr__(self) -> str:
        mapping_cells = {EMPTY_CELL: "   ", PLAYER_1: " X ", PLAYER_2: " 0 "}
        mapping_vwalls = {True: "#", False: "|"}
        mapping_hwalls = {True: "###", False: "―――"}
        WALL_INTERSECTION = 'o'
        board_repr = ""

        def _pick_items_alternatively(lst1, lst2):
            return "".join(
                i for pair in zip_longest(lst1, lst2, fillvalue=None)
                for i in pair if i is not None
            )
        
        for row_idx in range(self.board_size):
            cells_vwalls = _pick_items_alternatively(
                [mapping_cells[c] for c in self.cells[:, row_idx]],
                [mapping_vwalls[w] for w in self.vwalls[:, row_idx]]
            )

            if row_idx == (self.board_size // 2):
                info = f"ACTIVE PLAYER: {mapping_cells[self.active_player]}"
            elif row_idx == (self.board_size - 1):
                info = f"PLAYER 2: {self.available_walls[1]} WALLS"
            elif row_idx == 0:
                info = f"PLAYER 1: {self.available_walls[0]} WALLS"
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

    
    def _load_fen(self, fen):
        # walls available and ply are not taken into account when loading board
        hwalls, vwalls, player_positions, available_walls, ply  = fen.split(" / ")

        def not2pos(pos_notation):
            # gets pos indexes from pos notation (ex: a1 -> 0, 0; d2 : 1, 3)
            col = ord(pos_notation[0]) - 97  # convert lowercase to index
            row = int(pos_notation[1]) - 1  # rows index number is 1
            return row, col
        
        # init player positions
        p1, p2 = player_positions.split(" ")
        row1, col1 = not2pos(p1)
        row2, col2 = not2pos(p2)

        self.cells[col1, row1] = PLAYER_1
        self.cells[col2, row2] = PLAYER_2

        # init walls
        def _place_walls(walls, orient="h"):
            # retrieves the list wall move coordinates
            # a wall move is denoted by the closest square to a1
            wall_moves = [walls[i: i+2] for i in range(0, len(walls), 2)]

            for wall_move in wall_moves:
                row, col = not2pos(wall_move)

                if orient == "h":
                    self.hwalls[col, row] = True
                    self.hwalls[col+1, row] = True
                else:  # otherwise orient == "v"
                    self.vwalls[col, row] = True
                    self.vwalls[col, row + 1] = True
                    

        _place_walls(hwalls, "h")
        _place_walls(vwalls, "v")

        # TO DO: fix it :)
        # define active_player2ply(): (optionaly ply2active_player)
        # ply != active player
        def _set_ply(ply):
            # must be casted to int
            self.ply = ply

        _set_ply(ply)
        
        # TO DO: change this when updated above
        self.active_player = int(ply)

        def _set_available_walls(available_walls):
            p1_available_walls, p2_available_walls = available_walls.split(" ")
            self.available_walls = np.array((p1_available_walls, p2_available_walls))

        _set_available_walls(available_walls)
