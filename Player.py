import tkinter as tk


class Player(object):

    def __init__(self, name = "Player"):
        self.name = name

    def start(self, game, player_id):
        self.game = game
        self.player_id = player_id

        self.choice = tk.IntVar()

        game.fenetre.bind("<Button-1>" ,self.click)

    def play(self):
        self.choice.set(-1)
        print("Player's turn")

        while True:
            self.game.fenetre.wait_variable(self.choice)
            if self.choice.get() != -1:
                break
        return self.game.playMove(self.player_id, self.choice.get())

    def click(self, event):
        try:
            tile = int(self.game.canvas.itemconfigure("current")["tags"][4].replace(" current" ,""))
            self.choice.set(tile)
        except Exception:
            return
