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
    # Using a stack for we are working LIFO.
    fringe = util.Stack()

    # previously visited nodes in a list. Stored as (state, action)
    visitedNodes = []

    # define start state and tracking node
    startState = problem.getStartState()
    startNode = (startState, [])

    fringe.push(startNode)

    while not fringe.isEmpty():
        # check the most recently pushed node in fringe
        currState, actions = fringe.pop()
        if startState not in visitedNodes:
            # move the node to a visited node list
            visitedNodes.append(currState)
            if problem.isGoalState(currState):
                return actions
            else:
                # pull the list of potential successor node
                successors = problem.getSuccessors(currState)

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

    # previously visited nodes in a list
    visitedNodes = []

    startState = problem.getStartState()
    startNode = (startState, [], 0)

    fringe.push(startNode)

    while not fringe.isEmpty():
        # check the first or earliest-pushed node in fringe
        currState, actions, currCost = fringe.pop()
        if currState not in visitedNodes:
            # add popped node state into visited list
            visitedNodes.append(currState)
            if problem.isGoalState(currState):
                return actions
            else:
                # list the successor, action and stepCost
                successors = problem.getSuccessors(currState)
                for successorState, successorAction, successorCost in successors:
                    newAction = actions + [successorAction]
                    newCost = currCost + successorCost
                    newNode = (successorState, newAction, newCost)
                    fringe.push(newNode)

    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # Using a priority queue for UCS. We are working FIFO. Stored as (item, cost)
    fringe = util.PriorityQueue()

    # previously expanded state in a dictionary for cycle checking. (state:cost)
    visitedNodes = {}

    startState = problem.getStartState()
    startNode = (startState, [], 0) # (state, action, cost)

    fringe.push(startNode, 0)

    while not fringe.isEmpty():
        # explor the first node in fringe, which should be the cheapest cost
        currState, actions, currCost = fringe.pop()
        if (currState not in visitedNodes) or (currCost < visitedNodes[currState]):
            # place the popped state in our visited list
            visitedNodes[currState] = currCost
            #TODO: Finish this code

    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
