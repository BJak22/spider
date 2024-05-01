import copy

class State:
    def __init__(self, places, cards, hiddenCards, stack):
        self.cards = copy.deepcopy(cards)
        self.hiddenCards = copy.deepcopy(hiddenCards)
        self.places = list()
        for i in places:
            self.places.append(copy.deepcopy(i))