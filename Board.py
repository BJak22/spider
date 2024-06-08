import copy
import tkinter as tk
from Card import Card
from Card import LabelCard
from Queue import Queue
from Deck import Deck
from Stack import Stack
from state import State
import time
import threading
import csv
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
import joblib
import random

class Board:
    def __init__(self, window, level, player):
        self.last_move = None
        self.second_last_move = None
        self.predictor = joblib.load("solitaire4.0")
        self.player = player
        self.moves = list()
        self.move_list = list()
        self.stop_thread = False
        self.window = window
        if self.player:
            self.window.bind("<Control-z>", self.restoreState)
        self.points = 500

        # reading stats for leaderboard
        f = open("score.txt", 'r')
        self.won = False
        self.beginner_score = int(f.readline())
        self.beginner_time = int(f.readline())
        self.beginner_wins = int(f.readline())
        self.beginner_loses = int(f.readline())
        self.intermediate_score = int(f.readline())
        self.intermediate_time = int(f.readline())
        self.intermediate_wins = int(f.readline())
        self.intermediate_loses = int(f.readline())
        self.expert_score = int(f.readline())
        self.expert_time = int(f.readline())
        self.expert_wins = int(f.readline())
        self.expert_loses = int(f.readline())

        f.close()

        self.firstClick = True

        self.window.geometry("1700x800")
        self.window.resizable(False, False)
        # board with cards
        self.canvas = tk.Canvas(width=1700, height=800, bg="#3ea84a")
        self.canvas.pack()

        self.pointsLabel = self.canvas.create_text(30, 30, text=self.points, font = "TimesNewRoman")
        self.timeLabel = self.canvas.create_text(1660, 30, text="0:00", font="TimesNewRoman")

        # create deck and list of images of cards
        self.deck = Deck(level)
        self.time = 0
        self.level = level
        self.Images = []
        self.colors = ["H", "D", "C", "S"]
        for i in self.colors:
            val = 1
            while val < 14:
                Aux = str(val) + i + ".png"
                self.Images.append(tk.PhotoImage(file=Aux))
                val += 1
        self.Images.append(tk.PhotoImage(file="Back.png"))

        self.stack = Stack(self.deck, self.canvas, self.Images[-1])
        self.cards = list()
        self.hiddenCards = list()
        self.places = list()
        self.stateList = list()

        self.grids = [200, 350, 500, 650, 800, 950, 1100, 1250, 1400, 1550]

        val = 0
        for i in self.grids:
            self.places.append(Queue(i, self.canvas, self.deck.cards[val], val, 30))
            val += 1

        for i in self.places:
            ran = 5
            if i.grid > 3:
                ran -= 1
            for j in range(ran):
                i.HiddenCards.append(self.deck.cards[val])
                val += 1
        # data of object that is moving
        self.empty = tk.Canvas()
        self.move_data = {"object": 0, "x": 0, "y": 0, "startX": 0, "startY": 0, "cards": [],
                          "startPlace": Queue(1, self.empty, None, 11,0),
                          "card": LabelCard(None, "T", 0, None, None, self.Images[-1], 50, 70, -1)}
        self.add_cards("movable")
        if self.player:
            self.move_bind("movable")
            self.add_cards_bind("addCards")
        self.find_possible_moves()
        #self.write_moves()
        if not self.player:
            self.thread2 = threading.Thread(target = self.move_ai, daemon=True)
            self.thread2.start()

    def find_image(self, card):
        ind = self.colors.index(card.color)
        ind = 13*ind + card.value - 1
        return ind
    def add_cards(self, tag):
        val = 0
        for i in self.places:
            for j in i.HiddenCards:
                self.hiddenCards.append(LabelCard(self.window, j.color, j.value, None, self.canvas, self.Images[-1],
                                                  i.CoordX+50, i.CoordY + 70, i.grid))
                i.CoordY += 10
        for i in self.places:
            im_number = self.find_image(i.lastCard)
            self.cards.append(LabelCard(self.window, i.lastCard.color, i.lastCard.value,
                                        tag, self.canvas, self.Images[im_number], i.CoordX + 50, i.CoordY + 70, i.grid))
            val += 1
        for i in self.places:
            for j in self.cards:
                if j.grid == i.grid:
                    i.idList.append(j.id)
            for j in self.hiddenCards:
                if j.grid == i.grid:
                    i.HiddenIdList.append(j.id)
        self.stateList.append(State(self.places, self.cards, self.hiddenCards, self.stack, self.points))


    def move_bind(self, tag):
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.move_start)
        self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.move_stop)
        self.canvas.tag_bind(tag, "<B1-Motion>", self.move)

    def add_cards_bind(self, tag):
        self.canvas.tag_bind(tag, "<ButtonPress-1>", self.add_more_cards)

    def check_if_places_not_empty(self):
        for i in self.places:
            if i.lastCard is None:
                return False
        return True
    def add_more_cards(self, event):
        if len(self.stack.cards) > 0 and self.check_if_places_not_empty():
            self.points -= 1
            val = len(self.deck.cards) - len(self.stack.cards)
            for i in self.places:
                value = self.deck.cards[val].value + 1
                color = self.deck.cards[val].color
                j = len(i.cards) - 1
                i.CoordY = 70 + (i.interspace * (len(i.cards) - 1)) + (10 * len(i.HiddenCards))
                tmpCard = Card(self.deck.cards[val].color, self.deck.cards[val].value)
                i.cards.append(tmpCard)
                i.lastCard = tmpCard
                im_number = self.find_image(tmpCard)
                self.cards.append(LabelCard(self.window, self.deck.cards[val].color, self.deck.cards[val].value,
                                            "movable", self.canvas, self.Images[im_number], i.CoordX + 50, i.CoordY + 90,
                                            i.grid))
                val += 1
            for i in self.places:
                for j in self.cards:
                    if j.grid == i.grid and j.id not in i.idList:
                        i.idList.append(j.id)
            self.stack.cards = self.stack.cards[10:]
            if self.player:
                tk.messagebox.showinfo(title="Information", message=str(len(self.stack.cards)) + "Cards left")
            for i in self.places:
               if self.check_if_completed(i):
                    self.delete_completed(i)
            self.stateList.append(State(self.places, self.cards, self.hiddenCards, self.stack, self.points))
            self.canvas.itemconfig(self.pointsLabel, text=self.points)
        elif len(self.stack.cards) == 0 and self.player:
            tk.messagebox.showinfo(title="Information", message="No cards left!")
        else:
            if self.player:
                tk.messagebox.showinfo(title="Information", message="There should be cards on all of the places!")
        for i in self.places:
            self.add_movable_cards(i)
            self.change_interspace(i)
        self.find_possible_moves()

    def move_ai(self):
        number_of_moves = 0
        counter = 0
        while len(self.moves) != 0:
            if self.stop_thread == True:
                break
            if not self.firstClick:
                time.sleep(2)
            if self.stop_thread == True:
                break
            self.moves.clear()
            self.find_possible_moves()
            counter += 1
            moves1 = list()
            moves2 = list()
            moves3 = list()
            moves4 = list()
            moves5 = list()
            moves6 = list()
            moves7 = list()
            for i in self.moves:
                if i.move_color == 'H':
                    i.move_color = 1
                if i.drop_color == 'H':
                    i.drop_color = 1
                if i.move_color == 'D':
                    i.move_color = 2
                if i.drop_color == 'D':
                    i.drop_color = 2
                if i.move_color == 'S':
                    i.move_color = 3
                if i.drop_color == 'S':
                    i.drop_color = 3
                if i.move_color == 'C':
                    i.move_color = 4
                if i.drop_color == 'C':
                    i.drop_color = 4
                if i.show == 'nothing':
                    i.show = 1
                if i.show == 'new_card':
                    i.show = 2
                if i.show == 'empty_spot':
                    i.show = 3
                color = 0
                if i.move_color == i.drop_color:
                    color = 8
                data = pd.DataFrame({
                    'value': [i.value],
                    #'complete': [i.complete],
                    #'move_color': [i.move_color],
                    #'drop_color': [i.drop_color],
                    'color' : color,
                    'len_from': [i.len_from],
                    'len_to': [i.len_to],
                    'show': [i.show],
                })
                if (self.last_move == None or self.second_last_move == None\
                    or ((i.to_grid != self.last_move.from_grid or i.from_grid != self.last_move.to_grid))\
                        and (i.to_grid != self.second_last_move.from_grid or i.from_grid != self.second_last_move.to_grid)):
                    if self.predictor.predict(data) == 1:
                        moves1.append(i)
                    elif self.predictor.predict(data) == 2:
                        moves2.append(i)
                    elif self.predictor.predict(data) == 3:
                        moves3.append(i)
                    elif self.predictor.predict(data) == 4:
                        moves4.append(i)
                    elif self.predictor.predict(data) == 5:
                        moves5.append(i)
                    elif self.predictor.predict(data) == 6:
                        moves6.append(i)
                    elif self.predictor.predict(data) == 7:
                        moves7.append(i)
            if len(moves7) > 0:
                move = random.choice(moves7)
            elif len(moves6) > 0:
                move = random.choice(moves6)
            elif len(moves5) > 0:
                move = random.choice(moves5)
            elif len(moves4) > 0:
                move = random.choice(moves4)
            elif len(moves3) > 0:
                move = random.choice(moves3)
            elif len(moves2) > 0:
                move = random.choice(moves2)
            elif len(moves1) > 0:
                if (len(self.moves) <= 4) or (counter > 28 and counter < 30):
                    empty = 10
                    if len(self.stack.cards) > 0:
                        if not self.check_if_places_not_empty():
                            for i in self.places:
                                if i.lastCard == None:
                                    empty = i.grid
                                    break
                        else:
                            self.add_more_cards(0)
                        counter = 0
                    if empty == 10:
                        self.moves.clear()
                        self.find_possible_moves()
                        continue
                    else:
                        for i in self.moves:
                            if i.to_grid == empty:
                                move = i
                                break
                move = random.choice(moves1)
            else:
                empty = 10
                if len(self.stack.cards) > 0:
                    if not self.check_if_places_not_empty():
                        for i in self.places:
                            if i.lastCard == None:
                                empty = i.grid
                                break
                    else:
                        self.add_more_cards(0)
                    counter = 0
                else:
                    self.stop_threading()
                    tk.messagebox.showinfo(title="Inforamtion", message="LOST")
                    break
                if empty == 10:
                    continue
                else:
                    for i in self.moves:
                        if i.to_grid == empty:
                            move = i
                            break
            if counter > 28 and counter < 30:
                self.add_more_cards(0)
                empty = 10
                if len(self.stack.cards) > 0:
                    if not self.check_if_places_not_empty():
                        for i in self.places:
                            if i.lastCard == None:
                                empty = i.grid
                                break
                    counter = 0
                if empty == 10:
                    continue
                else:
                    for i in self.moves:
                        if i.to_grid == empty:
                            move = i
                            break
            self.second_last_move = self.last_move
            self.last_move = move
            listOfMovable = self.canvas.find_withtag("movable")
            for i in self.cards:
                if move.from_grid == i.grid and move.value == i.value and i.id in listOfMovable:
                    self.move_data["object"] = self.canvas.find_withtag(i.id)
            self.before_move_procedure()
            self.ai_make_move(move)
            self.move_stop(0)
            number_of_moves += 1
            if len(self.cards) == 0:
                tk.messagebox.showinfo(title="Inforamtion", message="WIN")
            self.moves.clear()
            self.find_possible_moves()
            if number_of_moves == 0:
                self.window.mainloop()
                number_of_moves += 1
            else:
                self.window.update()
            if counter > 50:
                tk.messagebox.showinfo(title="Inforamtion", message="LOST")
                self.stop_threading()
                break

    def ai_make_move(self, move):
        for i in self.move_list:
            label = self.canvas.find_withtag(i)
            self.canvas.moveto(i, self.places[move.to_grid].CoordX - 2, self.places[move.to_grid].CoordY +
                               ((self.move_list.index(i) + 1) * self.places[move.to_grid].interspace))

    def before_move_procedure(self):
        self.move_list.clear()
        if self.firstClick:
            if self.player:
                if self.level == 1:
                    self.beginner_loses +=1
                elif self.level == 2:
                    self.intermediate_loses +=1
                else:
                    self.expert_loses +=1
            self.firstClick = False
            self.startTime = time.time()
            self.thread = threading.Thread(target=self.timer, daemon=True)
            self.thread.start()
            self.save_score()
        ListcardsIds = list()
        for i in self.places:
            ListcardsIds.extend(i.idList)
        cardCoords = self.canvas.coords(self.move_data["object"])
        self.move_data["startX"] = cardCoords[0]
        self.move_data["startY"] = cardCoords[1]
        aux = (int(cardCoords[0]) - 150)
        aux = int(aux / 150)
        cardId = self.move_data["object"][-1]
        self.move_data["startPlace"] = self.places[aux]
        for i in self.cards:
            if cardId == i.id:
                self.move_data["card"] = i
        idList = list()
        if self.check_if_card_is_last():
            self.move_list.append(self.move_data["object"])
            while len(self.canvas.find_above(self.move_data["object"])) != 0:
                self.canvas.tag_raise(self.move_data["object"])
            idList.append(self.move_data["object"])
        else:
            idList.extend(self.canvas.find_overlapping(cardCoords[0], cardCoords[1], cardCoords[0], 700))
            removeList = list()
            checkList = self.canvas.find_withtag("movable")
            for i in idList:
                for j in self.cards:
                    if i == j.id and (j.value > self.move_data["card"].value or i not in checkList):
                        removeList.append(i)
            for i in removeList:
                if i in idList:
                    idList.remove(i)
            for i in idList:
                if i in ListcardsIds:
                    self.move_list.append(i)
        for i in self.cards:
            for j in idList:
                if j == i.id:
                    self.move_data["cards"].append(i)
        if self.move_data["card"] not in self.move_data["cards"]:
            self.move_data["cards"].append(self.move_data["card"])
        # sorting cards, so the list of cards in queue will be in correct order
        self.quickSort(self.move_data["cards"], 0, len(self.move_data["cards"]) - 1)
        self.move_data["cards"].reverse()
        for i in self.move_data["cards"]:
            while len(self.canvas.find_above(i.id)) != 0:
                self.canvas.tag_raise(i.id)
    def move_start(self, event):
        self.move_data["object"] = self.canvas.find_closest(event.x, event.y)
        self.move_data["x"] = event.x
        self.move_data["y"] = event.y
        self.before_move_procedure()

    def partition(self, array, low, high):
        pivot = array[high]

        i = low - 1

        for j in range(low, high):
            if array[j].value <= pivot.value:
                i = i + 1

                (array[i], array[j]) = (array[j], array[i])

        (array[i + 1], array[high]) = (array[high], array[i + 1])

        return i + 1

    def quickSort(self,array, low, high):
        if low < high:
            pi = self.partition(array, low, high)

            self.quickSort(array, low, pi - 1)

            self.quickSort(array, pi + 1, high)

    def drop(self):
        lenOfMoved = len(self.move_data["cards"])
        cardCoords = self.canvas.coords(self.move_data["object"])
        # checking on which place the card is dropped
        aux = (int(cardCoords[0]) - 150)
        aux = int(aux / 150)
        if cardCoords[0] >= 150 and (self.places[aux].lastCard == None or
                    ((self.places[aux].lastCard.value - 1) == self.move_data["cards"][0].value)):
            self.places[aux].CoordY = 60 + (self.places[aux].interspace * (len(self.places[aux].cards))) + (10 * len(self.places[aux].HiddenCards))
            if(self.places[aux] == self.move_data["startPlace"]):
                self.places[aux].CoordY -= self.places[aux].interspace
            else:
                self.points -= 1
            y = self.places[aux].CoordY - cardCoords[1] + 70
            x = 0
            self.to_grid = self.places[aux].grid
            if self.player:
                x = self.places[aux].CoordX - cardCoords[0] + 50
            for i in self.move_list:
                self.canvas.move(i, x, y)
                if self.places[aux].interspace == 15:
                    self.make_cards_closer(self.places[aux])
            self.places[aux].cards.extend(self.move_data["cards"])
            for i in self.move_data["cards"]:
                self.places[aux].idList.append(i.id)

            if self.places[aux].cards[-1] != None:
                self.add_movable_cards(self.places[aux])


            self.places[aux].lastCard = self.move_data["cards"][-1]
            for i in self.move_data["cards"]:
                i.grid = self.places[aux].grid

            if self.check_if_completed(self.places[aux]):
                self.delete_completed(self.places[aux])


            if len(self.move_data["startPlace"].cards) > lenOfMoved:
                for i in self.move_data["cards"]:
                    self.move_data["startPlace"].cards.pop()
                    self.move_data["startPlace"].idList.remove(i.id)
                self.move_data["startPlace"].CoordY -= self.move_data["startPlace"].interspace * lenOfMoved
                self.move_data["startPlace"].lastCard = self.move_data["startPlace"].cards[-1]
                self.add_movable_cards(self.move_data["startPlace"])

            else:
                self.move_data["startPlace"].lastCard = None
                self.move_data["startPlace"].cards.clear()
                self.move_data["startPlace"].idList.clear()
                self.move_data["startPlace"].CoordY = 60
                if len(self.move_data["startPlace"].HiddenCards) > 0:
                    self.show_hidden_cards(self.move_data["startPlace"])
            if self.move_data["startPlace"] != self.places[aux]:
                self.stateList.append(State(self.places, self.cards, self.hiddenCards, self.stack, self.points))
        else:
            x = self.move_data["startX"] - cardCoords[0]
            y = self.move_data["startY"] - cardCoords[1]
            for i in self.move_list:
                self.canvas.move(i, x, y)
            if self.move_data["startPlace"].interspace == 15:
                self.make_cards_closer(self.move_data["startPlace"])

    def make_cards_closer(self, place):
        mov = self.move_list[1:]
        for i in mov:
            self.canvas.move(i, 0, -15)


    def check_if_completed(self, place):
        val = 1
        col = place.lastCard.color
        leng = len(place.cards) -1
        while val < 14 and leng >= 0:
            if place.cards[leng].value != val or place.cards[leng].color != col:
                return False
            val += 1
            leng -= 1
        if val == 14:
            return True
        return False

    def move_stop(self, event):
        if self.move_data["object"] != None:
            self.drop()
            if len(self.cards) > 0:
                for i in self.places:
                    self.change_interspace(i)
            self.canvas.itemconfig(self.pointsLabel, text=self.points)
            if len(self.cards) == 0:
                self.stop_threading()
                if self.player:
                    self.window.unbind("<Control-z>")
                    tk.messagebox.showinfo(title="YOU'VE WON!", message="Congrats :)")
                    if self.level == 1 and (self.points > self.beginner_score):
                        self.beginner_score = self.points
                        self.beginner_time = self.time
                        self.beginner_wins += 1
                        self.beginner_loses -= 1
                    if self.level == 2 and (self.points > self.intermediate_score):
                        self.intermediate_score = self.points
                        self.intermediate_time = self.time
                        self.intermediate_wins += 1
                        self.intermediate_loses -= 1
                    if self.level == 4 and (self.points > self.expert_score):
                        self.expert_score = self.points
                        self.expert_time = self.time
                        self.expert_wins += 1
                        self.expert_loses -= 1
                    self.won = True
                    self.save_score()
            else:
                for i in self.places:
                    self.add_movable_cards(i)
                self.move_data["card"] = self.cards[0]
                self.move_data["cards"].clear()
                self.move_data["object"] = 0
                self.move_data["x"] = 0
                self.move_data["y"] = 0
                self.move_data["startX"] = 0
                self.move_data["startY"] = 0
                self.move_data["Value"] = 0
                self.move_data["startPlace"] = Queue(1, self.empty, None, 11, 0)
                self.moves.clear()
                self.find_possible_moves()


    def check_if_card_is_last(self):
        for i in self.places:
            if i.lastCard != None:
                if self.move_data["card"].id == i.idList[-1]:
                    return True
        return False

    def move(self, event):
        if event.x < 100:
            event.x = 100 - abs(event.x-100)
            if(abs(event.x-100) > 10):
                event.x = 100
        if event.y < 100:
            event.y = 100 - abs(event.y - 100)
            if (abs(event.y - 100) > 10):
                event.y = 100

        if event.x > 1600:
            event.x = 1100 - abs(event.x-1600)
            if (abs(event.x-1600)>10):
                event.x = 1600
        if event.y > 700:
            event.y = 700 - abs(event.y - 700)
            if (abs(event.y - 700) > 10):
                event.y = 700
        for i in self.move_list:
            cardCoords = self.canvas.coords(i)
            dx = event.x - cardCoords[0]
            dy = event.y - cardCoords[1]
            self.canvas.move(i, dx, dy + ((self.move_list.index(i))*30))
    def delete_completed(self, place):
        self.points += 101
        if len(place.cards) == 13:
            newSelfCards = list()
            for i in self.cards:
                if i.id not in place.idList:
                    newSelfCards.append(i)
            for i in place.idList:
                self.canvas.delete(i)
            self.cards = newSelfCards
            place.cards.clear()
            place.idList.clear()
            place.lastCard = None
            if len(place.HiddenCards) > 0:
                self.show_hidden_cards(place)
        else:
            idList = list()
            for i in range(13):
                place.cards.pop()
                x = place.idList.pop()
                self.canvas.delete(x)
                idList.append(x)
            newSelfCards = list()
            for j in self.cards:
                if j.id not in idList:
                    newSelfCards.append(j)
            self.cards = newSelfCards
            place.lastCard = place.cards[-1]

    def add_movable_cards(self, place):
        listOfMovable = list()
        i = len(place.cards) - 1
        val = 0
        if place.lastCard != None:
            val = place.lastCard.value
            while i >= 0 and place.cards[i].value == val \
                    and place.cards[i].color == place.lastCard.color:
                listOfMovable.append(place.idList[i])
                i -= 1
                val += 1
            for i in place.idList:
                self.canvas.dtag(i, "movable")
            for i in listOfMovable:
                self.canvas.addtag_withtag("movable", i)
    def show_hidden_cards(self,place):
        place.lastCard = place.HiddenCards[-1]
        place.cards.append(place.HiddenCards[-1])
        place.idList.append(place.HiddenIdList[-1])
        im = self.find_image(place.lastCard)
        self.canvas.itemconfig(place.HiddenIdList[-1], image=self.Images[im], tag="movable")
        #temporary Card
        auxCard = self.hiddenCards[0]
        for i in self.hiddenCards:
            if i.id == place.HiddenIdList[-1]:
                auxCard = i

        self.cards.append(auxCard)
        place.HiddenCards.pop()
        place.HiddenIdList.pop()
        place.CoordY += 10

    def restoreState(self, event):
        if len(self.stateList) > 1:
            self.stateList.pop()
        if len(self.stateList) >= 1:
            x = self.stateList[-1]
            if x.points + 90 < self.points:
                self.points -= 100
            self.points -= 1
            self.canvas.itemconfig(self.pointsLabel, text=self.points)
            for i in self.places:
                for j in x.places:
                    if i.grid == j.grid and len(i.HiddenCards) != len(j.HiddenCards):
                        for k in i.HiddenIdList:
                            self.canvas.delete(k)
                        i.HiddenCards.clear()
                        newHiddenCards = list()
                        i.lastCard = None
                        i.cards.remove(i.cards[0])
                        for k in self.hiddenCards:
                            if k.grid != i.grid:
                                newHiddenCards.append(k)
                        self.hiddenCards = newHiddenCards
                        for k in j.HiddenCards:
                            i.CoordY = 60 + (10 * len(i.HiddenCards))
                            self.hiddenCards.append(LabelCard(self.window, k.color, k.value,
                                                        None, self.canvas, self.Images[-1], i.CoordX + 50,
                                                        i.CoordY + 70, i.grid))
                            i.HiddenCards.append(k)
                        i.HiddenIdList.clear()
                        for k in self.hiddenCards:
                            if k.grid == i.grid:
                                i.HiddenIdList.append(k.id)

                    if i.grid == j.grid and len(i.cards) != len(j.cards):
                        i.cards.clear()
                        for k in i.idList:
                            self.canvas.delete(k)
                        newCards = list()
                        for k in self.cards:
                            if k.id not in i.idList:
                                newCards.append(k)
                        self.cards = newCards
                        for k in j.cards:
                            im = self.find_image(k)
                            i.CoordY = 60 + (i.interspace * (len(i.cards))) + (
                                        10 * len(i.HiddenCards))
                            self.cards.append(LabelCard(self.window, k.color, k.value,
                                                       "movable", self.canvas, self.Images[im],  i.CoordX + 50,
                                                        i.CoordY + 70, i.grid))
                            i.cards.append(k)
                        i.idList.clear()
                        for k in self.cards:
                            if k.grid == i.grid:
                                i.idList.append(k.id)
                        for k in self.places:
                            if len(k.cards) > 0:
                                k.lastCard = k.cards[-1]
                            else:
                                k.lastCard = None
                    for k in self.places:
                        self.add_movable_cards(k)
            if len(x.stack.cards) > len(self.stack.cards):
                self.stack.cards = x.stack.cards

    def change_interspace(self, place):
        if len(place.cards) > 15 and place.interspace != 15:
            place.interspace = 15
            for i in place.idList:
                mover = place.idList.index(i) * (-15)
                cardCoords = self.canvas.coords(i)
                if len(cardCoords) > 0:
                    x = place.CoordX - cardCoords[0] + 50
                    y = mover
                    self.canvas.move(i, x, y)
        if len(place.cards) < 15 and place.interspace == 15:
            place.interspace = 30
            for i in place.idList:
                mover = place.idList.index(i) * (15)
                cardCoords = self.canvas.coords(i)
                if len(cardCoords) > 0:
                    x = place.CoordX - cardCoords[0] + 50
                    y = mover
                    self.canvas.move(i, x, y)


    def timer(self):
        while True:
            if self.stop_thread:
               break
            time.sleep(1)
            if self.stop_thread:
                break
            tm = int(time.time()-self.startTime)
            min = int(tm/60)
            sec = tm - min*60
            if sec<10:
                sec = "0" + str(sec)
            self.canvas.itemconfig(self.timeLabel, text=str(min) + ":"+str(sec))
            self.time = tm
    def stop_threading(self):
        self.stop_thread = True

    def save_score(self):
        f = open("score.txt", mode='w')
        f.write(str(self.beginner_score)+'\n')
        f.write(str(self.beginner_time) + '\n')
        f.write(str(self.beginner_wins)+'\n')
        f.write(str(self.beginner_loses)+'\n')
        f.write(str(self.intermediate_score)+'\n')
        f.write(str(self.intermediate_time) + '\n')
        f.write(str(self.intermediate_wins)+'\n')
        f.write(str(self.intermediate_loses)+'\n')
        f.write(str(self.expert_score)+'\n')
        f.write(str(self.expert_time) + '\n')
        f.write(str(self.expert_wins)+'\n')
        f.write(str(self.expert_loses)+'\n')
        f.close()

    def find_possible_moves(self):
        mov = self.canvas.find_withtag("movable")
        last = list()
        for i in self.places:
            if i.lastCard != None:
                last.append(i.lastCard.value)
        for i in self.places:
            if i.lastCard != None:
                for j in i.idList:
                    num = i.idList.index(j)
                    tmpLast = last
                    ind = 0
                    while j in mov and ((i.cards[num].value + 1) in tmpLast and i.grid != tmpLast.index(i.cards[num].value + 1)):
                        from_grid = i.grid
                        to_grid = ind + (tmpLast.index(i.cards[num].value + 1))
                        value = i.cards[num].value
                        complete = 0
                        if (self.find_len_of_movable_to(self.places[ind + tmpLast.index(i.cards[num].value + 1)],
                                                        i.cards[num:])) == 13:
                            complete = 1
                        if i.cards[num].color == 'H':
                            move_color = 1
                        elif i.cards[num].color == 'D':
                            move_color = 2
                        elif i.cards[num].color == 'S':
                            move_color = 3
                        if i.cards[num].color == 'C':
                            move_color = 4
                        else:
                            move_color = 0
                        if self.places[ind + tmpLast.index(i.cards[num].value + 1)].lastCard != None:
                            if self.places[ind + tmpLast.index(i.cards[num].value + 1)].lastCard.color == 'H':
                                to_color = 1
                            elif self.places[ind + tmpLast.index(i.cards[num].value + 1)].lastCard.color == 'D':
                                to_color = 2
                            elif self.places[ind + tmpLast.index(i.cards[num].value + 1)].lastCard.color == 'S':
                                to_color = 3
                            if self.places[ind + tmpLast.index(i.cards[num].value + 1)].lastCard.color == 'C':
                                to_color = 4
                        else:
                            to_color = 0
                        len_from = self.find_len_of_movable_from(i, num)
                        len_to = self.find_len_of_movable_to(self.places[ind + tmpLast.index(i.cards[num].value + 1)], i.cards[num:])
                        ind += tmpLast.index(i.cards[num].value+1)+1
                        show = 1
                        if num == 0:
                            if len(i.HiddenCards) == 0:
                                show = 3
                            else:
                                show = 2
                        self.moves.append(
                            Move(from_grid, to_grid, value, complete, move_color, to_color, len_from, len_to, show))
                        tmpLast = tmpLast[tmpLast.index(i.cards[num].value+1)+1:]
            if i.lastCard == None:
                for j in self.places:
                    for k in j.idList:
                        if k in mov:
                            from_grid = j.grid
                            to_grid = i.grid
                            value = j.cards[j.idList.index(k)].value
                            complete = 0
                            move_color = j.cards[j.idList.index(k)].color
                            to_color = 0
                            len_from = self.find_len_of_movable_from(j, j.idList.index(k))
                            len_to = len(j.cards) - j.idList.index(k)
                            show = 1
                            if j.idList.index(k) == 0:
                                if len(j.HiddenCards) == 0:
                                    show = 3
                                else:
                                    show = 2
                            self.moves.append(
                                Move(from_grid, to_grid, value, complete, move_color, to_color, len_from, len_to, show))

    def write_moves(self):
        with open('moves.csv', 'a', encoding='utf-8') as csvfile:
            fieldnames = ["from_grid", "to_grid", "value", "complete", "move_color", "drop_color", "len_from",
                                "len_to", "show"]
            csvwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
            for i in self.moves:
                csvwriter.writerow({"from_grid": i.from_grid, "to_grid" : i.to_grid, "value" : i.value,
                                    "complete" : i.complete, "move_color" : i.move_color,
                                   "drop_color" : i.drop_color, "len_from" : i.len_from, "len_to" : i.len_to,
                                    "show" : i.show})
    def write_signed_move(self, move):
        type_of_move = input("Ocena za ten ruch (1-4): ")
        if int(type_of_move) > 0:
            with open('moves_signed.csv', 'a', encoding='utf-8') as csvfile:
                fieldnames = ["from_grid", "to_grid", "value", "complete", "move_color", "drop_color", "len_from",
                                    "len_to", "show", "type"]
                csvwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
                csvwriter.writerow({"from_grid": move.from_grid, "to_grid" : move.to_grid, "value" : move.value,
                                        "complete" : move.complete, "move_color" : move.move_color,
                                       "drop_color" : move.drop_color, "len_from" : move.len_from, "len_to" : move.len_to,
                                        "show" : move.show, "type": type_of_move})

