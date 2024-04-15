import tkinter as tk
from Card import Card
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
        self.move_data = {"object": None, "x": 0, "y": 0, "startX": 0, "startY": 0, "cards": [],
                          "startPlace": None, "card": None}
        self.add_cards("movable")
        self.move_bind("movable")

        self.window.mainloop()

    def add_cards(self, tag):
        val = 0
        for i in self.places:
            self.cards.append(LabelCard(self.window, i.lastCard.color, i.lastCard.value,
                                        tag, self.canvas, self.Images[val], i.CoordX + 50, i.CoordY + 70, i.grid))
            val += 1

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
        aux = (int(cardCoords[0]) - 150)
        aux = int(aux / 150)
        cardId = self.move_data["object"][-1]
        self.move_data["startPlace"] = self.places[aux]
        self.move_list = list()
        for i in self.cards:
            if cardId == i.id:
                self.move_data["card"] = i
        idList = list()
        if self.check_if_card_is_last():
            self.move_list.append(self.move_data["object"])
            while len(self.canvas.find_above(self.move_data["card"].id)) != 0:
                self.canvas.tag_raise(self.move_data["object"])
            idList.append(self.move_data["object"][0])
        else:
            idList.extend(self.canvas.find_overlapping(event.x, event.y, event.x, 700))
            removeList = list()
            for i in idList:
                for j in self.cards:
                    if i == j.id and j.value > self.move_data["card"].value:
                        removeList.append(i)
            for i in removeList:
                if i in idList:
                    idList.remove(i)
            for i in idList:
                if i > 10:
                    self.move_list.append(i)
        for i in self.cards:
            for j in idList:
                if j == i.id:
                    self.move_data["cards"].append(i)
        # sorting cards, so the list of cards in queue will be in correct order
        self.quickSort(self.move_data["cards"], 0, len(self.move_data["cards"]) - 1)
        self.move_data["cards"].reverse()
        for i in self.move_data["cards"]:
            while len(self.canvas.find_above(i.id)) != 0:
                self.canvas.tag_raise(i.id)

    def partition(self,array, low, high):
        pivot = array[high]

        i = low - 1

        for j in range(low, high):
            if array[j].value <= pivot.value:
                i = i + 1

                (array[i], array[j]) = (array[j], array[i])

        (array[i + 1], array[high]) = (array[high], array[i + 1])

        return i + 1

    def quickSort(self,array, low, high):
        if low < high:
            pi = self.partition(array, low, high)

            self.quickSort(array, low, pi - 1)

            self.quickSort(array, pi + 1, high)

    def drop(self):
        lenOfMoved = len(self.move_data["cards"])
        cardCoords = self.canvas.coords(self.move_data["object"])
        # checking on which place the card is dropped
        aux = (int(cardCoords[0]) - 150)
        aux = int(aux / 150)
        if cardCoords[0] >= 150 and (self.places[aux].lastCard == None or
                    ((self.places[aux].lastCard.value - 1) == self.move_data["cards"][0].value)):
            self.places[aux].CoordY = 60 + (20 * (len(self.places[aux].cards)))
            if(self.places[aux] == self.move_data["startPlace"]):
                self.places[aux].CoordY -= 20
            x = self.places[aux].CoordX - cardCoords[0] + 50
            y = self.places[aux].CoordY - cardCoords[1] + 70
            for i in self.move_list:
                self.canvas.move(i, x, y)
            self.places[aux].cards.extend(self.move_data["cards"])
            if self.places[aux].lastCard != None:
                i = 0
                if self.places[aux].lastCard.color != self.move_data["card"].color:
                    for i in self.cards:
                        if i.grid == self.places[aux].grid:
                            self.canvas.dtag(i.id, "movable")
            self.places[aux].lastCard = self.move_data["cards"][-1]
            for i in self.move_data["cards"]:
                i.grid = self.places[aux].grid
            if len(self.move_data["startPlace"].cards) > lenOfMoved:
                for i in range(len(self.move_data["cards"])):
                    self.move_data["startPlace"].cards.pop()
                self.move_data["startPlace"].lastCard = self.move_data["startPlace"].cards[-1]
                listOfMovable = list()
                i = len(self.move_data["startPlace"].cards) - 1
                val = self.move_data["startPlace"].lastCard.value
                while i >= 0 and self.move_data["startPlace"].cards[i].value == val \
                    and self.move_data["startPlace"].cards[i].color == self.move_data["startPlace"].lastCard.color:
                        listOfMovable.append(self.move_data["startPlace"].cards[i])
                        i -= 1
                        val += 1
                for i in self.cards:
                    if i.grid == self.move_data["startPlace"].grid:
                        self.canvas.dtag(i.id, "movable")
                for i in listOfMovable:
                    for j in self.cards:
                        if (i.value == j.value and i.color == j.color) and j.grid == self.move_data["startPlace"].grid:
                            self.canvas.addtag_withtag("movable", j.id)

            else:
                self.move_data["startPlace"].lastCard = None
                self.move_data["startPlace"].cards.clear()
                self.move_data["startPlace"].CoordY = 60
        else:
            x = self.move_data["startX"] - cardCoords[0]
            y = self.move_data["startY"] - cardCoords[1]
            for i in self.move_list:
                self.canvas.move(i, x, y)


    def move_stop(self, event):
        if self.move_data["object"] != None:
            self.drop()
            #for i in self.places:
                #print("----------")
                #print("grid: " + str(i.grid))
                #for j in i.cards:
                    #print(j.value)
            #for i in self.places:
                #print("----------")
                #if(i.lastCard != None):
                    #print("grid: " + str(i.grid)+ " last:" + str(i.lastCard.value))
            # for j in i.cards:
            # print(j.value)
            self.move_data["card"] = None
            self.move_data["cards"].clear()
            self.move_data["object"] = None
            self.move_data["x"] = 0
            self.move_data["y"] = 0
            self.move_data["startX"] = 0
            self.move_data["startY"] = 0
            self.move_data["Value"] = 0
            #lista = self.canvas.find_withtag("movable")
            #for i in range(21):
                #if i>10 and i not in lista:
                    #print(i)


    def check_if_card_is_last(self):
        for i in self.places:
            if i.lastCard != None:
                if (i.lastCard.color == self.move_data["card"].color and
                    i.lastCard.value == self.move_data["card"].value and
                    i.grid == self.move_data["card"].grid):
                    return True
        return False

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
        for i in self.move_list:
            cardCoords = self.canvas.coords(i)
            dx = event.x - cardCoords[0]
            dy = event.y - cardCoords[1]
            self.canvas.move(i, dx, dy + ((self.move_list.index(i))*20))

board = Board()