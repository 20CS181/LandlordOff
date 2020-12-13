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
        return True if self.cards==[] else False

    def takeAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action
        """
        raiseNotDefined()

    # update leagal cards
    def updateCards(self, cards_out):
        for card_out in cards_out:
            for card in self.cards:
                if (card[1:] == card_out) or (card == card_out):
                        self.cards.remove(card)
                        break

    # def takeAction(self, state):
        # action = self.getAction(state)
        # if action == None:
        #     return self.cards
        # else:
        #     self.updateCards(action)
        #     return self.cards


class HumanAgent(Agent):
    def takeAction(self, state):
        while True:
            choice = input("player %s: \nplease enter your card choices in ONE LINE:"%(self.name))
            cards_out = choice.split()
            # if pass
            if cards_out == []:
                return self.cards

            # check if input valid
            # if not, recurse
            cur_cards = self.cards[:]
            print("Your choice: ", cards_out)
            for card_out in cards_out:
                find = False
                for card in cur_cards:
                    if (card[1:] == card_out) or (card == card_out):
                        cur_cards.remove(card)
                        find = True
                        break
                if not find:
                    print("invalid card choice!! no card `%s` available!! Please enter again!!\n"%card_out) 
                    print("available cards: ", self.cards)
                    continue
            if find:

                self.cards = cur_cards
                return self.cards
            


######################## helper function ##############################

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)





