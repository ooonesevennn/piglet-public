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
        self.open_list_.push(start_node)

        # continue while there are still nods on OPEN
        while (len(self.open_list_) > 0):
            current = self.open_list_.pop()

            # goal test. if successful, return the solution
            if(current.state_ == goal_state):
                return self.solution(current)

            # expand the current node
            for succ in self.expander_.expand(current):
                # each successor is a (state, action) tuple which
                # which we map to a corresponding search_node and push
                # then push onto the OPEN list
                succ_node = self.generate(succ[0], succ[1], current)
                self.open_list_.push(succ_node)

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        return None


