
class State:
    def __init__(self, places, fromGrid, toGrid, action):
        # action: 0 - start game ; 1 - move; 2 - add cards
        self.action = action
        self.fromGrid = fromGrid
        self.toGrid = toGrid
        self.FromIdList = list()
        self.ToIdList = list()
        self.FromGrid_len_showed = list()
        self.ToGrid_len_hidden = list()
        self.FromHiddenIdList = list()
        self.ToHiddenIdList = list()
        if action == 0:
            for i in places:
                for j in i.idList:
                    self.FromIdList.append(j)
                for j in i.HiddenIdList:
                    self.FromHiddenIdList.append(j)
