import copy

class State:
    def __init__(self, places, cards, hiddenCards, stack, points):
        self.cards = copy.deepcopy(cards)
        self.hiddenCards = copy.deepcopy(hiddenCards)
        self.places = list()
        for i in places:
            self.places.append(copy.deepcopy(i))
        self.stack = copy.deepcopy(stack)
        self.points = points