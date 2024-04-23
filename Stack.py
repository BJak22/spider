

class Stack:
    def __init__(self, deck, canvas, image):
        self.cards = deck.cards[54:]
        self.id = canvas.create_image(90, 130, image=image, tag="addCards")
