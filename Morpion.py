from random import choice
from tkinter import *

from Player import Player
import Bot


def main():
    state = None
    # state = {'board': [1, -1, 1, 0, 0, 0, 1, 0, 0, -1, -1, 0, 1, -1, 0, 0, 0, 0, 0, 1, 0, 1, -1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 0, -1, 1, 1, 1, 1, 0, -1, -1, -1, 0, 1, 0, 1, 1, 1, 0, -1, 0, 1, -1, 1, 0, 0, -1, 1, 0, 1, 1, 1, 1, -1, -1, 0, 1, 0, -1, 0, 0], 'player': 0, 'square': 8}
    game = Game(Bot.Random(), Player(), windowSize = 800, state=state)
    game.start()


class Game(object):

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

    def __init__(self, playerA, playerB, *, windowSize = 800 ,state = None):
        self.players = [playerA, playerB]
        self.isStarted = False

        if state is None:
            self.board = [-1] * 81
            self.player = 0
            self.currentSquare = 4
        else:
            self.board = state["board"]
            self.player = state["player"]
            self.currentSquare = state["square"]

        self.__setupBoard(windowSize)
        self.__updateBoard()

    def __setupBoard(self, size):
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

        canvas.create_text(size / 2 - 200 ,margin / 2 ,text = f"{self.players[0].name}:"  ,fill = "#545454" ,font = ("Avenir" ,30))
        canvas.create_text(size / 2 - 100 ,margin / 2 ,text = "0"  ,fill = "#545454" ,font = ("Avenir" ,30), tag="playerA")
        canvas.create_text(size / 2 ,margin / 2 ,text = "-"  ,fill = "#545454" ,font = ("Avenir" ,30))
        canvas.create_text(size / 2 + 100 ,margin / 2 ,text = f"{self.players[1].name}:"  ,fill = "#545454" ,font = ("Avenir" ,30))
        canvas.create_text(size / 2 + 200 ,margin / 2 ,text = "0"  ,fill = "#545454" ,font = ("Avenir" ,30), tag="playerB")

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

    def __updateBoard(self, state = None):
        i = 0
        for cell in self.board:
            if cell == -1:
                symbol = ""
            elif cell == 0:
                symbol = "○"
            elif cell == 1:
                symbol = "X"
            self.canvas.itemconfigure(f"t{i}", text=symbol)
            i += 1
        self.__updateOverlay(self.currentSquare)
        self.canvas.update()

        index = 0

        self.score = {"A": 0, "B": 0}
        self.canvas.delete("lines")
        for sequence in [self.board[i: i + 9] for i in range(0 ,81 ,9)]:

            for line in Game.lines:
                if [sequence[i] for i in line['offsets']] == [0] * 3:
                    self.score['A'] += 1
                    self.__createLine(index, line['type'], line['index'])
                elif [sequence[i] for i in line['offsets']] == [1] * 3:
                    self.score['B'] += 1
                    self.__createLine(index, line['type'], line['index'])
            index += 1

        self.canvas.itemconfigure("playerA", text=self.score['A'])
        self.canvas.itemconfigure("playerB", text=self.score['B'])

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

    def __endGame(self):
        self.isStarted = False
        print("Game ended")

    def start(self):
        self.players[0].start(self, 0)
        self.players[1].start(self, 1)

        self.isStarted = True
        while self.isStarted:
            result = self.players[self.player].play()
            if result != "valid":
                print("Not valid move tried")
                continue
            self.player = (self.player + 1) % 2

        self.fenetre.mainloop()

    def playMove(self, player, move):
        if player == self.player and move in self.getLegalMoves():
            self.board[move] = player

            # If board is full, end the game
            if -1 not in self.board:
                self.__updateBoard()
                self.__endGame()
                return "end"

            newSquare = self.getNewSquare(move)
            if isinstance(newSquare, list):
                self.currentSquare = choice(newSquare)
            else:
                self.currentSquare = newSquare

            self.__updateBoard()
            # print(self.getState())
            return "valid"

        else:
            return "invalid"
            # raise Exception(f"Move cannot be played: {player} {self.player} and {move} in {self.getLegalMoves()} ({self.currentSquare})\n{self.board}")

    def getLegalMoves(self, state = None ,* ,square = None):
        board = state["board"] if state is not None else self.board
        if square is None:
            square = state["square"] if state is not None else self.currentSquare

        return [i for i in range(81) if board[i] == -1 and i // 9 == square]

    def getNewSquare(self, move, state = None):
        if not state:
            state = self.getState()

        targetSquare = move % 9

        # If target square is not full, it becomes the new current square
        if self.getLegalMoves(state, square = targetSquare) != []:
            return targetSquare

        # If target square is full and the current square is not full, it remains the same
        elif self.getLegalMoves(state, square = state["square"]) != []:
            return state["square"]

        # Else choose a random not full square:
        else:
            possibleSquares = []
            for i in range(9):
                if self.getLegalMoves(state, square = i) != []:
                    possibleSquares.append(i)

            return possibleSquares

    def getCurrentScore(player = None):
        if player is None:
            return self.score
        return self.score[player]

    def getState(self):
        return {"board": self.board, "player": self.player, "square": self.currentSquare}

    def forceUpdate(self, state):
        self.board = state["board"]
        self.player = state["player"]
        self.currentSquare = state["square"]
        self.__updateBoard()


if __name__ == '__main__':
    main()
    # x = Game(Player(), Player())
    # y = x.getLegalMoves({'board': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], 'player': 0, 'square': 4})
    # print(y)
    # exit()

