from tkinter import *


class GameDisplay(object):

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

	def __init__(self, players, *,state = None):

		self.__players = players

		self.__setupBoard()
		if state is None:
			state = {"board": [-1] * 81, "player": 0, "square": 4}
		self.update(state)


	def __setupBoard(self, size = 800):
		self.fenetre = fenetre = Tk()

		fenetre.title("TIC-TAC-TOE")
		fenetre.geometry(f"{size}x{size}+500+0")
		self.canvas = canvas = Canvas(fenetre, height=size, width=size, bg="#0da292")
		canvas.place(x=-3, y=-3)

		self.margin = margin = 50
		self.cellWidth = cellWidth = (size - 2 * margin) / 9

		for i in range(9):
			bigX = (i % 3) * (cellWidth * 3) + margin
			bigY = (i // 3) * (cellWidth * 3) + margin
			for j in range(9):
				x = (j % 3) * cellWidth
				y = (j // 3) * cellWidth
				canvas.create_rectangle(bigX + x, bigY + y, bigX + x + cellWidth, bigY + y + cellWidth, fill="#13beac", outline="", tags=str(9 * i + j), activefill="#15d1be")
				canvas.create_text(bigX + x + cellWidth / 2, bigY + y + cellWidth / 2, text="", tags=str("t" + str(9 * i + j)), fill="#545454", font=("", 70))

		for i in range(1, 9):
			if i in [3, 6]:
				lineWidth = 5
			else:
				lineWidth = 1
			canvas.create_line(margin + i * cellWidth, margin, margin + i * cellWidth, size - margin, width=lineWidth, fill="#545454")
			canvas.create_line(margin, margin + i * cellWidth, size - margin, margin + i * cellWidth, width=lineWidth, fill="#545454")

		canvas.create_text(size / 2 - 200 ,margin / 2 ,text = f"{self.__players[0].name}:"  ,fill = "#545454" ,font = ("Avenir" ,30))
		canvas.create_text(size / 2 - 100 ,margin / 2 ,text = "0"  ,fill = "#545454" ,font = ("Avenir" ,30), tag="playerA")
		canvas.create_text(size / 2 ,margin / 2 ,text = "-"  ,fill = "#545454" ,font = ("Avenir" ,30))
		canvas.create_text(size / 2 + 100 ,margin / 2 ,text = f"{self.__players[1].name}:"  ,fill = "#545454" ,font = ("Avenir" ,30))
		canvas.create_text(size / 2 + 200 ,margin / 2 ,text = "0"  ,fill = "#545454" ,font = ("Avenir" ,30), tag="playerB")

		self.overlay = canvas.create_rectangle(0 ,0 ,0 ,0, fill = "" ,outline = "#f2ebd3" ,width = 3)


	def update(self, state):
		i = 0
		for cell in state["board"]:
			if cell == -1:
				symbol = ""
			elif cell == 0:
				symbol = "○"
			elif cell == 1:
				symbol = "X"
			self.canvas.itemconfigure(f"t{i}", text=symbol)
			i += 1
		self.__updateOverlay(state["square"])
		self.canvas.update()

		# TODO: Update this function
		index = 0
		self.score = {"A": 0, "B": 0}
		self.canvas.delete("lines")
		for sequence in [state["board"][i: i + 9] for i in range(0 ,81 ,9)]:

			for line in GameDisplay.lines:
				if [sequence[i] for i in line['offsets']] == [0] * 3:
					self.score['A'] += 1
					self.__createLine(index, line['type'], line['index'])
				elif [sequence[i] for i in line['offsets']] == [1] * 3:
					self.score['B'] += 1
					self.__createLine(index, line['type'], line['index'])
			index += 1

		self.canvas.itemconfigure("playerA", text=self.score['A'])
		self.canvas.itemconfigure("playerB", text=self.score['B'])


	def __updateOverlay(self, index):
		x = index % 3
		y = index // 3
		self.canvas.coords(
			self.overlay,
			self.margin + x * (self.cellWidth * 3),
			self.margin + y * (self.cellWidth * 3),
			self.margin + (x + 1) * (self.cellWidth * 3),
			self.margin + (y + 1) * (self.cellWidth * 3),
		)


	def __createLine(self, square, lineType, index, padding = 15):
		if lineType == "horizontal":
			coords = [
				self.margin + square % 3 * (3 * self.cellWidth) + padding,
				self.margin + square // 3 * (3 * self.cellWidth) + (index + 0.5) * self.cellWidth,
				self.margin + (square % 3 + 1) * (3 * self.cellWidth) - padding,
				self.margin + (square // 3) * (3 * self.cellWidth) + (index + 0.5) * self.cellWidth,
			]
		elif lineType == "vertical":
			coords = [
				self.margin + square % 3 * (3 * self.cellWidth) + (index + 0.5) * self.cellWidth,
				self.margin + square // 3 * (3 * self.cellWidth) + padding,
				self.margin + square % 3 * (3 * self.cellWidth) + (index + 0.5) * self.cellWidth,
				self.margin + (square // 3 + 1) * (3 * self.cellWidth) - padding,
			]
		elif lineType == "diagonal":
			if index == 0:
				coords = [
					self.margin + square % 3 * (3 * self.cellWidth) + padding,
					self.margin + square // 3 * (3 * self.cellWidth) + padding,
					self.margin + (square % 3 + 1) * (3 * self.cellWidth) - padding,
					self.margin + (square // 3 + 1) * (3 * self.cellWidth) - padding,
				]
			else:
				coords = [
					self.margin + (square % 3 + 1) * (3 * self.cellWidth) - padding,
					self.margin + square // 3 * (3 * self.cellWidth) + padding,
					self.margin + square % 3 * (3 * self.cellWidth) + padding,
					self.margin + (square // 3 + 1) * (3 * self.cellWidth) - padding,
				]

		self.canvas.create_line(coords, fill="#f2ebd3" ,tag="lines", width=4, capstyle="round")
