# cli/run_tool.py
# This module provides function to run tasks for cli interface
#
# @author: mike
# @created: 2020-07-19


from lib_piglet.cli.cli_tool import task, args_interface, DOMAIN_TYPE
from lib_piglet.domains import gridmap,n_puzzle,graph
from lib_piglet.expanders import grid_expander, n_puzzle_expander, base_expander, graph_expander
from lib_piglet.search import tree_search, graph_search,base_search,search_node, iterative_deepening
from lib_piglet.utils.data_structure import queue,stack,bin_heap
from lib_piglet.heuristics import gridmap_h,n_puzzle_h,graph_h

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

    # if serach engine exist and domain file doesn't change, just update start and goal
    if search_engine is not None and t.domain == domain.domain_file_:
        if t.domain_type == DOMAIN_TYPE.gridmap:
            start = t.start_state
            goal = t.goal_state
        elif t.domain_type == DOMAIN_TYPE.n_puzzle:
            domain.set_start(t.start_state)
            start = domain.start_state()
            goal = domain.goal_state()
        elif t.domain_type == DOMAIN_TYPE.graph:
            start = domain.get_vertex(t.start_state)
            goal = domain.get_vertex(t.goal_state)

    # if no search engine or domain file change, reload domain.
    else:
        if t.domain_type == DOMAIN_TYPE.gridmap:
            domain = gridmap.gridmap(t.domain)
            start = t.start_state
            goal  = t.goal_state
            expander = grid_expander.grid_expander(domain)
            heuristic = gridmap_h.pigelet_heuristic

        elif t.domain_type == DOMAIN_TYPE.n_puzzle:
            domain = n_puzzle.n_puzzle(t.domain)
            domain.set_start(t.start_state)
            start = domain.start_state()
            goal = domain.goal_state()
            expander = n_puzzle_expander.n_puzzle_expander(domain)
            heuristic = n_puzzle_h.pigelet_heuristic
        elif t.domain_type == DOMAIN_TYPE.graph:
            domain = graph.graph(t.domain)
            expander = graph_expander.graph_expander(domain)
            heuristic = graph_h.pigelet_heuristic
            start = domain.get_vertex(t.start_state)
            goal = domain.get_vertex(t.goal_state)

        # prepare open list and heuristic_function for different strategy
        heuristic_function = None
        strategy = args.strategy
        if strategy == "depth":
            open_list = stack()
        elif strategy == "breadth":
            open_list = queue()
        elif strategy == "uniform":
            open_list = bin_heap(search_node.compare_node_g)
        elif strategy =="a-star":
            open_list =  bin_heap(search_node.compare_node_f)
            heuristic_function = heuristic
        elif strategy == "greedy-best":
            open_list =  bin_heap(search_node.compare_node_h)
            heuristic_function = heuristic

        # prepare search engine for different framework
        engine: base_search.base_search = None
        if args.framework == "tree":
            engine = tree_search.tree_search
        elif args.framework == "graph":
            engine = graph_search.graph_search
        elif args.framework == "iterative" :
            engine = iterative_deepening.iterative_deepening
            open_list = stack()
        search_engine = engine(open_list,expander,heuristic_function = heuristic_function,time_limit=args.time_limit)

    search_engine.heuristic_weight = args.heuristic_weight

    if args.framework == "iterative":
        if args.strategy == "depth":
            search_engine.get_path(start,goal,threshold_type=iterative_deepening.ID_threshold.depth)
        elif args.strategy == "a-star":
            search_engine.get_path(start,goal,threshold_type=iterative_deepening.ID_threshold.cost)
    elif args.framework == "tree":
        search_engine.get_path(start,goal,depth_limit=args.depth_limit,cost_limit=args.cost_limit)
    else:
        search_engine.get_path(start, goal)
    return search_engine
