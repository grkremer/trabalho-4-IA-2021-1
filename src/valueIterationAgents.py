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

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
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
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        
        old_values = util.Counter()

        for k in range(self.iterations):
            for state in mdp.getStates():
                old_values[state] = self.getValue(state)
            for state in mdp.getStates():
                if(mdp.isTerminal(state)):
                    self.values[state] = mdp.getReward(state, None, state)
                else:                 
                    max_sum = float('-inf')
                    for action in mdp.getPossibleActions(state):
                        sum_state = 0
                        for state_prob in mdp.getTransitionStatesAndProbs(state, action):
                            sum_state += state_prob[1]*old_values[state_prob[0]]
                        max_sum = max([max_sum, sum_state])
                    self.values[state] = mdp.getReward(state, None, state) + self.discount*max_sum


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        q = 0
        for state_prob in self.mdp.getTransitionStatesAndProbs(state, action):
            new_state = state_prob[0]
            new_state_prob = state_prob[1]
            q += self.mdp.getReward(state, action, new_state) + (new_state_prob * self.discount * self.getValue(new_state))
        return q

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        best_action = None
        best_q = float('-inf')
        for action in self.mdp.getPossibleActions(state):
            action_q = self.computeQValueFromValues(state, action)
            if action_q > best_q:
                best_q = action_q
                best_action = action
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
