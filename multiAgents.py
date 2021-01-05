from HumanAgent import Agent, raiseNotDefined

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    raiseNotDefined()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

        self.bestAction = " " # for AB/ exp


class AlphaBetaAgent(MultiAgentSearchAgent):
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