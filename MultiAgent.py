from collections import Counter
from HumanAgent import Agent
from util import *
from AI_agent import *
import copy
import random

def get_value(gameState, action):
    return 0


class MinimaxAgent(Agent):
    """
    the minimax agent as the LandLord
    """
    # def takeAction()
    def get_action(self, gameState):
        """
        Returns the minimax action from the current gameState using get_value()

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        depth = 1

        # Collect legal moves and successor states
        legalMoves = gameState.get_legal_choices(self.cards)

        # Choose one of the best actions
        successors = [gameState.generateSuccessor(0, action) for action in legalMoves]
        scores = [self.value(nextState , 1, depth-1) for nextState in successors]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]
    
    def value(self, gameState, agentID, depth):
        # terminal case
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction( gameState )

        if not agentID:
            return self.maxValue( gameState, depth-1 )
        else:
            return self.minValue(gameState, agentID, depth)

    # for maxValue(), agent ID = 0
    def maxValue(self, gameState, depth):    
        maxV = -999999
        for action in gameState.getLegalActions( 0 ):
            successor = gameState.generateSuccessor( 0, action )
            maxV = max( maxV, self.value( successor, 1, depth ) )
        return maxV

    # ghost turn, agentID >= 1
    def minValue(self, gameState, agentID, depth):
        minV = 999999
        for action in gameState.getLegalActions( agentID ):
            successor = gameState.generateSuccessor( agentID, action )
            if agentID == gameState.getNumAgents()-1 :
                if depth :
                    minV = min( minV, self.value( successor, 0,  depth) )
                else:
                    minV = min( minV, self.evaluationFunction(successor) )

            elif agentID < gameState.getNumAgents()-1:
                minV = min( minV, self.value( successor, agentID+1, depth ) )

        return minV

class AlphaBetaAgent(AI_agent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.value(gameState, 0, self.depth)

        return self.bestAction
    
    def value(self, gameState, agentID, depth, a=-9999, b=9999):
        # terminal case
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction( gameState )

        if not agentID:
            return self.maxValue( gameState, depth-1, a, b )
        else:
            return self.minValue(gameState, agentID, depth, a, b)

    # for maxValue(), agent ID = 0
    def maxValue(self, gameState, depth, a, b):    
        maxV = -999999
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
        minV = 999999
        for action in gameState.getLegalActions( agentID ):
            successor = gameState.generateSuccessor( agentID, action )
            if agentID == gameState.getNumAgents()-1 :
                if depth :
                    minV = min( minV, self.value( successor, 0,  depth, a, b) )
                else:
                    minV = min( minV, self.evaluationFunction(successor) )
            elif agentID < gameState.getNumAgents()-1:
                minV = min( minV, self.value( successor, agentID+1, depth, a,b) )
            
            if minV < a:
                return minV
            b = min(b, minV)        

        return minV