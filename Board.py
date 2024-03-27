import tkinter as tk
from Card import LabelCard
from Queue import Queue
from Deck import Deck

class Board:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1700x800")
        self.window.resizable(False, False)
        # board with cards
        self.canvas = tk.Canvas(width=1700, height=800, bg="#3ea84a")
        self.canvas.pack()

        # create deck
        self.deck = Deck(4)

        self.places = list()

        # data of object that is moving
        self.move_data = {"object": None, "x": 0, "y": 0, "startX": 0, "startY": 0, "Value": 0}
        self.add_cards("movable")
        self.move_bind("movable")
        self.grids = [200, 350, 500, 650, 800, 950, 1100, 1250, 1400, 1550]

        val = 1
        for i in self.grids:
            self.places.append(Queue(i, self.canvas, self.deck.cards[val]))
            val += 1

        print("wartosci kart z kolejek:")
        for i in self.places:
            print(i.lastCard.value)
            print(i.lastCard.color)

        self.window.mainloop()

    def add_cards(self, tag):
        self.card = LabelCard(self.window, self.deck.cards[0].color, self.deck.cards[0].value, tag, self.canvas)
        print("Twoja karta:")
        print(self.deck.cards[0].color)
        print(self.deck.cards[0].value)

    def move_bind(self, tag):
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(tag, "<B1-Motion>", self.move)


    def move_start(self, event):
        self.move_data["object"] = self.canvas.find_closest(event.x, event.y)
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y
        cardCoords = self.canvas.coords(self.move_data["object"])
        self.move_data["startX"] = cardCoords[0]
        self.move_data["startY"] = cardCoords[1]
        self.move_data["Value"] = self.card.value
        self.canvas.tag_raise(self.move_data["object"])

    def drop(self):
        cardCoords = self.canvas.coords(self.move_data["object"])
        # code to check on which place you dropped your card
        aux = (int(cardCoords[0]) - 150)
        aux = int(aux / 150)
        if cardCoords[0] >= 150 and (self.places[aux].lastCard.value - 1) == self.move_data["Value"]:
            x = self.places[aux].CoordX - cardCoords[0]
            y = self.places[aux].CoordY - cardCoords[1]
            self.canvas.move(self.move_data["object"],x,y)
        else:
            x = self.move_data["startX"] - cardCoords[0]
            y = self.move_data["startY"] - cardCoords[1]
            self.canvas.move(self.move_data["object"], x, y)

    def move_stop(self, event):
        self.drop()
        self.move_data["object"] = None
        self.move_data["x"] = 0
        self.move_data["y"] = 0
        self.move_data["startX"] = 0
        self.move_data["startY"] = 0
        self.move_data["Value"] = 0

    def move(self, event):
        if event.x < 100:
            event.x = 100 - abs(event.x-100)
            if(abs(event.x-100) > 10):
                event.x = 100
        if event.y < 100:
            event.y = 100 - abs(event.y - 100)
            if (abs(event.y - 100) > 10):
                event.y = 100

        if event.x > 1600:
            event.x = 1100 - abs(event.x-1600)
            if (abs(event.x-1600)>10):
                event.x = 1600
        if event.y > 700:
            event.y = 700 - abs(event.y - 700)
            if (abs(event.y - 700) > 10):
                event.y = 700

        dx = event.x - self.move_data["x"]
        dy = event.y - self.move_data["y"]

        self.canvas.move(self.move_data["object"], dx, dy)
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y

board = Board()