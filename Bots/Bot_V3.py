import copy
from Bots.Node import Node
import Utils
from time import sleep


class Bot_V3(object):

	def __init__(self, depth = 3):
		self.name = "V3"
		self.depth = depth

	def start(self, game, ID):
		self.game = game
		self.ID = ID

	def play(self):
		# print("start Move")
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
				newState = copy.deepcopy(currentNode.state)
				newState["board"][move] = newState["player"]
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

		# Utils.printDebugTree(root)
		return root


	def searchTree(self, root):
		# Minimax search

		results = []
		for node in root.children:
			result = self.minimax(node)
			results.append({"node": node, "cell": node.move, "value": result["score"]})

		# self.game.display.debug(results)
		# print(results)
		# sleep(1)
		bestMove = max(results, key=lambda x: x["value"])
		return bestMove


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
		# point = -1 if state["player"] == self.ID else 1

		for sequence in [state["board"][i: i + 9] for i in range(0 ,81 ,9)]:

			for line in Utils.lines:
				if [sequence[i] for i in line['offsets']] == [self.ID] * 3:
					score += 1
				elif [sequence[i] for i in line['offsets']] == [(self.ID + 1) % 2] * 3:
					score -= 1

		return score


if __name__ == '__main__':
	from Morpion import main
	main()
