# search/iterative deeping.py
#
#
# @author: dharabor
# @created: 2020-07-16
#

from lib_piglet.search.base_search import base_search
from lib_piglet.search.search_node import search_node
import time, sys



class iterative_deepening_dfs(base_search):


    # Search the path between two state
    # @param start_state The start of the path
    # @param goal_state Then goal of the path
    # @return solution Contains a list of locations between start and goal
    def get_path(self, start_state, goal_state, max_depth: int):
        self.open_list_.clear()
        self.reset_statistic()
        self.start_ = start_state
        self.goal_ = goal_state
        self.start_time = time.process_time()
        start_node = self.generate(start_state, None, None)

        # continue while there are still nods on OPEN
        thread_hold = 0
        while thread_hold <= max_depth:
            solution = self.DLS(start_node,thread_hold)
            if solution == None:
                thread_hold +=1
            else:
                return solution

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        self.runtime_ = time.process_time() - self.start_time
        self.status_ = "Failed"
        return None

    # Start a depth limited tree search
    # @param start The start node
    # @param limit The depth limit
    # @return solution Solution if find. None if solution not found.
    def DLS(self, start,limit):
        self.open_list_.clear()
        self.open_list_.push(start)

        while (len(self.open_list_) > 0):
            current: search_node = self.open_list_.pop()
            self.nodes_expanded_ += 1

            # goal test. if successful, return the solution
            if (current.state_ == self.goal_):
                self.solution_ = self.solution(current)
                self.status_ = "Success"
                self.runtime_ = time.process_time() - self.start_time
                return self.solution_

            # expand the current node
            for succ in self.expander_.expand(current):
                # each successor is a (state, action) tuple which
                # which we map to a corresponding search_node and push
                # then push onto the OPEN list
                succ_node = self.generate(succ[0], succ[1], current)
                if succ_node.g_ > limit:
                    continue
                self.open_list_.push(succ_node)
                self.nodes_generated_ += 1

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        self.runtime_ = time.process_time() - self.start_time
        self.status_ = "Failed"
        return None


class iterative_deepening_astar(base_search):


    # Search the path between two state
    # @param start_state The start of the path
    # @param goal_state Then goal of the path
    # @return solution Contains a list of locations between start and goal
    def get_path(self, start_state, goal_state):
        self.open_list_.clear()
        self.reset_statistic()
        self.start_ = start_state
        self.goal_ = goal_state
        self.start_time = time.process_time()
        start_node = self.generate(start_state, None, None)

        # continue while there are still nods on OPEN
        thread_hold = start_node.f_

        while True:
            solution = self.DLS(start_node,thread_hold)

            if type(solution) == int or type(solution) == float:
                if solution == sys.maxsize:
                    return None
                thread_hold = solution
            else:
                return solution

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        self.runtime_ = time.process_time() - self.start_time
        self.status_ = "Failed"
        return None

    # Start a depth limited tree search
    # @param start The start node
    # @param limit The depth limit
    # @return solution Solution if find. None if solution not found.
    def DLS(self, start,thread_hold):
        self.open_list_.clear()
        self.open_list_.push(start)
        min_next_f_ = sys.maxsize

        while (len(self.open_list_) > 0):
            current: search_node = self.open_list_.pop()
            self.nodes_expanded_ += 1

            # goal test. if successful, return the solution
            if (current.state_ == self.goal_):
                self.solution_ = self.solution(current)
                self.status_ = "Success"
                self.runtime_ = time.process_time() - self.start_time
                return self.solution_

            # expand the current node
            for succ in self.expander_.expand(current):
                # each successor is a (state, action) tuple which
                # which we map to a corresponding search_node and push
                # then push onto the OPEN list
                succ_node = self.generate(succ[0], succ[1], current)
                if succ_node.f_ > thread_hold:
                    if succ_node.f_<min_next_f_:
                        min_next_f_ = succ_node.f_
                    continue
                self.open_list_.push(succ_node)
                self.nodes_generated_ += 1

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        self.runtime_ = time.process_time() - self.start_time
        self.status_ = "Failed"
        return min_next_f_
