

class Queue:
    def __init__(self, x, canvas, card, grid, interspace):
        self.CoordX = x
        self.CoordY = 60
        self.Label = canvas.create_rectangle(x, 150, x+90, 60)
        self.cards = list()
        self.cards.append(card)
        self.grid = grid
        self.lastCard = card
        self.idList = list()
        self.HiddenCards = list()
        self.HiddenIdList = list()
        self.interspace = interspace
