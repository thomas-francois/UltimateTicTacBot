import copy
from Bots.Node import Node
import Utils


class Bot_V2(object):

	def __init__(self, depth = 3):
		self.name = "V2"
		self.depth = depth

	def start(self, game, ID):
		self.game = game
		self.ID = ID

	def play(self):
		# print("start Move")
		root = self.createTree()
		result = self.searchTree(root)

		bestMove = result["node"].getLineage()[1]
		# print(f"\nBest move: {bestMove} (score: {result['score']})")
		# exit()
		# sleep(0.5)

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
				newState = copy.deepcopy(currentNode.state)
				newState["board"][move] = self.ID
				newState["player"] = (newState["player"] + 1) % 2

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

		return root


	def searchTree(self, root):
		# Minimax search
		result = self.minimax(root)
		return result

	def minimax(self, node):
		if not node.children:
			return {"node": node, "score": self.evaluateBoard(node.state)}

		if node.state["player"] == self.ID:
			max_value = float('-inf')
			best_move = node
			for child in node.children:
				value = self.minimax(child)
				if value["score"] > max_value:
					max_value = value["score"]
					best_move = child
			return {"node": best_move, "score": max_value}
		else:
			min_value = float('inf')
			best_move = node
			for child in node.children:
				value = self.minimax(child)
				if value["score"] < min_value:
					min_value = value["score"]
					best_move = child
			return {"node": best_move, "score": min_value}


	def evaluateBoard(self, state):
		score = 0
		# state = {'board': [1, -1, 1, 0, 0, 0, 1, 0, 0, -1, -1, 0, 1, -1, 0, 0, 0, 0, 0, 1, 0, 1, -1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 0, -1, 1, 1, 1, 1, 0, -1, -1, -1, 0, 1, 0, 1, 1, 1, 0, -1, 0, 1, -1, 1, 0, 0, -1, 1, 0, 1, 1, 1, 1, -1, -1, 0, 1, 0, -1, 0, 0], 'player': 0, 'square': 8}
		# player = self.player_id if maximizing_player else (self.player_id + 1) % 2
		point = -1 if state["player"] == self.ID else 1
		for sequence in [state["board"][i: i + 9] for i in range(0 ,81 ,9)]:

			for line in Utils.lines:
				if [sequence[i] for i in line['offsets']] == [self.ID] * 3:
					score += point
				elif [sequence[i] for i in line['offsets']] == [(self.ID + 1) % 2] * 3:
					score -= point
		# print(f"{score}",end=" ")
		return score

# 0 > 9 > 81 > 729
# 0   1   2     3


if __name__ == '__main__':
	from Morpion import main
	main()
