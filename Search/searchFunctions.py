import util
import time
from game import Directions

UNREACHABLE_GOAL_STATE = [Directions.STOP]


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def dfs_bfs_ucs(problem, datatype, isucs):
    seen = []
    walk = []
    parentMap = {}
    goal = None
    startState = (problem.getStartState(), '', 0)
    parentMap[startState] = 'start'
    if (not isucs):
        datatype.push(startState)
    else:
        datatype.push(startState, 0)
    while not(datatype.isEmpty()):
        vertex = datatype.pop()
        if (problem.isGoalState(vertex[0])):
            goal = vertex
            break
        if vertex[0] not in seen:
            seen.append(vertex[0])
            for i in problem.getNextStates(vertex[0]):
                if (i[0] not in seen):
                    if (not isucs):
                        datatype.push(i)
                    else:
                        datatype.push(i, i[2])
                    parentMap[i] = vertex
    if (goal != None):
        while (goal != "start"):
            walk.append(goal[1])
            goal = parentMap[goal]
        return list(reversed(walk[0:len(walk)-1]))
    else:
        return [Directions.STOP]


def right_hand_maze_search(problem):
    """
    Q1: Search using right hand rule

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's next states:", problem.getNextStates(
        problem.getStartState())

    :param problem: instance of SearchProblem
    :return: list of actions
    """

    "*** YOUR CODE HERE ***"
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    state = problem.getStartState()
    direction = w
    rightHand = {w: n, n: e, e: s, s: w}
    leftHand = {w: s, s: e, e: n, n: w}
    walk = []
    while not(problem.isGoalState(state)):
        nextStates = problem.getNextStates(state)
        flag = False
        if (flag == False):
            for i in nextStates:
                if (rightHand[direction] == i[1]):
                    walk.append(rightHand[direction])
                    state = i[0]
                    direction = rightHand[direction]
                    flag = True
                    break
        if (flag == False):
            for i in nextStates:
                if (direction == i[1]):
                    walk.append(direction)
                    state = i[0]
                    flag = True
                    break
        if (flag == False):
            for i in nextStates:
                if (leftHand[direction] == i[1]):
                    walk.append(leftHand[direction])
                    state = i[0]
                    direction = leftHand[direction]
                    flag = True
                    break
        if (flag == False):
            for i in nextStates:
                if (leftHand[leftHand[direction]] == i[1]):
                    walk.append(leftHand[leftHand[direction]])
                    state = i[0]
                    direction = leftHand[leftHand[direction]]
                    flag = True
                    break
    return walk

    util.raiseNotDefined()


def dfs(problem):
    """
    Q2: Search the deepest nodes in the search tree first.
    """

    "*** YOUR CODE HERE ***"

    stack = util.Stack()
    return dfs_bfs_ucs(problem, stack, False)

    util.raiseNotDefined()


def bfs(problem):
    """
    Q3: Search the shallowest nodes in the search tree first.
    """

    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    return dfs_bfs_ucs(problem, queue, False)

    util.raiseNotDefined()


def ucs(problem):
    """
    Q6: Search the node of least total cost first.
    """

    "*** YOUR CODE HERE ***"

    pQueue = util.PriorityQueue()
    return dfs_bfs_ucs(problem, pQueue, True)
    util.raiseNotDefined()
