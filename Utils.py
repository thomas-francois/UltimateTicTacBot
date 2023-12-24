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
