# search/base_search.py
# This module defines a base search class and what attribute/method a search class should have.
#
# @author: mike
# @created: 2020-07-15
#
import sys
from lib_piglet.expanders.base_expander import base_expander
from lib_piglet.search.search_node import search_node
from lib_piglet.solution.solution import solution

statistic_template = "{0:10}| {1:10}| {2:10}| {3:10}| {4:10}| {5:10}| {6:10}| {7:10}| {8:10} "

class base_search:
    nodes_generated_: int = 0
    nodes_expanded_: int = 0
    runtime_: float = 0
    start_time_: float = 0
    time_limit_: int = sys.maxsize
    expander_: base_expander = None
    solution_: solution = None
    start_ = None
    goal_ = None
    status_ = None
    cost_function_ = None
    statistic_header_ = [
        "Status",
        "Cost",
        "Depth",
        "Nodes(exp)",
        "Nodes(gen)",
        "Runtime",
        "start",
        "goal",
        "Problem"]

    def __init__(self, open_list, expander:base_expander, cost_function = None, time_limit: int = sys.maxsize):
        self.open_list_ = open_list
        self.expander_ = expander
        self.time_limit_ = time_limit
        self.cost_function_ = cost_function

    # Search the path between two state
    # @param start_state The start of the path
    # @param goal_state Then goal of the path
    # @return a list of locations between start and goal
    def get_path(self,start_state, goal_state):
        raise NotImplementedError()

    # Generate search_node objects for a given state
    # For this operatin we we need to know:
    # @param state: the state which the search node maps to
    # @param action: the action which generated the state (could be [None])
    # @param parent: the parent state (could be [None])
    def generate(self, state, action, parent: search_node):

        retval = search_node()
        retval.state_ = state
        retval.action_ = action
        if (parent == None):
            # initialise the node from scratch
            # NB: we usually do this only for the start node
            retval.g_ = 0
            retval.depth_ = 0
            if self.cost_function_ == None:
                retval.h_ = 0
                retval.f_ = retval.g_
            else:
                self.cost_function_(retval)
        else:
            # initialise the node based on its parent
            retval.g_ = parent.g_ + action.cost_
            retval.depth_ = parent.depth_ + 1
            retval.parent_ = parent
            if self.cost_function_ == None:
                retval.h_ = 0
                retval.f_ = retval.g_
            else:
                self.cost_function(retval)
        return retval

    # extract the computed solution by following backpointers
    def solution(self, goal_node: search_node):
        tmp = goal_node
        depth = goal_node.depth_
        cost = goal_node.g_
        sol = []
        while (tmp != None):
            sol.append(tmp)
            tmp = tmp.parent_

        sol.reverse()
        return solution(sol,depth,cost)

    # Print statistic information on screen
    def print_statistic(self):
        print(statistic_template.format(*[str(x) for x in self.get_statistic()]))

    # Print header for statistic on screen
    def print_header(self):
        print(statistic_template.format(*self.get_header()))

    # Get statistic information
    # @return list A list of Statistic information
    def get_statistic(self):
        sta_ = [self.status_]
        if self.solution_!=None:
            sta_ += self.solution_.get_solution_info()
        else:
            sta_ += [None, None]
        sta_ += [self.nodes_expanded_,
                self.nodes_generated_,
                round(self.runtime_,4),
                self.start_,
                self.goal_,
                self.expander_]

        return sta_

    # Get header for statistic
    # @return list A list of header
    def get_header(self):
        return self.statistic_header_

    def reset_statistic(self):
        self.nodes_generated_: int = 0
        self.nodes_expanded_: int = 0
        self.runtime_: float = 0
        self.start_time_: float = 0
        self.solution_: solution = None
        self.start_ = None
        self.goal_ = None






