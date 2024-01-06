from Bots.Node import Node
import Utils


class Bot_Minimax(object):

	def __init__(self, depth = 3):
		self.name = "Minimax d=" + str(depth)
		self.depth = depth

	def start(self, game, ID):
		self.game = game
		self.ID = ID

	def play(self):
		root = self.createTree()
		result = self.searchTree(root)

		bestMove = result["node"].getLineage()[1]
		self.game.playMove(self, bestMove)

	def createTree(self):
		# Create the root node with the current game state
		root = Node(-1, self.game.state)
		currentNode = Node.getValidNode(self.depth)

		# While there is nodes not explored below the depth
		while currentNode is not None:

			# Get all legal moves from the current state
			moves = self.game.getLegalMoves(currentNode.state)

			# Create one children for each possible moves
			for move in moves:

				# Copy the parent state and change it with the new move
				newState = Utils.copyState(currentNode.state)

				newState["board"][move] = newState["player"]
				newState["player"] = 1 - newState["player"]

				# Get the square of the next move
				possibleSquares = self.game.getNewSquare(currentNode.state, move)

				# If multiple next squares create a child for each of them
				if isinstance(possibleSquares, list):
					for square in possibleSquares:
						newState["square"] = square
						currentNode.insertChild(Node(move, newState, currentNode))

				# Else create one child with the next square
				else:
					newState["square"] = possibleSquares
					currentNode.insertChild(Node(move, newState, currentNode))

			currentNode = Node.getValidNode(self.depth)

		return root

	def searchTree(self, root):
		# Minimax search

		results = []
		for node in root.children:
			result = self.minimax(node, alpha=float('-inf'), beta=float('inf'))
			results.append({"node": node, "score": result["score"]})

		bestMove = max(results, key=lambda x: x["score"])

		return bestMove

	def minimax(self, node, alpha, beta):
		if not node.children:
			return {"node": node, "score": self.evaluateBoard(node.state)}

		if node.state["player"] == self.ID:
			max_value = float('-inf')
			best_move = node
			for child in node.children:
				evaluation = self.minimax(child, alpha, beta)
				if evaluation["score"] > max_value:
					max_value = evaluation["score"]
					best_move = child
				alpha = max(alpha, evaluation["score"])
				if beta <= alpha:
					break
			return {"node": best_move, "score": max_value}
		else:
			min_value = float('inf')
			best_move = node
			for child in node.children:
				evaluation = self.minimax(child, alpha, beta)
				if evaluation["score"] < min_value:
					min_value = evaluation["score"]
					best_move = child
				beta = min(beta, evaluation["score"])
				if beta <= alpha:
					break
			return {"node": best_move, "score": min_value}

	def evaluateBoard(self, state):
		score = 0

		for sequence in [state["board"][i: i + 9] for i in range(0 ,81 ,9)]:

			for line in Utils.linesOpti:

				test = [sequence[i] for i in line]
				testSet = set(test)
				if testSet == {self.ID}:
					score += 10
				elif testSet == {1 - self.ID}:
					score -= 10

				if -1 in test and test.count(self.ID) == 2:
					score += 2
				elif -1 in test and test.count(1 - self.ID) == 2:
					score -= 2

			if sequence[4] == self.ID:
				score += 1
			elif sequence[4] == 1 - self.ID:
				score -= 1

		return score
