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

from search import search_node

class tree_search:

    def __init__(self, open_list, expander):
        self.open_list_ = open_list
        self.expander_ = expander

    def get_path(start_state, goal_state):
    
        start_node = generate(start_state, None, None)
        open_list.push(start_node)

        # continue while there are still nods on OPEN
        while(len(open_list) > 0):  
            current = open_list.pop()

            # goal test. if successful, return the solution
            if(current == goal_state):
                return solution(current)

            # expand the current node
            for(succ  in expander.expand(start_node)):
                # each successor is a (state, action) tuple which
                # which we map to a corresponding search_node and push
                # then push onto the OPEN list
                succ_node = generate(succ[0], succ[1], current.state_)
                open_list.push(succ_node)

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        return None

    def generate(state, action, parent):
        
        retval = search_node.search_node()
        retval.state_ = state
        retval.action_ = action
        retval.parent_ = parent
        if(parent == None):
            retval.g_ = 0
            retval.depth_ = 0
        else: 
            retval.g_ = parent.g_ + action.cost_
            retval.parent_ = parent

    # extract the computed solution by following backpointers
    def solution(goal_node):
        
        tmp = goal_node
        sol = []
        while(tmp != None)
            sol.append(tmp)
            tmp = tmp.parent
        
        sol.reverse()
        return sol