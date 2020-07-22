# heuristics/n_puzzle_h.py
#
# Heuristics for n_puzzle problem.
#
# @author: mike
# @created: 2020-07-22
#

import math
from lib_piglet.domains.n_puzzle import puzzle_state


def sum_manhattan_heuristic(current_state: puzzle_state, goal_state: puzzle_state):
    length = len(goal_state.state_list_)
    width = math.sqrt(length)
    h = 0
    for g in range(0,length):
        if goal_state.state_list_[g] == "x":
            continue
        c = current_state.state_list_.index(goal_state.state_list_[g])
        h += abs(c//width - g//width) + abs(c%width - g%width)
    return h


def sum_straight_heuristic(current_state, goal_state):
    length = len(goal_state.state_list_)
    width = math.sqrt(length)
    h = 0
    for g in range(0, length):
        if goal_state.state_list_[g] == "x":
            continue
        c = current_state.state_list_.index(goal_state.state_list_[g])
        h += round(math.sqrt((c // width - g // width)**2 + (c % width - g % width)**2))
    return h