# find move with you made, function used to sign quality of moves
    def find_made_move(self, to):
        for i in self.moves:
            if i.from_grid == self.move_data["startPlace"].grid and i.to_grid == to:
                return i

    def check_if_will_complete(self, place):
        val = 2
        col = place.lastCard.color
        leng = len(place.cards) - 1
        while val < 14 and leng >= 0:
            if place.cards[leng].value != val or place.cards[leng].color != col:
                return False
            val += 1
            leng -= 1
        if val == 13:
            return True
        return False

    def find_len_of_movable_to(self, place,cards):
        tmpCards = copy.deepcopy(place.cards)
        tmpCards.extend(cards)
        leng = 0
        i = len(tmpCards) -1
        val = 0
        if tmpCards[-1] != None and place.lastCard != None:
            val = tmpCards[-1].value
            while i >= 0 and tmpCards[i].value == val \
                    and tmpCards[i].color == place.lastCard.color:
                leng +=1
                i -= 1
                val += 1
        if leng == 0:
            leng += 1
        return leng

    def find_len_of_movable_from(self, place, ind):
        tmpCards = copy.deepcopy(place.cards[:ind])
        leng = 0
        i = len(tmpCards) -1
        val = 0
        if len(tmpCards) != 0:
            val = tmpCards[-1].value
            while i >= 0 and tmpCards[i].value == val \
                    and tmpCards[i].color == tmpCards[-1].color:
                leng += 1
                i -= 1
                val += 1
        if len(place.HiddenIdList) >0 and len(tmpCards) == 0:
            leng +=1
        return leng

class Move:
    def __init__(self, from_grid, to_grid, value, complete, move_color, drop_color, len_from, len_to, show):
        self.from_grid = from_grid
        self.to_grid = to_grid
        self.value = value
        self.complete = complete
        self.move_color = move_color
        self.drop_color = drop_color
        self.len_from = len_from
        self.len_to = len_to
        self.show = show