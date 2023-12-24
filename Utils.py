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


def calculteScore(state, names = ["A", "B"]):
	score = {name: 0 for name in names}

	for sequence in [state["board"][i: i + 9] for i in range(0 ,81 ,9)]:

		for line in lines:
			if [sequence[i] for i in line['offsets']] == [0] * 3:
				score[names[0]] += 1
			elif [sequence[i] for i in line['offsets']] == [1] * 3:
				score[names[1]] += 1

	return score


# def printDebugTree(node, indent="│ "):
# 	print(f"{indent * node.depth}├── {node.move}")
# 	for child in node.children:
# 		printDebugTree(child, indent)

def printDebugTree(node, indent="│   "):

	if node.isRoot:
		print(node.move)
	elif node.parent.isLeaf is False and node == node.parent.children[-1]:
		print(f"{indent * (node.depth - 1)}└── {node.move} <{len(node.children)}>")
	else:
		print(f"{indent * (node.depth - 1)}├── {node.move} <{len(node.children)}>")

	leafs = []
	notLeafs = []
	for child in node.children:
		if child.isLeaf:
			leafs.append(child)
		else:
			notLeafs.append(child)

	for child in notLeafs:
		printDebugTree(child, indent)
	if leafs:
		print(f"{indent * node.depth}└── {' '.join([str(leaf.move) for leaf in leafs])}")

