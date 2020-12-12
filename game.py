from util import *
import time
import os
import traceback
import sys

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

    def isWinner(self):
        return True if len(self.cards)==0 else False

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action
        """
        raiseNotDefined()

class HumanAgent(Agent):
    def gatAction(self, state):
        choice = input("player %s: please enter your choics:"%(self.name))

        
        return choice






