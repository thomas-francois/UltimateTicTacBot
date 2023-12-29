from Bots.Node import Node
import Utils
from functools import cache


class Bot_Negamax_Opti(object):

	def __init__(self, depth=3):
		self.name = "NegamaxOpti d=" + str(depth)
		self.depth = depth

	def start(self, game, ID):
		self.game = game
		self.ID = ID

	def play(self):
		# print("start Move")
		# self.searches = 0

		root = Node(-1, self.game.state)
		searchResult = self.negamax(root, self.depth, alpha=float('-inf'), beta=float('inf'))
		bestMove = searchResult["node"].getLineage()[1]

		# print(self.searches)
		self.game.playMove(self, bestMove)


	def createChildren(self, node):
		moves = self.game.getLegalMoves(node.state)

		# Create one children for each possible moves
		for move in moves:

			# Copy the parent state and change it with the new move
			newState = Utils.copyState(node.state)

			newState["board"][move] = newState["player"]
			newState["player"] = 1 - newState["player"]

			# Get the square of the next move
			possibleSquares = self.game.getNewSquare(node.state, move)

			# If multiple next squares create a child for each of them
			if isinstance(possibleSquares, list):
				for square in possibleSquares:
					newState["square"] = square
					node.insertChild(Node(move, newState, node))

			# Else create one child with the next square
			else:
				newState["square"] = possibleSquares
				node.insertChild(Node(move, newState, node))

	def negamax(self, node, depth, alpha, beta):
		if depth > 0:
			self.createChildren(node)

		if depth == 0 or not node.children:
			return {"node": node, "score": self.evaluateBoard(node.state)}

		max_value = float('-inf')
		best_move = node
		for child in node.children:
			evaluation = self.negamax(child, depth - 1, -beta, -alpha)
			if -evaluation["score"] > max_value:
				max_value = -evaluation["score"]
				best_move = evaluation["node"]
			alpha = max(alpha, -evaluation["score"])
			if beta <= alpha:
				break

		return {"node": best_move, "score": max_value}

	def evaluateBoard(self, state):
		score = 0
		player = state["player"]
		oponent = 1 - player
		# self.searches += 1

		for square in [state["board"][i: i + 9] for i in range(0, 81, 9)]:

			for lineMask in Utils.linesOpti:

				line = [square[j] for j in lineMask]

				if -1 in line:
					if line.count(player) == 2:
						score += 2
					elif line.count(oponent) == 2:
						score -= 2
				else:
					if oponent not in line:
						score += 10
					elif player not in line:
						score -= 10

			if square[4] == player:
				score += 1
			elif square[4] == oponent:
				score -= 1

		return score
