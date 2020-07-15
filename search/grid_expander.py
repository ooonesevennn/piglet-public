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

