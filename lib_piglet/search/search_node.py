# search/search_node.py
# 
# Data structure that represents a domain-independent search node
#
# @author: dharabor
# @created: 2020-07-15
#

import sys
from functools import total_ordering

class search_node:
    action_ = None
    state_ = None
    parent_ = None
    g_ = 0
    depth_ = None
    instance_ = None
    h_ = 0
    f_ = 0
    closed_ = False
    open_handle_ = None

    def __init__(self):
        # some default values for uninitialised nodes
        self.action_ = None
        self.state_ = None
        self.parent_ = None
        self.g_ = sys.maxsize
        self.depth_ = sys.maxsize
        self.instance_ = sys.maxsize

    # Is the node closed
    # @return bool True if the node is closed
    def is_closed(self):
        return self.closed_

    # Mark the node as closed
    def close(self):
        self.closed_ = True

    # Mark the node as open
    def open(self):
        self.closed_ = False

    def __str__(self):
        return str(self.state_)

    def __repr__(self):
        return self.state_.__repr__()

    def __le__(self, other):
        return self.f_<= other.f_

    def __ge__(self, other):
        return self.f_ >= other.f_

    def __lt__(self, other):
        return self.f_ < other.f_

    def __gt__(self, other):
        return self.f_ > other.f_

    def __eq__(self, other):
        if (other == None):
            return False
        return self.state_ == other.state_

    def __hash__(self):
        return hash(self.state_)



    
