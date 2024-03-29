import random
from Card import Card

CardColors = ['spades', 'hearts', 'diamonds', 'clubs']


class Deck:
    def __init__(self, level):
        self.level = level
        self.colors = list()
        self.cards = list()
        # creating deck
        if level != 4:
            self.colors.append(random.choice(CardColors))
            if level == 1:
                # 104 cards = 8*13 - every color is the same on level 1
                i = 0
                while i < 8:
                    i += 1
                    j = 1
                    while j < 14:
                        self.cards.append(Card(self.colors[0], j))
                        j += 1
            if level == 2:
                tmp_color = random.choice(CardColors)
                while self.colors.count(tmp_color) != 0:
                    tmp_color = random.choice(CardColors)
                self.colors.append(tmp_color)
                for color in self.colors:
                    i = 0
                    # 104 cards = 2*4*13 - 2 different colors on level 2
                    while i < 4:
                        i += 1
                        j = 1
                        while j < 14:
                            self.cards.append(Card(color, j))
                            j += 1
        else:
            self.colors = CardColors
            # 104 cards = 4*2*13 - 4 different colors on level 4
            for color in self.colors:
                i = 0
                while i < 2:
                    i += 1
                    j = 1
                    while j < 14:
                        self.cards.append(Card(color, j))
                        j += 1
        random.shuffle(self.cards)

        self.cardsLeft = len(self.cards)


#test = Deck(1)
#print(test.colors)
#test2 = Deck(2)
#print(test2.colors)