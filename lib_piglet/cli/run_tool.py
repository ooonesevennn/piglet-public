# cli/run_tool.py
# This module provides function to run tasks for cli interface
#
# @author: mike
# @created: 2020-07-19


from lib_piglet.cli.cli_tool import task, args_interface, DOMAIN_TYPE
from lib_piglet.domains import gridmap,n_puzzle
from lib_piglet.expanders import grid_expander, n_puzzle_expander, base_expander
from lib_piglet.search import tree_search, graph_search,base_search,search_node, iteritive_deepening
from lib_piglet.utils.data_structure import queue,stack,bin_heap
from lib_piglet.heuristics import gridmap_h,n_puzzle_h

search_engine: base_search.base_search = None
expander: base_expander.base_expander = None
domain = None



# run task with cli arguments
# @param t A task object describe the task domain, start and goal
# @param args Arguments object from cli interface
# @return search A search engine with search result
def run_task(t: task, args: args_interface):
    global search_engine, expander, domain
    same_problem = False
    if search_engine is not None and t.domain == domain.domain_file_:
        if t.domain_type == DOMAIN_TYPE.gridmap:
            start = t.start_state
            goal = t.goal_state
        elif t.domain_type == DOMAIN_TYPE.n_puzzle:
            domain.set_start(t.start_state)
            start = domain.start_state()
            goal = domain.goal_state()
    else:
        if t.domain_type == DOMAIN_TYPE.gridmap:
            domain = gridmap.gridmap(t.domain)
            start = t.start_state
            goal  = t.goal_state
            expander = grid_expander.grid_expander(domain)
            heuristic = gridmap_h.manhattan_heuristic

        elif t.domain_type == DOMAIN_TYPE.n_puzzle:
            domain = n_puzzle.n_puzzle(t.domain)
            domain.set_start(t.start_state)
            start = domain.start_state()
            goal = domain.goal_state()
            expander = n_puzzle_expander.n_puzzle_expander(domain)
            heuristic = n_puzzle_h.sum_manhattan_heuristic


        heuristic_function = None
        strategy = args.strategy
        if strategy == "depth":
            open_list = stack()
        elif strategy == "breath":
            open_list = queue()
        elif strategy == "uniform":
            open_list = bin_heap(search_node.compare_node_g)
        elif strategy =="a-star":
            open_list =  bin_heap(search_node.compare_node_f)
            heuristic_function = heuristic
        elif strategy == "greedy-best":
            open_list =  bin_heap(search_node.compare_node_h)
            heuristic_function = heuristic


        engine: base_search.base_search = None
        if args.framework == "tree":
            engine = tree_search.tree_search
        elif args.framework == "graph":
            engine = graph_search.graph_search
        elif args.framework == "iterative-depth" and strategy == "a-star":
            engine = iteritive_deepening.iterative_deepening_astar
            open_list = stack()
        elif args.framework == "iterative-depth" and strategy == "depth":
            engine = iteritive_deepening.iterative_deepening_dfs
            open_list = stack()

        search_engine = engine(open_list,expander,heuristic_function = heuristic_function,time_limit=args.time_limit)

    if args.framework == "iterative-depth" and args.strategy == "depth":
        search_engine.get_path(start,goal,args.depth_limit)
    else:
        search_engine.get_path(start,goal)
    return search_engine
