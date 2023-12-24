from random import choice
import Bot
import Utils
from Player import Player
from GameDisplay import GameDisplay


class GameEngine(object):

	def __init__(self, playerA, playerB, * ,state = None, display = False):
		self.__players = [playerA, playerB]
		self.display = display

		if state is None:
			self.state = {"board": [-1] * 81, "player": 0, "square": 4}
		else:
			self.state = state


	def start(self):
		if self.display:
			self.display = GameDisplay(self.__players, state = self.state)

		self.__players[0].start(self, 0)
		self.__players[1].start(self, 1)


		self.isStarted = True
		while self.isStarted:
			self.player.play()

		if self.display:
			self.display.fenetre.mainloop()

		return Utils.calculteScore(self.state, [p.name for p in self.__players])



	def playMove(self, player, move):
		if player == self.player and move in self.getLegalMoves(self.state):
			self.board[move] = player.ID

			# If board is full, end the game
			if -1 not in self.board:
				self.isStarted = False
				if self.display:
					self.display.update(self.state)
				return

			newSquare = self.getNewSquare(self.state, move)
			if isinstance(newSquare, list):
				self.square = choice(newSquare)
			else:
				self.square = newSquare

			self.player = (self.player.ID + 1) % 2

			if self.display:
				self.display.update(self.state)


	def getLegalMoves(self, state, targetSquare = None):
		board = state["board"]
		square = state["square"] if targetSquare is None else targetSquare

		return [i for i in range(81) if board[i] == -1 and i // 9 == square]


	def getNewSquare(self, state, move):
		targetSquare = move % 9

		# If target square is not full, it becomes the new current square
		if self.getLegalMoves(state, targetSquare = targetSquare) != []:
			return targetSquare

		# If target square is full and the current square is not full, it remains the same
		elif self.getLegalMoves(state, targetSquare = state["square"]) != []:
			return state["square"]

		# Else choose a random not full square:
		else:
			possibleSquares = []
			for i in range(9):
				if self.getLegalMoves(state, targetSquare = i) != []:
					possibleSquares.append(i)

			return possibleSquares


	@property
	def board(self):
		return self.state["board"]

	@property
	def player(self):
		return self.__players[self.state["player"]]

	@player.setter
	def player(self, value):
		self.state["player"] = value

	@property
	def square(self):
		return self.state["square"]

	@square.setter
	def square(self, value):
		self.state["square"] = value


if __name__ == '__main__':
	game = GameEngine(Bot.Random(), Bot.V3(depth = 3), display = True)
	print(game.start())
