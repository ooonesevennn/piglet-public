
from expanders.base_expander import base_expander
from domains.n_puzzle import n_puzzle, Puzzle_Actions,puzzle_action, puzzle_state
from search.search_node import search_node


class n_puzzle_expander(base_expander):
    puzzle_: n_puzzle
    succ_: list
    nodes_: list


    def __init__(self,puzzle: n_puzzle):
        self.puzzle_ = puzzle
        self.succ_ = []

    def expand(self, current_node: search_node):
        self.succ_.clear()
        current_state: puzzle_state = current_node.state_
        for action in range(0,len(self.puzzle_.swap_offset)):
            successor = self.__move(current_state, action)
            if successor == None:
                continue
            self.succ_.append((successor[0], successor[1]))
        return self.succ_[:]


    def __move(self, current: puzzle_state, action: int ):
        new_x_index = current.x_index_ + self.puzzle_.swap_offset[action]
        if not self.puzzle_.is_valid_move(current.x_index_, new_x_index):
            return None
        new_list = current.state_list_[:]
        temp = new_list[current.x_index_]
        new_list[current.x_index_] = new_list[new_x_index]
        new_list[new_x_index] = temp
        return puzzle_state(new_list,new_x_index,action), puzzle_action(action, 1)

    def __str__(self):
        return str(self.puzzle_)









