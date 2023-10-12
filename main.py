from state import State
from utils import play_move


if __name__ == "__main__":
    fen="d4f4e7 / a2a8 / e4 e6 / 7 8 / 2"
    state = State(fen=fen)
    print(state)
    print(fen)

    while True:
        legal_actions = [str(a) for a in state.compute_legal_actions()]
        print("Legal moves:", " ".join(legal_actions))
        move = input("Move ? ")
        while not (move in legal_actions):
            move = input("Illegal move. Command was ignored.\nMove ? ")
        fen = play_move(fen, move)
        state = State(fen=fen)
        print(state)
        print(fen)
