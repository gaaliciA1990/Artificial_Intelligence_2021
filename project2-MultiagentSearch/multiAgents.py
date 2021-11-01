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

        # enhanced for loop to populate the distance from each ghost
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

        # Enhanced for loop for determining the distance from each food
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
        legalActions = gameState.getLegalActions(0)  # all the legal actions of pacman.
        maxValue = float('-inf')
        maxAction = None  # one to be returned at the end.

        for action in legalActions:  # get the max value from all of it's successors.
            actionValue = self.minFunction(gameState.generateSuccessor(0, action), 0, 1)
            if actionValue > maxValue:  # take the max of all the children.
                maxValue = actionValue
                maxAction = action

        return maxAction  # Returns the final action

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

    # This helper method will compute the maximum value in minimax algorithm for pacman
    # Takes the gameState and depth of the tree
    def maxFunction(self, gameState, depth):
        maxValue = float('-inf')  # Value to be returned at the end
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


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE - Completed with helper functions ***"
        alpha = float('-inf')  # max best option on path to root
        beta = float('inf')  # min best option on path to root
        bestMove = None
        legalActions = gameState.getLegalActions(0)

        for action in legalActions:
            actionValue = self.minFunction(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if alpha < actionValue:
                alpha = actionValue
                bestMove = action

        return bestMove

    # This helper method will compute the minimum value in minimax algorithm for ghosts
    # Takes the gameState,  depth of the tree and index of the agent
    def minFunction(self, gameState, agentIndex, depth, alpha, beta):
        """ For Min agents best move """
        ghostLegalAction = gameState.getLegalActions(agentIndex)
        minValue = float('inf')
        ghostCount = gameState.getNumAgents() - 1

        # Check if there are no legal actions. If true, then return our evaluation value
        if len(ghostLegalAction) == 0:
            return self.evaluationFunction(gameState)

        # check each ghost agent for the minimum value when the index is less than the ghost count.
        for action in ghostLegalAction:
            if agentIndex < ghostCount:
                minValue = min(minValue, self.minFunction(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth, alpha, beta))
            else:  # the last ghost HERE
                minValue = min(minValue, self.maxFunction(gameState.generateSuccessor(agentIndex, action), depth + 1, alpha, beta))

            # Check if min value is less alpha. If yes, prune the tree by returning minValue
            if minValue < alpha:
                return minValue

            # Update beta value to smallest value
            beta = min(beta, minValue)

        return minValue

    # This helper method will compute the maximum value in minimax algorithm for pacman
    # Takes the gameState and depth of the tree
    def maxFunction(self, gameState, depth, alpha, beta):
        """For Max agents best move"""
        pacmacLegalAction = gameState.getLegalActions(0)
        maxValue = float('-inf')

        if depth == self.depth or len(pacmacLegalAction) == 0:
            return self.evaluationFunction(gameState)

        # check pacman's best option by evaluating the max option from the min node.
        for action in pacmacLegalAction:
            maxValue = max(maxValue, self.minFunction(gameState.generateSuccessor(0, action), 1, depth, alpha, beta))

            # Check if max value is greater than beta. If yes, prune the tree by returning maxValue
            if maxValue > beta:
                return maxValue

            # Update alphs value to largest value
            alpha = max(alpha, maxValue)

        return maxValue


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
        "*** YOUR CODE HERE - Completed with helper functions ***"
        pacmanLegalAction = gameState.getLegalActions(0)  # all the legal actions of pacman.
        maxValue = float('-inf')  # initialize our maxValue for comparison with value of action returned
        bestMove = None  # action returned at the end.

        # Determine the best action to take from the expectimax algorithm
        for action in pacmanLegalAction:
            actionValue = self.minFunction(gameState.generateSuccessor(0, action), 1, 0)
            if actionValue > maxValue:
                maxValue = actionValue
                bestMove = action

        return bestMove

    # This helper method will compute the minimum value in Expectimax algorithm for ghosts
    # Takes the gameState,  depth of the tree and index of the agent
    def minFunction(self, gameState, agentIndex, depth):
        numGhostActions = len(gameState.getLegalActions(agentIndex))  # total number of ghost actions
        ghostLegalActions = gameState.getLegalActions(agentIndex)  # legal actions a ghost can take
        ghostCount = gameState.getNumAgents() - 1  # number of ghosts in the game
        sumOfActions = 0  # variable for holding the sum of actions taken

        # Check if there are no legal actions. If true, then return our evaluation value
        if numGhostActions == 0:  # No Legal actions.
            return self.evaluationFunction(gameState)

        # For each ghost, take the sum of it's actions and return the average for determining the route
        # with the best probability for success
        if agentIndex < ghostCount:
            for action in ghostLegalActions:
                sumOfActions += self.minFunction(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth)
            return sumOfActions / float(numGhostActions)
        else:
            for action in ghostLegalActions:
                sumOfActions += self.Max_Value(gameState.generateSuccessor(agentIndex, action), depth + 1)
            return sumOfActions / float(numGhostActions)

    # This helper method will compute the maximum value in Expectimax algorithm for pacman
    # Takes the gameState and depth of the tree
    def Max_Value(self, gameState, depth):
        pacmanLegalAction = gameState.getLegalActions(0)  # legal actions pacman can take
        maxValue = float('-inf')  # Value to be returned at the end

        # If there are no Legal actions or we've reached the end, return the evaluation function
        if (depth == self.depth) or (len(pacmanLegalAction) == 0):
            return self.evaluationFunction(gameState)

        # Find the max value for pacmans action and return it
        for action in pacmanLegalAction:
            tempValue = self.minFunction(gameState.generateSuccessor(0, action), 1, depth)
            if tempValue > maxValue:
                maxValue = tempValue

        return maxValue


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Reworked the whole approach to take into consideration the larger food
    pellets and inverse the sum of the closest food and large food distances. Added the
    the score here to the current gameState score and subtracted the remaining
    food count from the score. Also optimized to the solution for finding the manhattan distance
    """
    "*** YOUR CODE HERE ***"
    ghostState = currentGameState.getGhostStates()  # all the ghost states
    ghostCount = currentGameState.getNumAgents()  # number of ghosts
    pacmanPosition = currentGameState.getPacmanPosition()  # pacman position
    food = (currentGameState.getFood()).asList()  # get all the food as list.
    largeFood = currentGameState.getCapsules()  # get all the large foods.
    foodCount = len(food)  # total food items in the maze
    largeFoodCount = len(largeFood)  # total larger food (timer) items in the maze
    score = currentGameState.getScore()  # initializing current game score to current gamestate score.
    ghostEncounterPenalty = -10000  # penalty for being near a ghost

    # Feature 1 no of Legalactions: Not working well
    # state_score += len(currentGameState.getLegalPacmanActions())/40.0

    ghostDistance = float('inf')
    # Determine the distances from ghosts if exists
    if ghostCount > 1:
        for ghost in ghostState:
            tempGhostDist = manhattanDistance(pacmanPosition, ghost.getPosition())
            if tempGhostDist < ghostDistance:
                ghostDistance = tempGhostDist
        if ghostDistance <= 1:
            return ghostEncounterPenalty
        score -= 1.0 / ghostDistance

    # Find the current food position
    currentFood = pacmanPosition
    for pellet in food:
        closestFood = min(food, key=lambda x: manhattanDistance(x, currentFood))
        score += 1.0 / (manhattanDistance(currentFood, closestFood))
        currentFood = closestFood
        food.remove(closestFood)

    # Feature 4 capsule positions
    currentLargeFood = pacmanPosition
    for largePellet in largeFood:
        closestLargePellet = min(largeFood, key=lambda x: manhattanDistance(x, currentLargeFood))
        score += 1.0 / (manhattanDistance(currentLargeFood, closestLargePellet))
        currentLargeFood = closestLargePellet
        largeFood.remove(closestLargePellet)

    # subtract the remaining food and largeFood counts times a penalty coefficient from the total score
    score -= 6 * (foodCount + largeFoodCount)

    return score


# Abbreviation
better = betterEvaluationFunction
