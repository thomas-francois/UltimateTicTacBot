import Bot
import multiprocessing
from GameEngine import GameEngine


class Tournament(object):

	def __init__(self, playerA, playerB, rounds, threading = False):
		self.playerA = playerA
		self.playerB = playerB
		self.rounds = rounds

		if not threading:
			self.start()
		else:
			self.startBatch()

	def start(self):
		A, B = self.playerA.name, self.playerB.name
		score = {A: 0, B: 0}
		win = {A: 0, B: 0}

		for i in range(self.rounds):
			if i % 2 == 0:
				game = GameEngine(self.playerA, self.playerB)
			else:
				game = GameEngine(self.playerB, self.playerA)
			newScore = game.start()

			score[A] = round(score[A] + newScore[A] / self.rounds, 1)
			score[B] = round(score[B] + newScore[B] / self.rounds, 1)

			if newScore[A] > newScore[B]:
				win[A] += 1
			elif newScore[A] < newScore[B]:
				win[B] += 1

		print(f"{A} ({score[A]}) > {win[A]} : {self.rounds - sum(win.values())} : {win[B]} < {B} ({score[B]})")


	def startBatch(self):
		A, B = self.playerA.name, self.playerB.name
		score = {A: 0, B: 0}
		win = {A: 0, B: 0}
		processes = []

		result_queue = multiprocessing.Queue()

		for i in range(self.rounds):
			process = multiprocessing.Process(target=self.individualGame, args=(result_queue, i, [A, B]))
			processes.append(process)
			process.start()

		for process in processes:
			process.join()

		while not result_queue.empty():
			newScore = result_queue.get()
			score[A] = round(score[A] + newScore[A] / self.rounds, 1)
			score[B] = round(score[B] + newScore[B] / self.rounds, 1)
			if newScore[A] > newScore[B]:
				win[A] += 1
			elif newScore[A] < newScore[B]:
				win[B] += 1

		print(f"{A} ({score[A]}) > {win[A]} : {self.rounds - sum(win.values())} : {win[B]} < {B} ({score[B]})")

	def individualGame(self, result_queue, order, names):
		if order % 2 == 0:
			game = GameEngine(self.playerA, self.playerB)
		else:
			game = GameEngine(self.playerB, self.playerA)

		score = game.start()
		result_queue.put(score)



if __name__ == '__main__':
	Tournament(Bot.Negamax(depth = 3), Bot.V5(depth = 3), 50, threading = True)

# VS Random (100 iterations):

# V5 d=3: 		100 -> 16.1
# Negamax d=3:	100 -> 11.5s

# V5 d=4:		50 -> 33.9s
# Negamax d=4:	50 -> 15.4s
