import numpy as np
from constants import BOARD_SIZE
from constants import EMPTY_CELL, PLAYER_1, PLAYER_2
from constants import LEFT, RIGHT, DOWN, UP
from itertools import zip_longest, chain
from string import ascii_lowercase
from utils import not2pos, is_within_bounds
from action import MovePawn


class State():
    def __init__(self, fen=" /  / e1 e9 / 10 10 / 1") -> None:
        BOARD_SIZE = 9
        self.vwalls = np.full((BOARD_SIZE - 1, BOARD_SIZE), False)
        self.hwalls = np.full((BOARD_SIZE, BOARD_SIZE - 1), False)

        hwalls, vwalls, pawn_positions, fences_left, active_player = fen.split(
            " / ")

        self._place_walls(hwalls, "h")
        self._place_walls(vwalls, "v")
        self.pawn_positions = [not2pos(p) for p in pawn_positions.split(" ")]
        self.fences_left = [int(w) for w in fences_left.split(" ")]
        self.idx_player = int(active_player) - 1

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

        cells = np.full((BOARD_SIZE, BOARD_SIZE), EMPTY_CELL)
        for player_idx, (row, col) in enumerate(self.pawn_positions):
            cells[col, row] = player_idx + 1

        def _pick_items_alternatively(lst1, lst2):
            return "".join(
                i for pair in zip_longest(lst1, lst2, fillvalue=None)
                for i in pair if i is not None
            )

        for row_idx in range(BOARD_SIZE):
            cells_vwalls = _pick_items_alternatively(
                [mapping_cells[c] for c in cells[:, row_idx]],
                [mapping_vwalls[w] for w in self.vwalls[:, row_idx]]
            )

            if row_idx == (BOARD_SIZE // 2):
                info = f"ACTIVE PLAYER: {mapping_cells[self.idx_player + 1]}"
            elif row_idx == (BOARD_SIZE - 1):
                info = f"PLAYER 2: {self.fences_left[1]} WALLS"
            elif row_idx == 0:
                info = f"PLAYER 1: {self.fences_left[0]} WALLS"
            else:
                info = ""

            board_repr = f"\n{row_idx + 1} {cells_vwalls}    {info}{board_repr}"

            if row_idx == (BOARD_SIZE - 1):
                continue

            hwalls = _pick_items_alternatively(
                [mapping_hwalls[w] for w in self.hwalls[:, row_idx]],
                (BOARD_SIZE - 1) * [WALL_INTERSECTION]
            )
            board_repr = f"\n  {hwalls}{board_repr}"

        letters = " ".join(
            [f" {ascii_lowercase[i]} " for i in range(BOARD_SIZE)]
        )
        board_repr += f"\n  {letters}"

        return board_repr

    def has_wall_collision(self, start, delta):
        mapping_delta_offset = {
            LEFT: (0, -1), RIGHT: (0, 0), DOWN: (-1, 0), UP: (0, 0)
        }

        row, col = start
        wall = self.vwalls if delta in [LEFT, RIGHT] else self.hwalls
        offset = mapping_delta_offset[delta]

        return wall[col + offset[1], row + offset[0]]

    def _compute_legal_pawn_moves(self):
        deltas = [LEFT, RIGHT, DOWN, UP]
        mapping_delta_adjacent_delta = {
            LEFT: [DOWN, UP],
            UP: [LEFT, RIGHT],
            RIGHT: [UP, DOWN],
            DOWN: [RIGHT, LEFT]
        }

        player_pos = self.pawn_positions[self.idx_player]
        opponent_pos = self.pawn_positions[(self.idx_player + 1) % 2]

        legal_pawn_moves = []

        for delta in deltas:
            drow, dcol = delta
            dest = (player_pos[0] + drow, player_pos[1] + dcol)

            if not is_within_bounds(dest):
                continue

            if self.has_wall_collision(player_pos, delta):
                continue

            if (dest != opponent_pos):
                # move pawn on adjacent cell
                legal_pawn_moves.append(MovePawn(player_pos, dest))

            if (dest == opponent_pos):
                new_dest = (dest[0] + drow, dest[1] + dcol)

                valid_jump_over_move = (
                    is_within_bounds(new_dest) and
                    not self.has_wall_collision(dest, delta)
                )

                # jump over opponent pawn
                if valid_jump_over_move:
                    legal_pawn_moves.append(MovePawn(player_pos, new_dest))

                # jump next to opponent pawn
                else:
                    for delta2 in mapping_delta_adjacent_delta[delta]:
                        drow2, dcol2 = delta2
                        new_dest = (dest[0] + drow2, dest[1] + dcol2)

                        valid_adjacent_to_opponent_move = (
                            is_within_bounds(new_dest) and
                            not self.has_wall_collision(dest, delta2)
                        )

                        if valid_adjacent_to_opponent_move:
                            legal_pawn_moves.append(
                                MovePawn(player_pos, new_dest))

        return legal_pawn_moves

    def compute_legal_actions(self):

        return list(
            chain(
                self._compute_legal_pawn_moves()
            )
        )
