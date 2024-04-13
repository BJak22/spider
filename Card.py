import tkinter as tk


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value


class LabelCard(Card,):
    def __init__(self, window, color, value, tag, canvas, image,coordX, coordY):
        Card.__init__(self, color, value)
        self.id = canvas.create_image(coordX, coordY, image=image, tags=tag)
