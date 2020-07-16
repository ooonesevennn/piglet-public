# search/base_search.py
# This module defines a base search class and what attribute/method a search class should have.
#
# @author: mike
# @created: 2020-07-15
#

from search.base_expander import base_expander


class base_search:
    expander_ : base_expander

    def __init__(self):
        pass

    # Search the path between two state
    # @param start_state The start of the path
    # @param goal_state Then goal of the path
    # @return a list of locations between start and goal
    def get_path(self,start_state, goal_state):
        raise NotImplementedError()

    # Generate search_node objects for a given state
    # For this operatin we we need to know:
    # @param state: the state which the search node maps to
    # @param action: the action which generated the state
    # @param parent: the parent
    def generate(self, state, action, parent):
        raise NotImplementedError()



