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

from search.search_node import search_node
from search.constants import *
from search.base_expander import base_expander
from domains.gridmap import gridmap

class grid_expander(base_expander):
    gm_: gridmap
    effects_: list
    succ_: list
    nodes_: list
    def __init__(self, map : gridmap):
        self.gm_ = map
        self.effects_ = [self.gm_.height_*-1, self.gm_.height_, -1, 1]

        # memory for storing successor (state, action) pairs
        self.succ_ = [None] * 4 

        # pre-allocate a pool of search nodes
        self.nodes_ = []
        for x in range(self.gm_.height_ * self.gm_.width_):
            self.nodes_.append(search_node.search_node())

    # identify successors of the current node
    #
    # @param current: The current node
    # @return : Possible next
    def expand(self, current: search_node):
        
        self.succ_.clear()
        for a in self.gm_.get_actions(current.state_):
            # NB: we only initialise the state and action attributes.
            # The search will initialise the rest, assuming it decides 
            # to add the corresponding successor to OPEN
            self.succ_.append((current.state_ + self.effects_[a.move_], a))
        return self.successors_

