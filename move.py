def play_move(fen, move):
    # updates a fen given a move (wikipedia notations)
    hwalls, vwalls, player_positions, available_walls, active_player = fen.split(" / ")
    active_player = int(active_player)
    p1, p2 = player_positions.split(" ")
    # number of walls available for each player
    w1, w2 = [int(w) for w in available_walls.split(" ")]

    if len(move) == 3:  # wall move
        if move[-1] == "h":
            hwalls = f"{hwalls} {move[:2]}"
        elif move[-1] == "v":
            vwalls = f"{vwalls} {move[:2]}"
        
        if active_player == 1:
            w1 -= 1
        else:
            w2 -= 1
    else:  # player move
        if active_player == 1:
            p1 = move
        else:
            p2 = move

    active_player = 1 + active_player % 2
    fen = f"{hwalls} / {vwalls} / {p1} {p2} / {w1} {w2} / {active_player}"

    return fen
