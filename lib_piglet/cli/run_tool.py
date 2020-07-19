# cli/run_tool.py
# This module provides function to run tasks for cli interface
#
# @author: mike
# @created: 2020-07-19


from lib_piglet.cli.cli_tool import task, args_interface, DOMAIN_TYPE
from lib_piglet.domains import gridmap,n_puzzle
from lib_piglet.expanders import grid_expander, n_puzzle_expander
from lib_piglet.search import tree_search, graph_search, uniform_cost_search,base_search
from lib_piglet.utils.data_structure import queue,stack,bin_heap


# run task with cli arguments
# @param t A task object describe the task domain, start and goal
# @param args Arguments object from cli interface
# @return search A search engine with search result
def run_task(t: task, args: args_interface):
    if t.domain_type == DOMAIN_TYPE.gridmap:
        domain = gridmap.gridmap()
        domain.load(t.domain)
        start = t.start_state
        goal  = t.goal_state
        expander = grid_expander.grid_expander(domain)

    elif t.domain_type == DOMAIN_TYPE.n_puzzle:
        domain = n_puzzle.n_puzzle()
        domain.load(t.domain)
        start = domain.start_state()
        goal = domain.goal_state()
        expander = n_puzzle_expander.n_puzzle_expander(domain)



    cost_function = None
    strategy = args.strategy[0]
    if strategy == "dfs":
        open_list = stack()
    elif strategy == "bfs":
        open_list = queue()
    elif strategy == "best-first":
        open_list = bin_heap()

    engine: base_search.base_search = None
    if args.framework == "tree-search":
        engine = tree_search.tree_search
    elif args.framework == "graph-search":
        engine = graph_search.graph_search
    elif args.framework == "uniform-cost-search":
        engine = uniform_cost_search.uniform_cost_search


    search_engine = engine(open_list,expander,cost_function,time_limit=args.time_limit)
    search_engine.get_path(start,goal)
    return search_engine
