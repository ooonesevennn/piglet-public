# expander/base_search.py
# This module defines a virtual implementation of expand class and what attribute/method a expander class should have.
#
# @author: mike
# @created: 2020-07-15
#


class base_expander:
    domain_ = None

    def __init__(self, domain):
        pass

    # identify successors of the current node
    #
    # @param current: The current node
    # @return : successer of a list of (state, action) tuple
    def expand(self, current):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()
