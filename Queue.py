from Card import Card


class Queue:
    def __init__(self):
        self.cards = list()
        self.lastCard = self.cards[-1]