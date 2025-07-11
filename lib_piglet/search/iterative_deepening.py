# search/iterative deeping.py
#
#
# @author: dharabor
# @created: 2020-07-16
#

from lib_piglet.search.base_search import base_search
from lib_piglet.search.tree_search import tree_search
from lib_piglet.search.search_node import search_node
from lib_piglet.expanders.base_expander import base_expander
from enum import IntEnum
import time, sys


class ID_threshold(IntEnum):
    depth = 1
    cost = 2


class iterative_deepening(base_search):

    def __init__(self, open_list, expander: base_expander, heuristic_function=None, time_limit: int = sys.maxsize):
        super(iterative_deepening, self).__init__(open_list, expander, heuristic_function, time_limit)
        self.tree_search_engine: tree_search = tree_search(open_list, expander, heuristic_function, time_limit)

    # Search the path between two state
    # @param start_state The start of the path
    # @param goal_state Then goal of the path
    # @return solution Contains a list of locations between start and goal
    def get_path(self, start_state, goal_state, threshold_type=ID_threshold.depth):
        self.open_list_.clear()
        self.reset_statistic()
        self.start_ = start_state
        self.goal_ = goal_state
        self.start_time = time.process_time()
        start_node = self.generate(start_state, None, None)

        ## set initial depth limit here
        depth_threshold = start_node.depth_

        # Keep search until reach timelimit.
        while self.runtime_ < self.time_limit_:
            # Set time limit to DLS
            self.tree_search_engine.time_limit_ = self.time_limit_ - self.runtime_

            # Choose which value to limit based on search strategy, note tree_search_engine, is a tree_search implementation under
            # lib_piglet/search/tree_search, check the interface of get_path, find what you can use to limit the search on cost.
            solution = self.tree_search_engine.get_path(self.start_, self.goal_, depth_limit=depth_threshold)
            
            # Search finishes, get the minimal depth of unexpanded nodes as the depth limit of next iteration. 
            # Check tree search implementation on what results return after search finishes, find how you can get the minimal cost of 
            # unexpanded nodes to limit the cost of next iteration.
            next_depth = solution[1]


            # Update statistic info
            self.nodes_generated_ += self.tree_search_engine.nodes_generated_
            self.nodes_expanded_ += self.tree_search_engine.nodes_expanded_
            self.runtime_ = time.process_time() - self.start_time

            if solution[0] is None:
                if (threshold_type == ID_threshold.depth and next_depth == sys.maxsize):
                    self.solution_ = None
                    self.status_ = "Failed"
                    return None
                # if solution not found yet, we set the new depth limit and start next iteration.
                depth_threshold = next_depth
            else:
                self.solution_ = solution[0]
                self.status_ = "Success"
                return self.solution_

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        self.runtime_ = time.process_time() - self.start_time
        self.status_ = "Time out"
        self.solution_ = None
        return None
