import tkinter as tk


class Player(object):

    def __init__(self, name = "Player"):
        self.name = name

    def start(self, game, ID):
        self.game = game
        self.ID = ID

        self.choice = tk.IntVar()

        game.display.fenetre.bind("<Button-1>" ,self.click)

    def play(self):
        self.choice.set(-1)
        print("Player's turn")

        while True:
            self.game.display.fenetre.wait_variable(self.choice)
            if self.choice.get() != -1:
                break

        self.game.playMove(self, self.choice.get())

    def click(self, event):
        try:
            tile = int(self.game.display.canvas.itemconfigure("current")["tags"][4].replace(" current" ,""))
            self.choice.set(tile)
        except Exception:
            return
