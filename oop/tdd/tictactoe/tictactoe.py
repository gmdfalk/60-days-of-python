class Board(object):

    def __init__(self):

        self.pawns = {0: "X", 1: "O"}
        self.player = self.pawns[0]
        self.npc = self.pawns[1]

if __name__ == "__main__":
    b = Board()
    print b.pawns, b.player, b.npc
