# heuristics/gridmap_h.py
#
# Heuristics for gridmap.
#
# @author: mike
# @created: 2020-07-22
#

import math

def manhattan_heuristic(current_state, goal_state):
    return abs(current_state[0] - goal_state[0]) + abs(current_state[1] - goal_state[1])


def straight_heuristic(current_state, goal_state):
    return round(math.sqrt((current_state[0] - goal_state[0])**2 + (current_state[1] - goal_state[1])**2), 5)