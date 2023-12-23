#        x
#      /    \
#     x      x
#    / \    /  \
#   x   x   x   x
#  / \ / \ / \ / \
#  0 8 7 1 4 9 3 4

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

# Build the tree
root = Node("x")
root.children = [Node("x"), Node("x")]
root.children[0].children = [Node("x"), Node("x")]
root.children[1].children = [Node("x"), Node("x")]

root.children[0].children[0].children = [Node(0), Node(8)]
root.children[0].children[1].children = [Node(7), Node(1)]
root.children[1].children[0].children = [Node(4), Node(9)]
root.children[1].children[1].children = [Node(3), Node(4)]

def minimax(node, depth, is_maximizing):
    if depth == 0 or not node.children:
        return node.value

    if is_maximizing:
        max_value = float('-inf')
        for child in node.children:
            value = minimax(child, depth - 1, False)
            max_value = max(max_value, value)
        return max_value
    else:
        min_value = float('inf')
        for child in node.children:
            value = minimax(child, depth - 1, True)
            min_value = min(min_value, value)
        return min_value

# Call the minimax algorithm on the root node
result = minimax(root, float('inf'), True)
print(result)
