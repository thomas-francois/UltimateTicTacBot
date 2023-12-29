from Bots.Node import Node
import Utils


class Bot_Negamax_Opti(object):

	def __init__(self, depth=3):
		self.name = "NegamaxOpti d=" + str(depth)
		self.depth = depth

	def start(self, game, ID):
		self.game = game
		self.ID = ID

	def play(self):
		# print("start Move")
		root = Node(-1, self.game.state)

		# self.searches = 0

		searchResult = self.negamax(root, self.depth, alpha=float('-inf'), beta=float('inf'))
		bestMove = searchResult["node"].getLineage()[1]

		# print("Not OPTI", self.searches)

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
						# print("Inserted from depth (random square)", possibleSquares, currentNode.depth)

				# Else create one child with the next square
				else:
					newState["square"] = possibleSquares
					currentNode.insertChild(Node(move, newState, currentNode))
					# print("Inserted from depth ", currentNode.depth, possibleSquares)

			currentNode = Node.getValidNode(self.depth)

		# Utils.printDebugTree(root)
		return root


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
		# self.searches += 1

		for sequence in [state["board"][i: i + 9] for i in range(0, 81, 9)]:

			for line in Utils.linesOpti:

				test = [sequence[i] for i in line]
				testSet = set(test)
				if testSet == {state["player"]}:
					score += 10
				elif testSet == {1 - state["player"]}:
					score -= 10

				if -1 in test and test.count(state["player"]) == 2:
					score += 2
				elif -1 in test and test.count(1 - state["player"]) == 2:
					score -= 2

			if sequence[4] == state["player"]:
				score += 1
			elif sequence[4] == 1 - state["player"]:
				score -= 1

		return score
