from board import Board
from move import play_move

if __name__ == "__main__":
    board = Board()
    print(board)

    move="e2"
    print(move[0])
    print(move[-1])

    fen="d4f4e7 / a2a8 / e4 e6 / 7 8 / 2"
    print(play_move(fen, "e2"))
    
    board = Board(fen=fen)
    print(board)
    while True:
        move = input("Move ?")
        fen = play_move(fen, move)
        board = Board(fen=fen)
        print(board)
        print(fen)



