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

        # create deck and list of images of cards
        self.deck = Deck(4)
        self.Images = []
        for i in self.deck.cards:
            Aux = str(i.value) + i.color + ".png"
            self.Images.append(tk.PhotoImage(file=Aux))

        self.cards = list()
        self.places = list()

        self.grids = [200, 350, 500, 650, 800, 950, 1100, 1250, 1400, 1550]

        val = 0
        for i in self.grids:
            self.places.append(Queue(i, self.canvas, self.deck.cards[val], val))
            val += 1

        # data of object that is moving
        self.move_data = {"object": None, "x": 0, "y": 0, "startX": 0, "startY": 0, "card": None,
                          "startPlace": None}
        self.add_cards("movable")
        self.move_bind("movable")

        self.window.mainloop()

    def add_cards(self, tag):
        val = 0
        for i in self.places:
            self.cards.append(LabelCard(self.window, i.lastCard.color, i.lastCard.value,
                                        tag, self.canvas, self.Images[val], i.CoordX + 50, i.CoordY + 70))
            val += 1

    def move_bind(self, tag):
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(tag, "<B1-Motion>", self.move)


    def move_start(self, event):
        self.move_data["object"] = self.canvas.find_closest(event.x, event.y)
        canvasItemId = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        print(canvasItemId)
        if canvasItemId[-1] in self.canvas.find_withtag("movable"):
            print("true")
            print(self.canvas.find_withtag("movable"))
            self.move_data["x"] = event.x
            self.move_data["y"] = event.y
            cardCoords = self.canvas.coords(self.move_data["object"])
            self.move_data["startX"] = cardCoords[0]
            self.move_data["startY"] = cardCoords[1]
            aux = (int(cardCoords[0]) - 150)
            aux = int(aux / 150)
            self.move_data["card"] = self.places[aux].lastCard
            self.move_data["startPlace"] = self.places[aux]
            self.canvas.tag_raise(self.move_data["object"])
        else:
            self.move_data["object"] = None
            print("false")
            print(self.canvas.find_withtag("movable"))

    def drop(self):
        cardCoords = self.canvas.coords(self.move_data["object"])
        # checking on which place the card is dropped
        aux = (int(cardCoords[0]) - 150)
        aux = int(aux / 150)
        if cardCoords[0] >= 150 and (self.places[aux].lastCard == None or
                                     ((self.places[aux].lastCard.value - 1)== self.move_data["card"].value)):
            self.places[aux].CoordY = 60 + (20 * (len(self.places[aux].cards)))
            x = self.places[aux].CoordX - cardCoords[0] + 50
            y = self.places[aux].CoordY - cardCoords[1] + 70
            self.canvas.move(self.move_data["object"], x, y)
            self.places[aux].cards.append(self.move_data["card"])
            if self.places[aux].lastCard != None:
                for i in self.cards:
                    if i.value == self.places[aux].lastCard.value and i.color == self.places[aux].lastCard.color:
                        print(i.id)
                        self.canvas.dtag(i.id,"movable")
            self.places[aux].lastCard = self.move_data["card"]
            self.move_data["startPlace"].cards.pop()
            if len(self.move_data["startPlace"].cards) != 0:
                self.move_data["startPlace"].lastCard =  self.move_data["startPlace"].cards[-1]
                for i in self.cards:
                    if (i.value == self.move_data["startPlace"].lastCard.value
                            and i.color == self.move_data["startPlace"].lastCard.color):
                        self.canvas.addtag_withtag("movable",i.id)
            else:
                self.move_data["startPlace"].lastCard = None
        else:
            x = self.move_data["startX"] - cardCoords[0]
            y = self.move_data["startY"] - cardCoords[1]
            self.canvas.move(self.move_data["object"], x, y)

    def move_stop(self, event):
        if self.move_data["object"] != None:
            self.drop()
            self.move_data["card"] = None
            self.move_data["object"] = None
            self.move_data["x"] = 0
            self.move_data["y"] = 0
            self.move_data["startX"] = 0
            self.move_data["startY"] = 0
            self.move_data["Value"] = 0

    def move(self, event):
        if self.move_data["object"] != None:
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