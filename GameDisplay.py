from tkinter import *
import Utils


class GameDisplay(object):

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
				canvas.create_rectangle(bigX + x, bigY + y, bigX + x + cellWidth, bigY + y + cellWidth, fill="#13beac", outline="", tags="cell" + str(9 * i + j), activefill="#15d1be")
				canvas.create_text(bigX + x + cellWidth / 2, bigY + y + cellWidth / 2, text="", tags="t" + str(9 * i + j), fill="#545454", font=("", 70))

		for i in range(1, 9):
			if i in [3, 6]:
				lineWidth = 5
			else:
				lineWidth = 1
			canvas.create_line(margin + i * cellWidth, margin, margin + i * cellWidth, size - margin, width=lineWidth, fill="#545454")
			canvas.create_line(margin, margin + i * cellWidth, size - margin, margin + i * cellWidth, width=lineWidth, fill="#545454")

		canvas.create_text(size / 2 ,margin / 2 ,text = "-"  ,fill = "#545454" ,font = ("Avenir" ,30))
		canvas.create_text(size / 4  ,margin / 2 ,text = f"{self.__players[0].name}: 0"  ,fill = "#545454" ,font = ("Avenir" ,30), tag="playerA")
		canvas.create_text(3 * size / 4 ,margin / 2 ,text = f"{self.__players[1].name}: 0"  ,fill = "#545454" ,font = ("Avenir" ,30), tag="playerB")

		self.overlay = canvas.create_rectangle(0 ,0 ,0 ,0, fill = "" ,outline = "#f2ebd3" ,width = 3)

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

		index = 0
		self.score = {"A": 0, "B": 0}
		self.canvas.delete("lines")
		for sequence in [state["board"][i: i + 9] for i in range(0 ,81 ,9)]:

			for line in Utils.lines:
				if [sequence[i] for i in line['offsets']] == [0] * 3:
					self.score['A'] += 1
					self.__createLine(index, line['type'], line['index'])
				elif [sequence[i] for i in line['offsets']] == [1] * 3:
					self.score['B'] += 1
					self.__createLine(index, line['type'], line['index'])
			index += 1

		self.canvas.itemconfigure("playerA", text=f"{self.__players[0].name}: {self.score['A']}")
		self.canvas.itemconfigure("playerB", text=f"{self.__players[1].name}: {self.score['B']}")

	def debug(self, data):
		for item in data:
			if 'color' in item:
				self.canvas.itemconfigure(f"t{item['cell']}", text=item['value'], fill=item['color'])
			else:
				self.canvas.itemconfigure(f"t{item['cell']}", text=item['value'])

		self.canvas.update()
