from collections import Counter
from HumanAgent import Agent
import copy
import random
from gameData import *

card_utility = {'3':-5, '4':-4, '5':-3, '6':-2, '7':-1, '8':0, '9':1, '10':2, 'J':3, 'Q':4, 'K':5, 'A':6, '2':7, "x":8, "X":9}

class MinimaxAgent(Agent):
    """
    the minimax agent as the LandLord
    """
    def takeAction(self, gameState):
        print("MiniMax Lord!")
        print("before: ", self.cards)
        cards_out = self.getAction(gameState)
        print("cards_out: ", cards_out)

        # take action
        if cards_out != [] and cards_out!= None:
            # update gameState
            gameState.last_turn = self.name
            gameState.cards_out = cards_out
            print("this round player %s take out:"%(self.name), cards_out)
        
            # remove cards in both card_dic
            for card_out in cards_out:
                self.cards.remove(card_out)
                # remove the cards in huase
                for card in gameState.colored_card_dic[self.name]:
                    if card[-1] == card_out[-1]:
                        gameState.colored_card_dic[self.name].remove(card)
                        break

        print("after: ",self.cards)
        # return the remaining cards
        return self.cards

        
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using evaluationFunction()
        """
        self.depth = 1
        legalMoves = gameState.getLegalActions( 0 )
        if legalMoves == []:
            return []

        # Choose one of the best actions
        successors = [gameState.generateSuccessor(0, action) for action in legalMoves]
        scores = [self.value(nextState , 1, self.depth-1) for nextState in successors]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) 
        # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, gameState):
        """ evaluating the current state """
        if gameState.lordWin():
            return 999
        if gameState.farmerWin():
            return -999
        lord_value = sum(card_utility[c]for c in self.cards)-len(self.cards)
        farmer1_value = sum( card_utility[c]for c in gameState.card_dic[gameState.players[1]])
        farmer2_value = sum(card_utility[c]for c in gameState.card_dic[gameState.players[2]])

        return 20+lord_value-farmer1_value-farmer2_value

    
    def value(self, gameState, agentID, depth):
        if gameState==None:
            return float('-inf')
        # terminal case
        if gameState.farmerWin() or gameState.lordWin():
            return self.evaluationFunction( gameState )

        if not agentID:
            # agentID = 0: lord wants max value
            return self.maxValue(gameState, depth-1 )
        else:
            return self.minValue(gameState, agentID, depth)

    # for maxValue(), agent ID = 0
    def maxValue(self, gameState, depth):    
        maxV = -9999
        for action in gameState.getLegalActions( 0 ):
            successor = gameState.generateSuccessor( 0, action )
            maxV = max( maxV, self.value( successor, 1, depth ) )
        return maxV

    # ghost turn, agentID >= 1
    def minValue(self, gameState, agentID, depth):
        minV = 9999
        for action in gameState.getLegalActions( agentID ):
            successor = gameState.generateSuccessor( agentID, action )
            if agentID == 2 :
                if depth :
                    minV = min( minV, self.value( successor, 0,  depth) )
                else:
                    minV = min( minV, self.evaluationFunction(successor) )

            elif agentID < 2:
                minV = min( minV, self.value( successor, agentID+1, depth ) )

        return minV

class AlphaBetaAgent(MinimaxAgent):
    """
    Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        self.bestAction=[]
        self.depth = 1
        self.value(gameState, 0, self.depth)

        return self.bestAction
    
    def value(self, gameState, agentID, depth, a=-9999, b=9999):
        if gameState==None:
            print("gameState is None!!")
            return float('-inf')
        # terminal case
        if gameState.farmerWin() or gameState.lordWin():
            return self.evaluationFunction( gameState )

        if not agentID:
            # lord
            return self.maxValue( gameState, depth-1, a, b )
        else:
            return self.minValue(gameState, agentID, depth, a, b)

    # for maxValue(), agent ID = 0
    def maxValue(self, gameState, depth, a, b):    
        maxV = -9999
        for action in gameState.getLegalActions( 0 ):
            successor = gameState.generateSuccessor( 0, action )
            newV = self.value( successor, 1, depth, a, b )
            if newV > maxV:
                maxV = newV
                if depth==self.depth-1:
                    self.bestAction = action
            
            if maxV > b:
                return maxV
            a = max(a, maxV)
        return maxV

    # ghost turn, agentID >= 1
    def minValue(self, gameState, agentID, depth, a, b):
        minV = 9999
        for action in gameState.getLegalActions( agentID ):
            successor = gameState.generateSuccessor( agentID, action )
            if agentID == 2 :
                if depth :
                    minV = min( minV, self.value( successor, 0,  depth, a, b) )
                else:
                    minV = min( minV, self.evaluationFunction(successor) )
            elif agentID < 2:
                minV = min( minV, self.value( successor, agentID+1, depth, a,b) )

            if minV < a:
                return minV
            b = min(b, minV)

        return minV