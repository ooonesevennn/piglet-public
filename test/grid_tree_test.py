import os,sys
sys.path.extend("../")
from lib_piglet.domains import gridmap
from lib_piglet.expanders.grid_expander import grid_expander
from lib_piglet.search.tree_search import tree_search
from lib_piglet.search.graph_search import graph_search
from lib_piglet.search.uniform_cost_search import uniform_cost_search
from lib_piglet.utils.data_structure import bin_heap,stack,queue


file_folder = os.path.dirname(os.path.abspath(__file__))
inputfile = os.path.join(file_folder, "gridmap/empty-16-16.map")



gm = gridmap.gridmap()
gm.load(inputfile)

expander = grid_expander(gm)
search = tree_search(bin_heap(), expander)
search.print_header()
path = search.get_path((1,2),(10,2))
search.print_statistic()
search = tree_search(queue(), expander)
path = search.get_path((1,2),(10,2))
search.print_statistic()
search = graph_search(queue(), expander)
path = search.get_path((1,2),(10,2))
search.print_statistic()
search = graph_search(stack(), expander)
path = search.get_path((1,2),(10,2))
search.print_statistic()
search = graph_search(bin_heap(), expander)
path = search.get_path((1,2),(10,2))
search.print_statistic()
search = uniform_cost_search(queue(), expander)
path = search.get_path((1,2),(10,2))
search.print_statistic()
search = uniform_cost_search(stack(), expander)
path = search.get_path((1,2),(10,2))
search.print_statistic()
search = uniform_cost_search(bin_heap(), expander)
path = search.get_path((1,2),(10,2))
search.print_statistic()






