# heuristics/gridmap_h.py
#
# Heuristics for gridmap.
#
# @author: mike
# @created: 2020-07-22
#

import math

def piglet_heuristic(domain,current_state, goal_state):
    return manhattan_heuristic(current_state, goal_state)

def pigelet_multi_agent_heuristic(domain,current_state, goal_state):
    h = 0
    for agent, loc in current_state.agent_locations_.items():
        h += manhattan_heuristic(loc, goal_state.agent_locations_[agent])
    return h

def manhattan_heuristic(current_state, goal_state):
    return abs(current_state[0] - goal_state[0]) + abs(current_state[1] - goal_state[1])


def straight_heuristic(current_state, goal_state):
    return round(math.sqrt((current_state[0] - goal_state[0])**2 + (current_state[1] - goal_state[1])**2), 5)

def octile_heuristic(current_state, goal_state):
    delta_x = abs(current_state[0] - goal_state[0])
    delta_y = abs(current_state[1] - goal_state[1])
    return min(delta_x, delta_y) * math.sqrt(2) + max(delta_x,delta_y) - min(delta_x, delta_y)