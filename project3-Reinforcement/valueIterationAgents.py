# valueIterationAgents.py
# -----------------------
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

import mdp, util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Extract all the states start with the value of zero
        self.values = util.Counter()  # A Counter is a dict with default 0
        states = self.mdp.getStates()  # get all States from our mdp function

        # Update each state with the new value in newValue.
        for i in range(0, self.iterations):
            newValue = util.Counter()
            for state in states:
                action = self.getAction(state)
                # Pick the best action using the policy.
                if action is not None:
                    # Get the value from the state, using the maximum utility from the best q-state.
                    newValue[state] = self.getQValue(state, action)

            self.values = newValue

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.

          Q*(s,a) = sum[s']T(s,a,s')[R(s,a,s') + Y(V_{k}(s'))
        """
        qValue = 0  # total variable for return the qValue
        transitionStateProb = self.mdp.getTransitionStatesAndProbs(state, action)

        for tranStateProb in transitionStateProb:
            tState = tranStateProb[0]  # pull the first transition state from our list
            probability = tranStateProb[1]  # extract the probability from our list
            reward = self.mdp.getReward(state, action, tState)  # get the reward value
            value = self.getValue(tState)  # get the Value of our tState

            # calculate the accumulative qValue based on extracted variables
            qValue += probability * (reward + self.discount * value)

        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.

          V_{k+1}(s) = max[a]Q*(s,a)
        """

        if self.mdp.isTerminal(state):
            return None
        else:
            actions = self.mdp.getPossibleActions(state)  # Get all of the possible actions for the given state
            maxValue = self.getQValue(state, actions[0])  # Set the max QValue based on state and the first action
            maxAction = actions[0]  # set our max action to the first action in our list, updated as we solve

            # loop through our list of actions and determine which value returned
            # is max and store the action associated with that qValue
            for action in actions:
                value = self.getQValue(state, action)
                if maxValue <= value:
                    maxValue = value
                    maxAction = action

        return maxAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        states = self.mdp.getStates()  # get all states
        numStates = len(states)  # get the total number of states

        for i in range(self.iterations):
            state = states[i % numStates]  # set the state to the modulus of the state at i
            # check the state is not terminal and determine the max value
            if not self.mdp.isTerminal(state):
                maxValues = []
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    qValue = self.computeQValueFromValues(state, action)
                    maxValues.append(qValue)
                self.values[state] = max(maxValues)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        priorityQ = util.PriorityQueue()
        predecessors = {}
        states = self.mdp.getStates()

        # determine the next states
        for state in states:
            # check the state is not terminal, else skip
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    tranStatesProbs = self.mdp.getTransitionStatesAndProbs(state, action)
                    for statePrime, probability in tranStatesProbs:
                        if statePrime in predecessors:
                            # add the next state (s') to the predecessor set for tracking
                            predecessors[statePrime].add(state)
                        else:
                            # create a new set with the state inside
                            predecessors[statePrime] = {state}

        # populate the priority queue with the state and difference value
        for state in states:
            if not self.mdp.isTerminal(state):
                values = []
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    qValue = self.computeQValueFromValues(state, action)
                    values.append(qValue)
                # find the difference
                diff = abs(max(values) - self.values[state])
                priorityQ.update(state, - diff)     # add the state and negative difference to the priorityQ

        # Conduct the value iteration
        for i in range(self.iterations):
            # if the priority queue is empty, break from for loop
            if priorityQ.isEmpty():
                break
            tempState = priorityQ.pop()
            if not self.mdp.isTerminal(tempState):
                values = []
                actions = self.mdp.getPossibleActions(tempState)
                for action in actions:
                    qValue = self.computeQValueFromValues(tempState, action)
                    values.append(qValue)
                # update values variable declared in ValueIteration class
                # with max values from our calculation here
                self.values[tempState] = max(values)

            # conduct value iteration for predecessor states
            for pred in predecessors[tempState]:
                if not self.mdp.isTerminal(pred):
                    values = []
                    actions = self.mdp.getPossibleActions(pred)
                    for action in actions:
                        qValue = self.computeQValueFromValues(pred, action)
                        values.append(qValue)
                    diff = abs(max(values) - self.values[pred])
                    if diff > self.theta:
                        priorityQ.update(pred, -diff)