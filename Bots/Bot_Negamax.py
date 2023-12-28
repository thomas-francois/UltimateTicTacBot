from Bots.Node import Node
import Utils


class Bot_Negamax(object):

    def __init__(self, depth=3):
        self.name = "Negamax d=" + str(depth)
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

    def searchTree(self, root):
        # Negamax search
        # self.searches = 0
        result = self.negamax(root, alpha=float('-inf'), beta=float('inf'))
        # print(self.searches)
        return result

    def negamax(self, node, alpha, beta):
        if not node.children:
            return {"node": node, "score": self.evaluateBoard(node.state)}

        max_value = float('-inf')
        best_move = node
        for child in node.children:
            evaluation = -self.negamax(child, -beta, -alpha)["score"]
            if evaluation > max_value:
                max_value = evaluation
                best_move = child
            alpha = max(alpha, evaluation)
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
                if testSet == {self.ID}:
                    score -= 10
                elif testSet == {1 - self.ID}:
                    score += 10

                if -1 in test and test.count(self.ID) == 2:
                    score -= 2
                elif -1 in test and test.count(1 - self.ID) == 2:
                    score += 2

            if sequence[4] == self.ID:
                score -= 1
            elif sequence[4] == 1 - self.ID:
                score += 1

        return score
