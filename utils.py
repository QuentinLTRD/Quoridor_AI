from string import ascii_lowercase


def not2pos(pos_notation):
    # gets pos indices from pos notation (ex: a1 -> 0, 0; d2 -> 1, 3)
    col = ord(pos_notation[0]) - 97  # convert lowercase to index
    row = int(pos_notation[1]) - 1  # rows index number is 1
    return row, col


def pos2not(pos):
    # get pos notation from pos indices (ex: (0, 0) -> a1 ; (1, 3) -> d2)
    pos_row = int(pos[0]) + 1
    pos_col = ascii_lowercase[pos[1]]
    return f"{pos_col}{pos_row}"


def play_move(fen, move):
    # updates a fen given a move (wikipedia notations)
    hwalls, vwalls, pawn_positions, fences_left, active_player = fen.split(
        " / ")

    active_player = int(active_player)
    pawn_positions = [p for p in pawn_positions.split(" ")]
    fences_left = [int(w) for w in fences_left.split(" ")]

    if len(move) == 3:  # wall move
        if move[-1] == "h":
            hwalls += move[:2]
        elif move[-1] == "v":
            vwalls += move[:2]

        fences_left[active_player - 1] -= 1

    else:  # player move
        pawn_positions[active_player - 1] = move

    active_player = 1 + active_player % 2
    pawn_positions = " ".join(pawn_positions)
    fences_left = " ".join([str(w) for w in fences_left])
    fen = f"{hwalls} / {vwalls} / {pawn_positions} / {fences_left} / {active_player}"

    return fen
