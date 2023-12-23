from random import choice


class Bot_Random(object):

    def __init__(self):
        self.name = "Random"

    def start(self, game, player_id):
        self.game = game
        self.player_id = player_id

    def play(self):
        possibleMoves = self.game.getLegalMoves()
        return self.game.playMove(self.player_id, choice(possibleMoves))
