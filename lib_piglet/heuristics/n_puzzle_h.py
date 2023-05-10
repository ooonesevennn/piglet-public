# heuristics/n_puzzle_h.py
#
# Heuristics for n_puzzle problem.
#
# @author: mike
# @created: 2020-07-22
#

import math, copy, sys,json
from lib_piglet.domains.n_puzzle import puzzle_state, n_puzzle
from lib_piglet.expanders import n_puzzle_expander
from lib_piglet.search import dijkstra_search
from lib_piglet.utils.data_structure import bin_heap
from lib_piglet.search.search_node import compare_node_g

pattern_database = {}
pattern_database_pattern_width = 0

# piglet cli will use this function as heuristic.
def piglet_heuristic(domain,current_state, goal_state):
    return sum_manhattan_heuristic(current_state, goal_state)

def num_wrong_heuristic(current_state: puzzle_state, goal_state: puzzle_state):
    length = len(goal_state.state_list_)
    width = math.sqrt(length)
    h = 0
    for g in range(0,length):
        if goal_state.state_list_[g] != current_state.state_list_[g]:
            h+=1
    return h

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








