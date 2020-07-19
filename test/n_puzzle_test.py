import os, sys
sys.path.extend("../")

from lib_piglet.domains import n_puzzle
from lib_piglet.expanders.n_puzzle_expander import n_puzzle_expander
from lib_piglet.search.tree_search import tree_search
from lib_piglet.search.graph_search import graph_search
from lib_piglet.search.uniform_cost_search import uniform_cost_search
from lib_piglet.utils.data_structure import queue,stack,bin_heap

file_folder = os.path.dirname(os.path.abspath(__file__))
inputfile = os.path.join(file_folder, "n_puzzle/sample_9_puzzle")



puzzle = n_puzzle.n_puzzle()
puzzle.load(inputfile)

expander = n_puzzle_expander(puzzle)
search = tree_search(queue(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_header()
search.print_statistic()

search = tree_search(stack(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()

search = tree_search(bin_heap(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()

search = graph_search(queue(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()

search = graph_search(stack(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()

search = graph_search(bin_heap(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()

search = uniform_cost_search(queue(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()

search = uniform_cost_search(stack(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()

search = uniform_cost_search(bin_heap(), expander, time_limit=10)
path = search.get_path(puzzle.start_state(), puzzle.goal_state())
search.print_statistic()
