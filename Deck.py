import random
from Card import Card
import secrets


class Deck:
    def __init__(self, level):
        CardColors = ['S', 'H', 'D', 'C']
        BlackColors = ['S', 'C']
        RedColors = ['H', 'D']
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
                if self.colors[0] in BlackColors:
                    CardColors.remove("S")
                    CardColors.remove("C")
                else:
                    CardColors.remove("H")
                    CardColors.remove("D")
                self.colors.append(random.choice(CardColors))
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
        secrets._sysrand.shuffle(self.cards)

        self.cardsLeft = len(self.cards)
        print(self.cardsLeft)


#test = Deck(1)
#print(test.colors)
#test2 = Deck(2)
#print(test2.colors)