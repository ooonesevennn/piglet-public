# domains/grid_expander.py
# 
# Expand function for the 4-connected gridmap domain.
#
# Given a current search node, the expander checks the set of valid grid actions 
# and generates search node successors for each.
#
# @author: dharabor
# @created: 2020-07-15
#

from search import search_node,constants

class grid_expander

    def __init__(self, gridmap):
        self.gm_ = gridmap
        self.effects_ = [gm_.height_*-1, gm_.height_, -1, 1]

        # memory for storing successor (state, action) pairs
        self.succ_ = [None] * 4 

        # pre-allocate a pool of search nodes
        self.nodes_ = []
        for x in range(gm_.height_ * gm_.width_)
            self.nodes_.append(search_node.search_node()])

    # identify successors of the current node
    def expand(self, current):
        
        self.succ_.clear()
        for(a in gm_.get_actions(current.state_))
            # NB: we only initialise the state and action attributes.
            # The search will initialise the rest, assuming it decides 
            # to add the corresponding successor to OPEN
            self.succ_.append((current.state_ + self.effects_[a.move_], a))
        return self.successors_

    # Generate search_node objects for a given state
    # For this operatin we we need to know: 
    # @param state: the state which the search node maps to
    # @param action: the action which generated the state (could be [None])
    # @param parent: the parent state (could be [None])
    def generate(state, action, parent):

        # validate that the state is legit
        if(state < 0 or state >= (gm_.width_ * gm_.height_))
            return None;
        
        retval = nodes_[state]
        retval.state_ = state
        retval.action_ = action
        if(parent != None):
            # initialise the node based on its parent
            retval.parent_ = parent
            retval.g_ = parent.g_ + action.cost_
            retval.depth_ = parent.depth_ + 1
        else:
            # initialise the node from scratch 
            # NB: we usually do this only for the start node
            retval.parent_ = None
            retval.g_ = 0
            
