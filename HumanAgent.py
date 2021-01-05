import time
import os
import traceback
import sys
import inspect
from collections import Counter

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
        The Agent will receive a GameState,
        it must take an action 
        and return the remaining cards
        """
        raiseNotDefined()
    
    def getAction(self, state):
        raiseNotDefined()

    # update leagal cards
    # def updateCards(self, cards_out):
    #     copy_cards=self.cards
    #     for card_out in cards_out:
    #         for card in self.cards:
    #             if (card[1:] == card_out) or (card == card_out):
    #                     copy_cards.remove(card)
    #                     break
    #     self.cards=copy_cards

    # def takeAction(self, state):
        # action = self.getAction(state)
        # if action == None:
        #     return self.cards
        # else:
        #     self.updateCards(action)
        #     return self.cards


class HumanAgent(Agent):
    def takeAction(self, state):
        # active
        # to make sure you have the cards you hand out
        while True:
            choice = input("player %s: \nplease enter your card choices in ONE LINE:"%(self.name))
            cards_out = choice.split()
            # if pass
            if cards_out == []:
                return self.cards

            # check if input valid
            # if not, recurse
            cur_cards = self.cards.copy()
            print("Your choice: ", cards_out)

            # check if the chosen cards exist
            for card_out in cards_out:
                find = False
                for card in cur_cards :
                    if (card[1:] == card_out) or (card == card_out):
                        cur_cards.remove(card)
                        find = True
                        break
                if not find:
                    print("invalid card choice!! no card `%s` available!! Please enter again!!\n"%card_out) 
                    print("available cards: ", self.cards)
                    #continue

            # check if the action is leagal
            legal = self.checkAction(state.cards_out, cards_out, (state.last_turn==self.name))
            if not legal:
                print("invalid card choice!! make sure you follow the rules!!\n") 
                print("In last turn, %s puts out "%(state.last_turn), (state.cards_out)) 
            
            if find and legal:
                state.cards_out=cards_out
                #print("this round player %s take out"%(self.name),cards_out)
                state.last_turn=self.name
                self.cards = cur_cards
                return self.cards

    def checkAction(self, last_cards, my_cards, is_active):
        """ given `last_cards` from the other, check if `my_cards` are leagal """
        # wang_zha
        if last_cards==['x', 'X']: return False
        
        # default as cards with colors
        
        # others
        # func=[dan_pai,two,three,three_plus_one,three_plus_two,dan_lian,er_lian,san_lian]
        priority = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, '0':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, "x":13, "X":14}
        otherCards = Counter() 
        for card_with_color in last_cards:
            otherCards[card_with_color[-1]]+=1
        
        myCards = Counter()
        for card_with_color in my_cards:
            myCards[card_with_color[-1]]+=1

        # dan_pai
        if len(my_cards)==1:
            if is_active: 
                return True
            elif len(last_cards)==1 and  priority[my_cards[0]] > priority[last_cards[0]]: 
                return True
            else: 
                return False
        
        # two
        if len(my_cards)==2 and (my_cards[0]==my_cards[1]):
            if is_active: 
                return True
            elif len(last_cards)==1 and  priority[my_cards[0]] > priority[last_cards[0]]: 
                return True
            else: 
                return False
        
        return True
        
            


######################## helper function ##############################

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)






