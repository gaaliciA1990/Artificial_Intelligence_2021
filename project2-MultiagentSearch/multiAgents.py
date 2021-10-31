# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        pacmanSuccessorDirection = successorGameState.getPacmanState().getDirection()
        pacmanDirection = currentGameState.getPacmanState().getDirection()

        "*** YOUR CODE HERE - Completed ***"
        foodReward = 50
        nearFoodReward = 1
        scaredTimeReward = 10
        ghostEncounterPenalty = -50
        stopPenalty = -50
        reversePenalty = -15  # penalty for going in reverse to prevent back and forth loop

        score = successorGameState.getScore()

        ghostDistance = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        closestGhost = float('inf')
        scaredGhostTimer = 0

        # Determine the closest ghost and that ghosts scared status to determine when to run
        for i in range(len(ghostDistance)):
            if ghostDistance[i] < closestGhost:
                closestGhost = ghostDistance[i]
                scaredGhostTimer = newScaredTimes[i]

        # run from the ghosts, unless the timer is active
        if closestGhost <= 1:
            if scaredGhostTimer > 0:
                score += scaredTimeReward
            else:
                score += ghostEncounterPenalty

        foodDistance = [manhattanDistance(newPos, foodPos) for foodPos in newFood]

        # If the length of the foodDistance list is 0 (empty) we won! Return a large number
        if len(foodDistance) == 0:
            return float('inf')

        # Always have the closest food variable to use for maximizing food eating
        closestFood = min(foodDistance)

        # Find the food, move closer to the food and eat the food. This isn't actually being hit when running
        # not sure how we can tell pacman he's eaten the food
        if closestFood == 0:
            score += foodReward
        # If we are near the food, we get a smaller reward based on distance to pellet
        # to encourage movement towards the food
        else:
            score += nearFoodReward / closestFood

        # add penalty for going in reverse when scores are close to each other
        # to avoid back and forth loop.
        if pacmanSuccessorDirection == Directions.REVERSE[pacmanDirection]:
            score += reversePenalty

        # add a penalty for stopping
        if action == 'Stop':
            score += stopPenalty

        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    # This helper method will compute the maximum value in minimax algorithm for pacman
    # Takes the gameState and depth of the tree
    def maxFunction(self, gameState, depth):
        maxValue = float('-inf')    # Value to be returned at the end
        pacmanLegalAction = gameState.getLegalActions(0)

        # If there are no Legal actions or we've reached the end, return the evaluation function
        if (depth == self.depth) or (len(pacmanLegalAction) == 0):
            return self.evaluationFunction(gameState)

        # Find the max value for pacmans action and return it
        for action in pacmanLegalAction:
            tempValue = self.minFunction(gameState.generateSuccessor(0, action), depth, 1)
            if tempValue > maxValue:
                maxValue = tempValue

        return maxValue

    # This helper method will compute the minimum value in minimax algorithm for ghosts
    # Takes the gameState,  depth of the tree and index of the agent
    def minFunction(self, gameState, depth, agentIndex):
        minValue = float('inf')  # Value to be returned at the end
        ghostLegalAction = gameState.getLegalActions(agentIndex)
        ghostCount = gameState.getNumAgents() - 1

        # If there are no Legal actions, return the evaluation function
        if len(ghostLegalAction) == 0:
            return self.evaluationFunction(gameState)
        # Check the ghost action values and return the smallest number for the min branch
        if agentIndex < ghostCount:
            for action in ghostLegalAction:
                tempValue = self.minFunction(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                if tempValue < minValue:
                    minValue = tempValue
            return minValue
        # check the last ghosts action values against max function and return min value
        else:
            for action in ghostLegalAction:
                tempValue = self.maxFunction(gameState.generateSuccessor(agentIndex, action), depth + 1)
                if tempValue < minValue:
                    minValue = tempValue
            return minValue

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

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
        "*** YOUR CODE HERE - Competed with helper functions ***"
        pacmanLegalActions = gameState.getLegalActions(0)  # all the legal actions of pacman.
        maxValue = float('-inf')
        maxAction = None  # one to be returned at the end.

        for action in pacmanLegalActions:  # get the max value from all of it's successors.
            actionValue = self.minFunction(gameState.generateSuccessor(0, action), 0, 1)
            if actionValue > maxValue:  # take the max of all the children.
                maxValue = actionValue
                maxAction = action

        return maxAction  # Returns the final action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
