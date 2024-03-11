import tkinter as tk


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value


class LabelCard(Card):
    def __init__(self, window, color, value, tag, canvas):
        Card.__init__(self, color, value)
        canvas.create_rectangle(10, 10, 100, 100, fill="white", tags=tag)
