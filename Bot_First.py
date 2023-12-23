from random import choice


class Bot_First(object):

    def __init__(self):
        self.name = "First"

    def start(self, game, player_id):
        self.game = game
        self.player_id = player_id

    def play(self):
        possibleMoves = self.game.getLegalMoves()
        return self.game.playMove(self.player_id, possibleMoves[0])
