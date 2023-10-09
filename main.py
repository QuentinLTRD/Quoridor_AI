from state import State
from utils import play_move


if __name__ == "__main__":
    fen="d4f4e7 / a2a8 / e4 e6 / 7 8 / 2"
    state = State(fen=fen)
    print(state)
    
    while True:
        move = input("Move ?")
        fen = play_move(fen, move)
        state = State(fen=fen)
        print(state)
        print(fen)
