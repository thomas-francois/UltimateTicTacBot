from Node import Node
import copy


class Bot_V1(object):

	def __init__(self, depth = 3):
		self.name = "V1"
		self.depth = depth

	def start(self, game, player_id):
		self.game = game
		self.player_id = player_id

	def play(self):
		# print("start Move")
		root = self.createTree()
		result = self.searchTree(root)

		bestMove = result["node"].getLineage()[1]
		# print(f"\nBest move: {bestMove} (score: {result['score']})")
		# exit()

		return self.game.playMove(self.player_id, bestMove)

	def createTree(self):
		# Create the root node with the current game state
		root = Node(-1, self.game.getState())
		currentNode = Node.getValidNode(self.depth)

		# While there is nodes not explored below the depth
		while currentNode is not None:

			# Get all legal moves from the current state
			moves = self.game.getLegalMoves(currentNode.state)

			# Create one children for each possible moves
			for move in moves:

				# Copy the parent state and change it with the new move
				newState = copy.deepcopy(currentNode.state)
				newState["board"][move] = self.player_id
				newState["player"] = (newState["player"] + 1) % 2

				# Get the square of the next move
				possibleSquares = self.game.getNewSquare(move, currentNode.state)

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

		return root


	def searchTree(self, root):
		# Minimax search with alpha-beta pruning
		result = self.minimax(root, depth=self.depth, maximizing_player=True, alpha=float('-inf'), beta=float('inf'))
		return result

	def minimax(self, node, depth, maximizing_player, alpha, beta):
		if depth == 0 or not node.children:
			return {"node": node, "score": self.evaluateBoard(node.state)}

		if maximizing_player:
			max_eval = float('-inf')
			for child in node.children:
				evaluation = self.minimax(child, depth - 1, False, alpha, beta)
				max_eval = max(max_eval, evaluation["score"])
				alpha = max(alpha, evaluation["score"])
				if beta <= alpha:
					break
			return {"node": evaluation["node"], "score": max_eval}
		else:
			min_eval = float('inf')
			for child in node.children:
				evaluation = self.minimax(child, depth - 1, True, alpha, beta)
				min_eval = min(min_eval, evaluation["score"])
				beta = min(beta, evaluation["score"])
				if beta <= alpha:
					break
			return {"node": evaluation["node"], "score": min_eval}

	def evaluateBoard(self, state):
		score = 0
		for sequence in [state["board"][i: i + 9] for i in range(0 ,81 ,9)]:

			for line in self.game.lines:
				if [sequence[i] for i in line['offsets']] == [self.player_id] * 3:
					score += 1
				elif [sequence[i] for i in line['offsets']] == [(self.player_id + 1) % 2] * 3:
					score -= 1
		# print(score,end="-")
		return score

# 0 > 9 > 81 > 729
# 0   1   2     3


if __name__ == '__main__':
	from Morpion import main
	main()
