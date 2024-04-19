

class Stack:
    def __init__(self, deck, canvas):
        self.cards = deck.cards[54:]
        self.id = canvas.create_rectangle(40, 60, 100, 120, fill="white", tag="addCards")
