import tkinter as tk
from Card import Card
from Card import LabelCard
from Queue import Queue
from Deck import Deck
from Stack import Stack


class Board:
    def __init__(self):
        self.window = tk.Tk()


        self.window.geometry("1700x800")
        self.window.resizable(False, False)
        # board with cards
        self.canvas = tk.Canvas(width=1700, height=800, bg="#3ea84a")
        self.canvas.pack()

        # create deck and list of images of cards
        self.deck = Deck(2)
        self.Images = []
        for i in self.deck.cards:
            Aux = str(i.value) + i.color + ".png"
            self.Images.append(tk.PhotoImage(file=Aux))
        self.Images.append(tk.PhotoImage(file="Back.png"))

        self.stack = Stack(self.deck, self.canvas, self.Images[-1])
        self.cards = list()
        self.hiddenCards = list()
        self.places = list()

        self.grids = [200, 350, 500, 650, 800, 950, 1100, 1250, 1400, 1550]

        val = 0
        for i in self.grids:
            self.places.append(Queue(i, self.canvas, self.deck.cards[val], val))
            val += 1

        for i in self.places:
            ran = 5
            if i.grid > 3:
                ran -= 1
            for j in range(ran):
                i.HiddenCards.append(self.deck.cards[val])
                i.HiddenVals.append(val)
                val += 1
        # data of object that is moving
        self.move_data = {"object": None, "x": 0, "y": 0, "startX": 0, "startY": 0, "cards": [],
                          "startPlace": None, "card": None}
        self.add_cards("movable")
        self.move_bind("movable")
        self.add_cards_bind("addCards")
        self.window.mainloop()

    def add_cards(self, tag):
        val = 0
        for i in self.places:
            for j in i.HiddenCards:
                self.hiddenCards.append(LabelCard(self.window, j.color, j.value, None, self.canvas, self.Images[-1],
                                                  i.CoordX+50, i.CoordY + 70, i.grid))
                i.CoordY += 10
        for i in self.places:
            self.cards.append(LabelCard(self.window, i.lastCard.color, i.lastCard.value,
                                        tag, self.canvas, self.Images[val], i.CoordX + 50, i.CoordY + 70, i.grid))
            val += 1
        for i in self.places:
            for j in self.cards:
                if j.grid == i.grid:
                    i.idList.append(j.id)
            for j in self.hiddenCards:
                if j.grid == i.grid:
                    i.HiddenIdList.append(j.id)

    def move_bind(self, tag):
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(tag, "<B1-Motion>", self.move)

    def add_cards_bind(self, tag):
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.add_more_cards)

    def check_if_places_not_empty(self):
        for i in self.places:
            if i.lastCard is None:
                return False
        return True
    def add_more_cards(self, event):
        if len(self.stack.cards) > 0 and self.check_if_places_not_empty():
            val = len(self.deck.cards) - len(self.stack.cards)
            for i in self.places:
                value = self.deck.cards[val].value + 1
                color = self.deck.cards[val].color
                j = len(i.idList) - 1
                move = list()
                while j >= 0 and value == i.cards[j].value and color == i.cards[j].color:
                    move.append(i.idList[j])
                    value += 1
                    j -= 1
                for j in self.cards:
                    if j.grid == i.grid and j.id not in move:
                        self.canvas.dtag(j.id, "movable")
                i.CoordY = 70 + (30 * (len(i.cards) - 1))
                self.cards.append(LabelCard(self.window, self.deck.cards[val].color, self.deck.cards[val].value,
                                           "movable", self.canvas, self.Images[val], i.CoordX + 50, i.CoordY + 90, i.grid))
                tmpCard = Card(self.deck.cards[val].color, self.deck.cards[val].value)
                i.cards.append(tmpCard)
                i.lastCard = tmpCard
                val += 1
            for i in self.places:
                for j in self.cards:
                    if j.grid == i.grid and j.id not in i.idList:
                        i.idList.append(j.id)
            self.stack.cards = self.stack.cards[10:]
            if len(self.stack.cards) == 0:
                self.canvas.delete(self.stack.id)
            print("zostalo: "+str(len(self.stack.cards))+" kart")
        elif len(self.stack.cards) == 0:
            print("brak kart")
        else:
            print("zakryj wszystkie pola")

    def move_start(self, event):
        ListcardsIds= list()
        for i in self.places:
            ListcardsIds.extend(i.idList)
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
            checkList = self.canvas.find_withtag("movable")
            for i in idList:
                for j in self.cards:
                    if i == j.id and (j.value > self.move_data["card"].value or i not in checkList):
                        removeList.append(i)
            for i in removeList:
                if i in idList:
                    idList.remove(i)
            for i in idList:
                if i in ListcardsIds:
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

    def partition(self, array, low, high):
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
            self.places[aux].CoordY = 60 + (30 * (len(self.places[aux].cards))) + (10 * len(self.places[aux].HiddenCards))
            if(self.places[aux] == self.move_data["startPlace"]):
                self.places[aux].CoordY -= 30
            x = self.places[aux].CoordX - cardCoords[0] + 50
            y = self.places[aux].CoordY - cardCoords[1] + 70
            for i in self.move_list:
                self.canvas.move(i, x, y)
            self.places[aux].cards.extend(self.move_data["cards"])
            for i in self.move_data["cards"]:
                self.places[aux].idList.append(i.id)

            for i in self.places[aux].idList:
                    self.canvas.dtag(i, "movable")

            if self.places[aux].cards[-1] != None:
                i = len(self.places[aux].idList) - 1
                val = self.places[aux].cards[-1].value
                col = self.places[aux].cards[-1].color
                mov = list()
                while i >= 0 and self.places[aux].cards[i].value == val and self.places[aux].cards[i].color == col:
                    mov.append(self.places[aux].idList[i])
                    i -= 1
                    val += 1
                for i in mov:
                    self.canvas.addtag_withtag("movable", i)


            self.places[aux].lastCard = self.move_data["cards"][-1]
            for i in self.move_data["cards"]:
                i.grid = self.places[aux].grid
            if len(self.move_data["startPlace"].cards) > lenOfMoved:
                for i in self.move_data["cards"]:
                    self.move_data["startPlace"].cards.pop()
                    self.move_data["startPlace"].idList.remove(i.id)
                self.move_data["startPlace"].lastCard = self.move_data["startPlace"].cards[-1]
                listOfMovable = list()
                i = len(self.move_data["startPlace"].cards) - 1
                val = self.move_data["startPlace"].lastCard.value
                while i >= 0 and self.move_data["startPlace"].cards[i].value == val \
                    and self.move_data["startPlace"].cards[i].color == self.move_data["startPlace"].lastCard.color:
                        listOfMovable.append(self.move_data["startPlace"].idList[i])
                        i -= 1
                        val += 1
                for i in self.move_data["startPlace"].idList:
                        self.canvas.dtag(i, "movable")
                for i in listOfMovable:
                    self.canvas.addtag_withtag("movable", i)

            else:
                if len(self.move_data["startPlace"].HiddenCards) > 0:
                    self.move_data["startPlace"].lastCard = self.move_data["startPlace"].HiddenCards[-1]
                    print(self.move_data["startPlace"].lastCard)
                    self.move_data["startPlace"].cards.append(self.move_data["startPlace"].HiddenCards[-1])
                    self.move_data["startPlace"].idList.append(self.move_data["startPlace"].HiddenIdList[-1])
                    print(self.move_data["startPlace"].HiddenVals[-1])
                    im = self.Images[self.move_data["startPlace"].HiddenVals[-1]]
                    self.canvas.itemconfig(self.move_data["startPlace"].HiddenIdList[-1], image=im, tag="movable")
                    self.move_data["startPlace"].HiddenCards.pop()
                    self.move_data["startPlace"].HiddenIdList.pop()
                    self.move_data["startPlace"].HiddenVals.pop()
                    print(len(self.move_data["startPlace"].HiddenCards))
                    print(len(self.move_data["startPlace"].HiddenIdList))
                    self.move_data["startPlace"].CoordY += 10
                else:
                    self.move_data["startPlace"].lastCard = None
                    self.move_data["startPlace"].cards.clear()
                    self.move_data["startPlace"].idList.clear()
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
            self.canvas.move(i, dx, dy + ((self.move_list.index(i))*30))

board = Board()