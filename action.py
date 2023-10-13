from utils import pos2not


class Action():
    pass


class MovePawn(Action):
    def __init__(self, start_pos, end_pos) -> None:
        super().__init__()
        self.start_pos = start_pos
        self.end_pos = end_pos
    
    def __repr__(self) -> str:
        return pos2not(self.end_pos)


class PlaceWall(Action):
    def __init__(self, start_pos, is_horizontal) -> None:
        super().__init__()
        self.start_pos = start_pos
        self.is_horizontal = is_horizontal
    
    def __repr__(self) -> str:
        suffix = "h" if self.is_horizontal else "v"
        return f"{pos2not(self.start_pos)}{suffix}"
