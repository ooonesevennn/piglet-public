import os, sys
sys.path.extend("../")

from lib_piglet.domains import pddl
from lib_piglet.expanders.pddl_expander import pddl_expander
from lib_piglet.search.tree_search import tree_search
from lib_piglet.search.graph_search import graph_search
from lib_piglet.search.search_node import compare_node_g, compare_node_f
from lib_piglet.utils.data_structure import queue,stack,bin_heap
from lib_piglet.cli.cli_tool import statistic_template, print_header
# from lib_piglet.heuristics import n_puzzle_h
from lib_piglet.search.iterative_deepening import iterative_deepening, ID_threshold

file_folder = os.path.dirname(os.path.abspath(__file__))
domainfile = os.path.join(file_folder, "pddl/pacman/pacman_bool.pddl")
problemfile = os.path.join(file_folder, "pddl/pacman/test_problem.pddl")

domain = pddl.pddl(domainfile, problemfile)
expander = pddl_expander(domain)
search = graph_search(bin_heap(compare_node_f), expander,time_limit=60)
solution = search.get_path(domain.start_state_, domain.goal_state_)

print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], "Hidden"))


