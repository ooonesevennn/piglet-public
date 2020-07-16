# search/tree_search.py
# 
# Implements the Tree-Search algorithm:
# Given an expander and an open list, this approach will 
# search until it finds the goal state.
# 
# The expansion order is determined by the type of open list.
# The task environment is determined by the expander
# 
# @author: dharabor
# @created: 2020-07-16
#

from search.search_node import search_node
from search.base_search import base_search


class tree_search(base_search):

    def __init__(self, open_list, expander):
        self.open_list_ = open_list
        self.expander_ = expander

    # Search the path between two state
    # @param start_state The start of the path
    # @param goal_state Then goal of the path
    # @return a list of locations between start and goal
    def get_path(self,start_state, goal_state):
    
        start_node = self.generate(start_state, None, None)
        self.open_list.push(start_node)

        # continue while there are still nods on OPEN
        while (len(self.open_list) > 0):
            current = self.open_list.pop()

            # goal test. if successful, return the solution
            if(current == goal_state):
                return self.solution(current)

            # expand the current node
            for succ in self.expander.expand(start_node):
                # each successor is a (state, action) tuple which
                # which we map to a corresponding search_node and push
                # then push onto the OPEN list
                succ_node = self.generate(succ[0], succ[1], current.state_)
                self.open_list.push(succ_node)

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        return None

    # Generate search_node objects for a given state
    # For this operatin we we need to know: 
    # @param state: the state which the search node maps to
    # @param action: the action which generated the state (could be [None])
    # @param parent: the parent state (could be [None])
    def generate(self,state: search_node, action, parent: search_node):
        
        retval = search_node()
        retval.state_ = state
        retval.action_ = action
        retval.parent_ = parent
        if(parent == None):
            # initialise the node from scratch 
            # NB: we usually do this only for the start node
            retval.g_ = 0
            retval.depth_ = 0
        else: 
            # initialise the node based on its parent
            retval.g_ = parent.g_ + action.cost_
            retval.depth_ = parent.depth_ + 1
            retval.parent_ = parent

    # extract the computed solution by following backpointers
    def solution(self,goal_node: search_node):
        
        tmp = goal_node
        sol = []
        while (tmp != None):
            sol.append(tmp)
            tmp = tmp.parent
        
        sol.reverse()
        return sol
