def play_move(fen, move):
    # updates a fen given a move (wikipedia notations)
    hwalls, vwalls, player_positions, available_walls, ply  = fen.split(" / ")
    if move[-1] == "h":
        fen = f"{hwalls}{move[:2]} / {vwalls} / {player_positions} / {available_walls} / {ply}"

    elif move[-1] == "v":
        fen = f"{hwalls} / {vwalls}{move[:2]} / {player_positions} / {available_walls} / {ply}"
    
    else:
        p1, p2 = player_positions.split(" ")
        if ply == 1:
            fen = f"{hwalls} / {vwalls} / {move} {p2} / {available_walls} / {(int(ply) + 1)}"
        
        else:
            fen = f"{hwalls} / {vwalls} / {p1} {move} / {available_walls} / {(int(ply) - 1)}"
    
    return fen


