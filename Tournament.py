from random import choice
from Bot_Random import Bot_Random
from Bot_V1 import Bot_V1
from Bot_V2 import Bot_V2
from Bot_First import Bot_First
import multiprocessing


class Game(object):

	lines = [
		{"type": "horizontal", "index": 0, 'offsets': [0, 1, 2]},
		{"type": "horizontal", "index": 1, 'offsets': [3, 4, 5]},
		{"type": "horizontal", "index": 2, 'offsets': [6, 7, 8]},
		{"type": "vertical", "index": 0, 'offsets': [0, 3, 6]},
		{"type": "vertical", "index": 1, 'offsets': [1, 4, 7]},
		{"type": "vertical", "index": 2, 'offsets': [2, 5, 8]},
		{"type": "diagonal", "index": 0, 'offsets': [0, 4, 8]},
		{"type": "diagonal", "index": 1, 'offsets': [2, 4, 6]},
	]

	def __init__(self, playerA, playerB, *, windowSize = 800 ,state = None):
		self.players = [playerA, playerB]
		self.isStarted = False

		if state is None:
			self.board = [-1] * 81
			self.player = 0
			self.currentSquare = 4
		else:
			self.board = state["board"]
			self.player = state["player"]
			self.currentSquare = state["square"]

		self.updateScore()

	def start(self):
		self.players[0].start(self, 0)
		self.players[1].start(self, 1)

		self.isStarted = True
		while self.isStarted:
			result = self.players[self.player].play()
			if result != "valid":
				continue
			self.player = (self.player + 1) % 2

		self.updateScore()
		return self.score


	def updateScore(self):
		self.score = {"A": 0, "B": 0}
		for sequence in [self.board[i: i + 9] for i in range(0 ,81 ,9)]:
			for line in Game.lines:
				if [sequence[i] for i in line['offsets']] == [0] * 3:
					self.score['A'] += 1
				elif [sequence[i] for i in line['offsets']] == [1] * 3:
					self.score['B'] += 1


	def __endGame(self):
		self.isStarted = False


	def playMove(self, player, move):
		if player == self.player and move in self.getLegalMoves():
			self.board[move] = player

			# If board is full, end the game
			if -1 not in self.board:
				self.__endGame()
				return "end"

			newSquare = self.getNewSquare(move)
			if isinstance(newSquare, list):
				self.currentSquare = choice(newSquare)
			else:
				self.currentSquare = newSquare

			self.updateScore()
			return "valid"

		else:
			return "invalid"
			# raise Exception(f"Move cannot be played: {player} {self.player} and {move} in {self.getLegalMoves()} ({self.currentSquare})\n{self.board}")

	def getLegalMoves(self, state = None ,* ,square = None):
		board = state["board"] if state is not None else self.board
		if square is None:
			square = state["square"] if state is not None else self.currentSquare

		return [i for i in range(81) if board[i] == -1 and i // 9 == square]

	def getNewSquare(self, move, state = None):
		if not state:
			state = self.getState()

		targetSquare = move % 9

		# If target square is not full, it becomes the new current square
		if self.getLegalMoves(state, square = targetSquare) != []:
			return targetSquare

		# If target square is full and the current square is not full, it remains the same
		elif self.getLegalMoves(state, square = state["square"]) != []:
			return state["square"]

		# Else choose a random not full square:
		else:
			possibleSquares = []
			for i in range(9):
				if self.getLegalMoves(state, square = i) != []:
					possibleSquares.append(i)

			return possibleSquares

	def getCurrentScore(self, player = None):
		if player is None:
			return self.score
		return self.score[player]

	def getState(self):
		return {"board": self.board, "player": self.player, "square": self.currentSquare}


class Tournament(object):
	"""docstring for Tournament"""
	def __init__(self, playerA, playerB, rounds):
		self.playerA = playerA
		self.playerB = playerB
		self.rounds = rounds
		self.start()


	# def start(self):
	# 	score = {"A": 0, "B": 0}
	# 	win = {"A": 0, "B": 0}
	# 	for i in range(self.rounds):
	# 		if i % 2 == 0:
	# 			game = Game(self.playerA, self.playerB)
	# 			newScore = game.start()
	# 		else:
	# 			game = Game(self.playerB, self.playerA)
	# 			newScore = game.start()
	# 			newScore["A"], newScore["B"] = newScore["B"], newScore["A"]
	# 		score["A"] += newScore["A"] / self.rounds
	# 		score["B"] += newScore["B"] / self.rounds
	# 		if newScore["A"] > newScore["B"]:
	# 			win["A"] += 1
	# 		elif newScore["A"] < newScore["B"]:
	# 			win["B"] += 1

	# 	print(f"{self.playerA.name} ({round(score['A'], 2)}) > {win['A']} : {self.rounds - win['A'] - win['B']} : {win['B']} < {self.playerB.name} ({round(score['B'], 2)})")


	def batchWorker(self, result_queue, order):
		if order % 2 == 0:
			game = Game(self.playerA, self.playerB)
			newScore = game.start()
		else:
			game = Game(self.playerB, self.playerA)
			newScore = game.start()
			newScore["A"], newScore["B"] = newScore["B"], newScore["A"]
		result_queue.put(newScore)

	def start(self):
		score = {"A": 0, "B": 0}
		win = {"A": 0, "B": 0}
		processes = []

		result_queue = multiprocessing.Queue()

		for i in range(self.rounds):
			process = multiprocessing.Process(target=self.batchWorker, args=(result_queue, i))
			processes.append(process)
			process.start()

		for process in processes:
			process.join()

		while not result_queue.empty():
			newScore = result_queue.get()
			score["A"] += newScore["A"] / self.rounds
			score["B"] += newScore["B"] / self.rounds
			if newScore["A"] > newScore["B"]:
				win["A"] += 1
			elif newScore["A"] < newScore["B"]:
				win["B"] += 1

		print(
			f"{self.playerA.name} ({round(score['A'], 2)}) > {win['A']} : {self.rounds - win['A'] - win['B']} : {win['B']} < {self.playerB.name} ({round(score['B'], 2)})"
		)


if __name__ == '__main__':
	Tournament(Bot_V2(), Bot_V1(), 100)

# Random 42 - 38  Random
# V1 	 45 - 38  Random
# V2     62 - 21  Random
# V1     16 - 50  V2
