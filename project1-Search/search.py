# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
  """

    # Using a stack of tuples to track the (location, actions) based on LIFO.
    fringe = util.Stack()

    # previously visited location (nodes) in a list. Holds the location/state
    visitedNodes = []

    # define start state and tracking node
    startState = problem.getStartState()
    startNode = (startState, [])

    # Push the tuples into our start Node for the coordinates and action taken
    fringe.push(startNode)

    while not fringe.isEmpty():
        # check the most recently pushed node in fringe to find the location and action (path)
        state, actions = fringe.pop()

        # Validate we don't expand an already visited node
        if state not in visitedNodes:
            # move the node to a visited node list
            visitedNodes.append(state)
            # print("The state is: " + str(state))

            if problem.isGoalState(state):
                return actions
            else:
                # pull the list of potential successor node
                successors = problem.getSuccessors(state)
                # print("My next move is: " + str(successors))

                # push each successor to fringe
                for successorState, successorAction, successorCost in successors:
                    newAction = actions + [successorAction]
                    newNode = (successorState, newAction)
                    fringe.push(newNode)
    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # Using a queue since we are working FIFO. Stored as (state, action, cost)
    fringe = util.Queue()

    # previously visited location (nodes) in a list
    visitedNodes = []

    startState = problem.getStartState()
    startNode = (startState, [], 0)

    fringe.push(startNode)

    while not fringe.isEmpty():
        # check the first or earliest-pushed node in fringe
        state, actions, cost = fringe.pop()

        # Validate we don't expand an already visited node
        if state not in visitedNodes:
            # add popped node state into visited list
            visitedNodes.append(state)
            # print("My location is: " + str(location))

            if problem.isGoalState(state):
                return actions
            else:
                # list the successor, action and stepCost
                successors = problem.getSuccessors(state)
                # print("My next move is: " + str(successors))

                for successorState, successorAction, successorCost in successors:
                    newAction = actions + [successorAction]
                    newCost = cost + successorCost
                    newNode = (successorState, newAction, newCost)
                    fringe.push(newNode)

    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # Using a priority queue for UCS. We are working FIFO. Stored as (item, cost)
    fringe = util.PriorityQueue()

    # previously expanded nodes in a dictionary for cycle checking. Tuple = (state:cost)
    visitedNodes = {}

    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, action, cost)

    fringe.push(startNode, 0)

    while not fringe.isEmpty():
        # explore the first node in fringe, which should be the cheapest cost
        state, actions, cost = fringe.pop()

        if (state not in visitedNodes) or (cost < visitedNodes[state]):
            # place the popped location (state) into our visited list
            visitedNodes[state] = cost

            if problem.isGoalState(state):
                return actions
            else:
                successors = problem.getSuccessors(state)

                for successorLocation, successorAction, successorCost in successors:
                    newAction = actions + [successorAction]
                    newCost = cost + successorCost
                    newNode = (successorLocation, newAction, newCost)
                    fringe.update(newNode, newCost)

    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Using a priority queue for UCS. We are working FIFO. Stored as (item, cost+heauristic)
    fringe = util.PriorityQueue()

    # store previously visited locations (nodes) in a list of tuples (location, cost)
    visitedNodes = []

    # pull the initial starting location and store this in a node variable
    # holding (location, action, cost)
    startLocation = problem.getStartState()
    startNode = (startLocation, [], 0)

    fringe.push(startNode, 0)

    while not fringe.isEmpty():
        # explore the cheapest node in fringe first (cost + heauristic)
        location, actions, cost = fringe.pop()

        # add location and cost to the visitedNodes list
        visitedNodes.append((location, cost))

        if problem.isGoalState(location):
            return actions
        else:
            # create a list to hold the successor, action and stepCost
            successors = problem.getSuccessors(location)

            # check each successor
            for successorLocation, successorAction, successorCost in successors:
                newAction = actions + [successorAction]
                newCost = problem.getCostOfActions(newAction)
                # print("True cost is = " + str(newCost))
                newNode = (successorLocation, newAction, newCost)

                # verify if the successor has already been visited
                prevVisited = False
                for visited in visitedNodes:
                    # check each visited node tuple
                    prevLocation, prevCost = visited

                    # if successor is previously visited, update bool value of prevVisited
                    if (successorLocation == prevLocation) and (newCost >= prevCost):
                        prevVisited = True

                # if successor is not previously visited, add it to fringe and visited list
                if not prevVisited:
                    fringe.push(newNode, newCost + heuristic(successorLocation, problem))
                    visitedNodes.append((successorLocation, newCost))
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
