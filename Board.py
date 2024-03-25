import tkinter as tk
from Card import LabelCard


class Board:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x700")
        self.window.resizable(False, False)
        # board with cards
        self.canvas = tk.Canvas(width=1200, height=700, bg="#3ea84a")
        self.canvas.pack()

        # data of object that is moving
        self.move_data = {"object": None, "x": 0, "y": 0, "startX": 0, "startY": 0}
        self.add_cards("movable")
        self.move_bind("movable")
        self.place = self.canvas.create_rectangle(200, 150, 290, 60)
        self.place2 = self.canvas.create_rectangle(500, 150, 590, 60)
        self.window.mainloop()

    def add_cards(self, tag):
        self.card = LabelCard(self.window, "spades", 1, tag, self.canvas)

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
        self.canvas.tag_raise(self.move_data["object"])

    def drop(self):
        cardCoords = self.canvas.coords(self.move_data["object"])
        if(cardCoords[0]>= 110 and cardCoords[0]<=290):
            coords = self.canvas.coords(self.place)
            x = coords[0] - cardCoords[0]
            y = coords[1] - cardCoords[1]
            self.canvas.move(self.move_data["object"],x,y)
        elif (cardCoords[0] >= 410 and cardCoords[0] <= 590):
            coords = self.canvas.coords(self.place2)
            x = coords[0] - cardCoords[0]
            y = coords[1] - cardCoords[1]
            self.canvas.move(self.move_data["object"], x, y)
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

    def move(self, event):
        if (event.x < 100):
            event.x = 100 - abs(event.x-100)
            if(abs(event.x-100) > 10):
                event.x = 100
        if (event.y < 100):
            event.y = 100 - abs(event.y - 100)
            if (abs(event.y - 100) > 10):
                event.y = 100

        if(event.x > 1100):
            event.x = 1100 - abs(event.x-1100)
            if (abs(event.x-1100)>10):
                event.x = 1100
        if (event.y > 600):
            event.y = 600 - abs(event.y - 600)
            if (abs(event.y - 600) > 10):
                event.y = 600

        dx = event.x - self.move_data["x"]
        dy = event.y - self.move_data["y"]

        self.canvas.move(self.move_data["object"], dx, dy)
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y
