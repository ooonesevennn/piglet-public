import os,sys
sys.path.extend("../")
from lib_piglet.domains import gridmap
from lib_piglet.expanders.grid_expander import grid_expander
from lib_piglet.search.tree_search import tree_search
from lib_piglet.search.graph_search import graph_search
from lib_piglet.utils.data_structure import bin_heap,stack,queue
from lib_piglet.search.search_node import compare_node_g, compare_node_f
from lib_piglet.cli.cli_tool import print_header, statistic_template

file_folder = os.path.dirname(os.path.abspath(__file__))
inputfile = os.path.join(file_folder, "gridmap/empty-16-16.map")



gm = gridmap.gridmap(inputfile)

expander = grid_expander(gm)
search = tree_search(bin_heap(compare_node_g), expander)
print_header()
path = search.get_path((1,2),(10,2))
print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], str(search.solution_)))
search = tree_search(queue(), expander)
path = search.get_path((1,2),(10,2))
print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], str(search.solution_)))
search = graph_search(queue(), expander)
path = search.get_path((1,2),(10,2))
print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], str(search.solution_)))
search = graph_search(stack(), expander)
path = search.get_path((1,2),(10,2))
print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], str(search.solution_)))
search = graph_search(bin_heap(compare_node_g), expander)
path = search.get_path((1,2),(10,2))
print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], str(search.solution_)))

search = graph_search(bin_heap(compare_node_f), expander,heuristic_function=gridmap.gridmap_manhattan_heuristic)
path = search.get_path((1,2),(10,2))
print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], str(search.solution_)))

search = graph_search(bin_heap(compare_node_f), expander,heuristic_function=gridmap.gridmap_straight_heuristic)
path = search.get_path((1,2),(10,2))
print(statistic_template.format("","",*[str(x) for x in search.get_statistic()], str(search.solution_)))








