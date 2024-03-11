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
        self.move_data = {"object": None, "x": 0, "y": 0}
        self.add_cards("movable")
        self.bind_tags("movable")
        self.window.mainloop()

    def add_cards(self, tag):
            """
            Create example objects with given tag
            :param tag: str
            :return: None
            """
            self.card = LabelCard(self.window, "spades", 1, tag, self.canvas)

    def bind_tags(self, tag):
            """
            Binding the given tag to events that correspond to drag and drop action
            :param tag: str
            :return: None
            """
            self.canvas.tag_bind(tag, "<ButtonPress-1>", self.move_start)
            self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.move_stop)
            self.canvas.tag_bind(tag, "<B1-Motion>", self.move)

    def move_start(self, event):
            """
            Method that gets called whenever the drag and drop action starts
            :param event: tk.Event
            :return: None
            """
            self.move_data["object"] = self.canvas.find_closest(event.x, event.y)[0]
            self.move_data["x"] = event.x
            self.move_data["y"] = event.y
            print(event.x)
            self.canvas.tag_raise(self.move_data["object"])

    def move_stop(self, event):
            """
            Method that gets called whenever the drag and drop action finishes
            :param event: tk.Event
            :return: None
            """
            self.move_data["object"] = None
            self.move_data["x"] = 0
            self.move_data["y"] = 0

    def move(self, event):
            """
            Method that gets called while the drag and drop action continues
            :param event: tk.Event
            :return: None
            """

            if (event.x < 10):
                event.x = - event.x
                if(event.x > 10):
                    event.x = 90
            if (event.y < 10):
                event.y = - event.y
                if (event.y > 10):
                    event.y = 90

            if(event.x > 1100):
                event.x = 1100 - abs(event.x-1100)
                if (abs(event.x-1100)>10):
                    event.x = 1100
            if (event.y > 600):
                event.y = 600 - abs(event.y - 600)
                if (abs(event.y - 600) > 10):
                    event.y = 600
            print(event.x)

            dx = event.x - self.move_data["x"]
            dy = event.y - self.move_data["y"]

            self.canvas.move(self.move_data["object"], dx, dy)
            self.move_data["x"] = event.x
            self.move_data["y"] = event.y
