# expander/grid_expander.py
# 
# Expand function for the 4-connected gridmap domain.
#
# Given a current search node, the expander checks the set of valid grid actions 
# and generates search node successors for each.
#
# @author: dharabor
# @created: 2020-07-15
#

from lib_piglet.search.search_node import search_node
from lib_piglet.expanders.base_expander import base_expander
from lib_piglet.domains.gridmap import gridmap
from lib_piglet.domains.grid_action import  Move_Actions, grid_action

class grid_expander(base_expander):
    domain_: gridmap
    effects_: list
    succ_: list
    nodes_: list
    def __init__(self, map : gridmap):
        self.domain_ = map
        self.effects_ = [self.domain_.height_*-1, self.domain_.height_, -1, 1]

        # memory for storing successor (state, action) pairs
        self.succ_ = [None] * 4 

        # pre-allocate a pool of search nodes
        self.nodes_ = []
        for x in range(self.domain_.height_ * self.domain_.width_):
            self.nodes_.append(search_node())

    # identify successors of the current node
    #
    # @param current: The current node
    # @return : Possible next
    def expand(self, current: search_node):
        
        self.succ_.clear()
        for a in self.get_actions(current.state_):
            # NB: we only initialise the state and action attributes.
            # The search will initialise the rest, assuming it decides 
            # to add the corresponding successor to OPEN
            new_state = self.__move(current.state_, a.move_)
            self.succ_.append((new_state, a))
        return self.succ_[:]

        # return a list with all the applicable/valid actions
        # at tile (x, y)
        # @param loc A (x,y) coordinate tuple
        # @return a list of gridaction object.

    def get_actions(self, loc: tuple):
        x = loc[0]
        y = loc[1]
        retval = []

        if (x < 0 or x >= int(self.domain_.height_) or y < 0 or y >= int(self.domain_.width_)):
            return retval

        if (self.domain_.map_[x][y] == False):
            return retval

        if (int(y - 1) >= 0 and self.domain_.map_[x][y - 1]):
            retval.append(grid_action())
            retval[-1].move_ = Move_Actions.MOVE_LEFT
            retval[-1].cost_ = 1;

        if (int(y + 1) < int(self.domain_.height_) and self.domain_.map_[x][y + 1]):
            retval.append(grid_action())
            retval[-1].move_ = Move_Actions.MOVE_RIGHT
            retval[-1].cost_ = 1;

        if ((int(x) - 1) >= 0 and self.domain_.map_[x - 1][y]):
            retval.append(grid_action())
            retval[-1].move_ = Move_Actions.MOVE_UP
            retval[-1].cost_ = 1;

        if ((int(x) + 1) < int(self.domain_.width_) and self.domain_.map_[x + 1][y]):
            retval.append(grid_action())
            retval[-1].move_ = Move_Actions.MOVE_DOWN
            retval[-1].cost_ = 1;

        return retval

    def __move(self, curr_state: tuple, move):
        x = curr_state[0]
        y = curr_state[1]
        if move == Move_Actions.MOVE_UP:
            x -= 1
        elif move == Move_Actions.MOVE_DOWN:
            x += 1
        elif move == Move_Actions.MOVE_LEFT:
            y -= 1
        elif move == Move_Actions.MOVE_RIGHT:
            y += 1
        return x, y

    def __str__(self):
        return str(self.domain_)


