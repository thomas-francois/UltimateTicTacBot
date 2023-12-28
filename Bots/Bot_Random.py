from random import choice


class Bot_Random(object):

    def __init__(self, *args, **kwargs):
        self.name = "Random"

    def start(self, game, ID):
        self.game = game
        self.ID = ID

    def play(self):
        possibleMoves = self.game.getLegalMoves(self.game.state)
        self.game.playMove(self, choice(possibleMoves))
