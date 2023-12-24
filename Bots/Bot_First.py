from random import choice


class Bot_First(object):

    def __init__(self):
        self.name = "First"

    def start(self, game, ID):
        self.game = game
        self.ID = ID

    def play(self):
        possibleMoves = self.game.getLegalMoves(self.game.state)
        self.game.playMove(self, possibleMoves[0])
