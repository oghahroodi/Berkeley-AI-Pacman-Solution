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
import random
import util

from game import Agent
from ghostAgents import GHOST_AGENT_MAX_DEPTH, GhostAgent


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class AdversarialSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxAgent, SmartPacmanAgent, SmartGhostAgent

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # index should be 0 by default
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getOpponentIndex(self):
        return 1 - self.index


class MinimaxAgent(AdversarialSearchAgent):

    def getAction(self, gameState):
        """
        The Agent will receive a GameState and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        minimaxScores = []
        legalActions = gameState.getLegalActions(self.index)
        for action in legalActions:
            score = self.minimax(
                gameState.generateSuccessor(self.index, action),
                self.getOpponentIndex(),
                0
            )
            minimaxScores.append((score, action))

        bestAction = max(minimaxScores)[1]

        return bestAction

    def minimax(self, gameState, maximizingAgent, currentDepth):
        """
        Returns the minimax score for the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        self.index:
            Return your agent's index
        self.getOpponentIndex():
            Return your opponent's index
        gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
        gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

        Args:
            gameState: an instance of pacman.GameState, minimax algorithm should be started on this state
            maximizingAgent: index of agent we're maximizing score for, you can check this paramterer against self.index 
            currentDepth: current depth in minmax tree

        Returns:
            Return minimax score
        """

        if (currentDepth == self.depth or gameState.getLegalActions(maximizingAgent) == []):
            return self.evaluationFunction(gameState)
        else:
            if self.index == maximizingAgent:
                self.min_init = float('-inf')
                for i in gameState.getLegalActions(self.index):
                    self.min_init = max(self.min_init, self.minimax(
                        gameState.generateSuccessor(self.index, i), self.getOpponentIndex(), currentDepth+1))
                return self.min_init
            else:
                self.max_init = float('inf')
                for i in gameState.getLegalActions(self.index):
                    self.max_init = min(self.max_init, self.minimax(
                        gameState.generateSuccessor(self.index, i), self.index, currentDepth+1))
                return self.max_init

        # util.raiseNotDefined()


class SmartPacmanAgent(MinimaxAgent):
    def __init__(self, depth='2'):
        self.index = 0
        self.depth = int(depth)

    @staticmethod
    def evaluationFunction(gameState):
        """
        Returns evaluation score for each gameState

        Args:
            gameState: an instance of pacman.GameState

        Returns:
            Return the evaluation score
        """
        if gameState.isLose():
            return -float("inf")
        if gameState.isWin():
            return float("inf")

        pacman_position = gameState.getPacmanPosition()

        ghost_position = gameState.getGhostPosition(1)
        foods = gameState.getFood().asList()
        food_number = gameState.getNumFood()
        capsules_positions = gameState.getCapsules()
        ghost_state = gameState.getGhostState(1)
        tmp = +1

        if pacman_position == (9, 5) or pacman_position == (10, 5) or pacman_position == (8, 5) or pacman_position == (11, 5):
            return -float("inf")

        if ghost_state.scaredTimer:
            tmp = -5

        ghost_distance = util.manhattanDistance(
            pacman_position, ghost_position)

        food_distance = 100000
        for i in foods:
            food_distance = min(
                food_distance, util.manhattanDistance(i, pacman_position))

        value = scoreEvaluationFunction(
            gameState)+0.5*tmp*ghost_distance - 1*food_distance - 10*food_number - 50*len(capsules_positions) + random.randint(1, 5)
        return value
        # util.raiseNotDefined()


class SmartGhostAgent(MinimaxAgent):
    def __init__(self, index):
        self.index = 1
        self.depth = GHOST_AGENT_MAX_DEPTH

    @staticmethod
    def evaluationFunction(gameState):
        """
        Similar to SmartPacmanAgent
        """

        if gameState.isLose():
            return float("inf")
        elif gameState.isWin():
            return -float("inf")

        foods = gameState.getFood().asList()
        pacman_position = gameState.getPacmanState().getPosition()

        food_distance = 100000
        pos = (0, 0)
        for i in foods:
            if food_distance > util.manhattanDistance(i, pacman_position):
                food_distance = util.manhattanDistance(i, pacman_position)
                pos = pacman_position

        if gameState.getPacmanState().getDirection() == 'North':
            goal_position = (pacman_position[0], pacman_position[1]+1)

        elif gameState.getPacmanState().getDirection() == 'West':
            goal_position = (pacman_position[0]-1, pacman_position[1])

        elif gameState.getPacmanState().getDirection() == 'South':
            goal_position = (pacman_position[0], pacman_position[1]-1)

        elif gameState.getPacmanState().getDirection() == 'East':
            goal_position = (pacman_position[0]+1, pacman_position[1])
        return -util.manhattanDistance(goal_position, gameState.getGhostPosition(1))-util.manhattanDistance(pos, gameState.getGhostPosition(1))


class SuperGhostAgent(GhostAgent):
    def __init__(self, index):
        self.index = index
        self.depth = GHOST_AGENT_MAX_DEPTH

    def getAction(self, gameState):
        minimaxScores = []
        legalActions = gameState.getLegalActions(self.index)
        for action in legalActions:
            score = self.minimax(
                gameState.generateSuccessor(self.index, action),
                self.getOpponentIndex(),
                0
            )
            minimaxScores.append((score, action))

        bestAction = max(minimaxScores)[1]

        return bestAction

    def getOpponentIndex(self):
        return 1 - self.index

    def minimax(self, gameState, maximizingAgent, currentDepth):

        if (currentDepth == self.depth or gameState.getLegalActions(maximizingAgent) == []):
            return self.evaluationFunction(gameState)
        else:
            if self.index == maximizingAgent:
                self.min_init = float('-inf')
                for i in gameState.getLegalActions(self.index):
                    self.min_init = max(self.min_init, self.minimax(
                        gameState.generateSuccessor(self.index, i), self.getOpponentIndex(), currentDepth+1))
                return self.min_init
            else:
                self.max_init = float('inf')
                for i in gameState.getLegalActions(self.index):
                    self.max_init = min(self.max_init, self.minimax(
                        gameState.generateSuccessor(self.index, i), self.index, currentDepth+1))
                return self.max_init

    def evaluationFunction(self, gameState):

        if gameState.isLose():
            return float("inf")
        elif gameState.isWin():
            return -float("inf")

        foods = gameState.getFood().asList()
        pacman_position = gameState.getPacmanState().getPosition()

        food_distance = 100000
        pos = (0, 0)
        for i in foods:
            if food_distance > util.manhattanDistance(i, pacman_position):
                food_distance = util.manhattanDistance(i, pacman_position)
                pos = pacman_position

        if gameState.getPacmanState().getDirection() == 'North':
            goal_position = (pacman_position[0], pacman_position[1]+1)

        elif gameState.getPacmanState().getDirection() == 'West':
            goal_position = (pacman_position[0]-1, pacman_position[1])

        elif gameState.getPacmanState().getDirection() == 'South':
            goal_position = (pacman_position[0], pacman_position[1]-1)

        elif gameState.getPacmanState().getDirection() == 'East':
            goal_position = (pacman_position[0]+1, pacman_position[1])
        return -util.manhattanDistance(goal_position, gameState.getGhostPosition(1))-util.manhattanDistance(pos, gameState.getGhostPosition(1))
