from lib_piglet.utils.data_structure import bin_heap
from lib_piglet.search.search_node import search_node
from typing import Callable, Dict

class item_handle:
    def __init__(self):
        self.focal_handle = None
        self.open_handle = None



"""
The default compare function for FOCAL.
You could modify it to observe the changes on FOCAL search behavior.
"""
def compare_function_2(a: search_node, b:search_node):
    return a.h_ >= b.h_


"""
This data structure maintains two priority queue, the focal list and open list. 
It will track the value of f_min and w*f_min and decide where a node will be stroed.
"""
class focal_priority_queue():

    

    def __init__(self, compare_function_1:Callable, compare_function_2 = compare_function_2, weight : float = 1.0):
        self.weight:float = weight # The suboptimality weight
        self.focal: bin_heap = bin_heap(compare_function_2)
        self.open: bin_heap = bin_heap(compare_function_1)
        self.f_min = None
        self.w_f_min = None
        self.id = 0 # The id of the next item inserted to FOCAL or OPEN
        
        # For the item with an id, use this dictionary to store the corresponding handle of the item in FOCAL or in OPEN 
        # We need to use handle to tell bin_heap who to increase/decrease
        self.handles: Dict[int, item_handle] = {} 
    
    def push(self, item: search_node) -> int:
        if self.f_min == None:
            self.f_min = item.f_
            self.w_f_min = item.f_ * self.weight
        id = self.id
        self.id += 1

        # Create the corresponding object to store the open handle and focal handle for the item
        # When you push a node to OPEN/FOCAL you should record the returned handle to open_handle/focal_handle to this object
        # So that in increase/decrease function, we know what handle to pass to OPEN/FOCAL for increase/decrease
        self.handles[id] = item_handle()

        # The id of the item will also be recored in the search node, 
        # so that when you pop a node from OPEN/FOCAL you can access the id and
        # use it to find corresponding item_handle object in self.handles
        item.priority_queue_handle_ = id

        if item.f_ >= self.f_min and item.f_ <= self.w_f_min:
            self.handles[id].focal_handle =  self.focal.push(item)
        else:
            self.handles[id].open_handle = self.open.push(item)
        
        if self.focal.size() == 0:
            self.update_focal()
        return id
        
    def pop(self)->search_node:
        """
        Pop the top node from FOCAL. 
        Don't forget to remove the corresponding heap_handle from the FOCAL.
        """
        node: search_node = self.focal.pop()
        self.handles.pop(node.priority_queue_handle_)
        if self.focal.size() == 0:
            self.update_focal()
        return node

    
    def update_focal(self):
        """
        This function is used to update the f_min and w_f_min.
        Then it will bring nodes in OPEN with f_ <= w_f_min to FOCAL
        Remember to update the open_handle/focal_handle when you move node from one to another
        """
        if len(self.focal)!= 0:
            return
        if len(self.open) == 0:
            return

        self.f_min = self.open.top().f_
        self.w_f_min = self.f_min * self.weight
        while len(self.open) != 0 and self.open.top().f_ <= self.w_f_min:
            top:search_node = self.open.pop()
            self.handles[top.priority_queue_handle_].open_handle = None
            self.handles[top.priority_queue_handle_].focal_handle = self.focal.push(top)
    
    def decrease(self, handle: int):
        h = self.handles[handle]
        if h.focal_handle!= None:
            self.focal.decrease(h.focal_handle)
        if h.open_handle!= None:
            self.open.decrease(h.open_handle)
    
    def increase(self, handle: int):
        h = self.handles[handle]
        if h.focal_handle!= None:
            self.focal.increase(h.focal_handle)
        if h.open_handle!= None:
            self.open.increase(h.open_handle)

    def clear(self):
        self.open.clear()
        self.focal.clear()
        self.handles.clear()
        self.f_min = None
        self.w_f_min = None
        self.id = 0 

        
    def __len__(self):
        return self.focal.size() + self.open.size()


            



        
        
        
    

            
