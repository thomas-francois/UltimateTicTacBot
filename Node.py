class Node(object):

	members = {}

	def __init__(self, move, state, parent = None):
		self.move = move
		self.state = state
		self.parent = parent
		self.children = []
		# if parent is not None:
		Node.members.setdefault(self.depth, []).append(self)

	def insertChild(self, child):
		self.children.append(child)

	def removeChild(self, child):
		if child in self.children:
			self.children.remove(child)

	def getLineage(self):
		if self.isRoot:
			return [self.move]
		return [*self.parent.getLineage(), self.move]

	@property
	def isRoot(self):
		return self.parent is None

	@property
	def isLeaf(self):
		return self.children == []

	@property
	def rootNode(self):
		if self.isRoot:
			return self
		return self.parent.rootNode

	@property
	def depth(self):
		if self.isRoot:
			return 0
		return self.parent.depth + 1

	@classmethod
	def getValidNode(cls, depth):
		for i in range(depth):
			if i in cls.members and len(cls.members[i]) != 0:
				return cls.members[i].pop(0)
		return None

	@classmethod
	def remove(cls, node):
		cls.members[node.depth].remove(node)

	@classmethod
	def debug(cls):
		return cls.members

	@classmethod
	def resetTree(cls):
		cls.members = {}

	def __str__(self):
		return self.move


if __name__ == '__main__':
	state = ""
	depth = 3

	# Create starting node
	Node(-1, state)

	print("Tree :", Node.debug())

	currentNode = Node.getValidNode(depth)

	while currentNode is not None:
		# Get all legal moves from the current state and create children



		currentNode.insertChild(Node(0, state, currentNode))

		# Remove node from tree and get a new one
		print("Tree :", Node.debug())

		currentNode = Node.getValidNode(depth)
