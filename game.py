import time
import os
import traceback
import sys
import inspect

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, name, cards, isLord):
        self.name = name
        self.cards = cards
        self.isLord = isLord

    def getName(self):
        return self.name

    def isWinner(self):
        return True if len(self.cards)==0 else False

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action
        """
        raiseNotDefined()

    # update leagal cards
    def updateCards(self, cards_out):
        for card_out in cards_out:
            for card in self.cards:
                if card[2:] == str(card_out):
                    self.cards.remove(card)

    def takeAction(self, state):
        action = self.getAction(state)
        if action == None:
            return self.cards
        else:
            self.updateCards(action)
            return self.cards


class HumanAgent(Agent):
    def getAction(self, state):
        choice = input("player %s: \nplease enter your card choices in ONE LINE:"%(self.name))
        cards_out = choice.split()
        # if pass
        if cards_out == []:
            return None

        # check if input valid
        # if not recurse
        print("Your choice: ", cards_out)
        for card_out in cards_out:
            find = False
            for card in self.cards:
                if card[1:] == str(card_out) or card == card_out:
                    self.cards.remove(card)
                    find = True
            if not find:
                print("invalid card choice!! Enter again!!\n") 
                return self.getAction(state)

        return cards_out


######################## helper function ##############################

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)






