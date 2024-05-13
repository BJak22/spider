

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
        self.number = 0


class LabelCard(Card):
    def __init__(self, window, color, value, tag, canvas, image,coordX, coordY, grid):
        Card.__init__(self, color, value)
        self.id = canvas.create_image(coordX, coordY, image=image)
        if tag != None:
            canvas.itemconfig(self.id, tag=tag)
        self.grid = grid