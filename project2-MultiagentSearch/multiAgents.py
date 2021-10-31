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
        max_result = Directions.STOP
        pacmanIndex = 0 # The index for pacman is 0.
        actions = gameState.getLegalActions(pacmanIndex) # The legal actions pacman can take.
        maxValue = -100000  # maxVale set to the negative infinity for Minimax algorithm.

        # Terminal test determine if we've finished the game.
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Loop to generate successors.
        for action in actions:
            # Generate next action from non-Stop legal actions
            if action != Directions.STOP:
                # Generate successor for the pacman using action from actions.
                nextState = gameState.generateSuccessor(pacmanIndex, action)

                # Minimize next agent
                ghostIndex = pacmanIndex + 1
                value = self.minFunction(nextState, depth, ghostIndex)

                # Check if value is greater than negative infinity.
                if value > maxValue:  # and action!= Directions.STOP:
                    # Update value of negative infinity
                    maxValue = max(value, maxValue)
                    # Update the action taken by max-player.
                    max_result = action
            # Return action taken for depth being 1.
        return (maxValue, max_result)[depth == 1]

    # This helper method will compute the minimum value in minimax algorithm for ghosts
    # Takes the gameState and depth of the tree
    def minFunction(self, gameState, depth, agentIndex):
        value = 1000000
        # Ghost actions denotes legal action the ghost agent can take.
        ghost_actions = gameState.getLegalActions(agentIndex)
        # lbound denotes the positive inifinity value of MinMax algorithm.
        lbound = 100000
        # agent_count dentoes the total number of enemy agents in game.
        agent_count = gameState.getNumAgents()

        # Terminal test to check if the state is terminal state so as to cut-off.
        if gameState.isLose():
            return self.evaluationFunction(gameState)

        # Loop for every action in legal ghost/agent actions.
        for action in ghost_actions:
            # Remove action from legal actions according to question.
            if action != Directions.STOP:
                next_node = gameState.generateSuccessor(agentIndex, action)
                # Decrement the agent_count to check if ghost/agent left.
                if agentIndex == agent_count - 1:
                    # Check if leaf node reached.
                    if depth == self.depth:
                        value = self.evaluationFunction(next_node)
                    # Else call max_fun to maximize value in next ply.
                    else:
                        value = self.maxFunction(next_node, depth + 1)
                else:
                    # For remaining ghosts, minimize the value.
                    value = self.minFunction(next_node, depth, agentIndex + 1)
            # Update the value of positive infinity
            if value < lbound:  # and action!= Directions.STOP:
                lbound = min(value, lbound)
                min_result = action
        return lbound

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
        "*** YOUR CODE HERE - Competed ***"
        max_result = self.maxFunction(gameState, 0)

        return max_result

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