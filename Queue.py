from Card import Card


class Queue:
    def __init__(self, x, canvas, card):
        self.CoordX = x
        self.CoordY = 60
        self.Label = canvas.create_rectangle(x, 150, x+90, 60)
        self.cards = list()
        self.lastCard = card
