# utils.binary_heap/Binary_Heap.py
# Implements a binary heap data structure. It maintain the data in a priority order and pop the top (min) item.
#

#
# @author: mike
# @created: 2020-07-16
#


class bin_heap:
    """
    Binary heap maintain highest priority items at the front of the queue
    and the lowest priority items at the back.
    """
    heapList: list = [0]
    currentSize: int = 0

    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def insert(self, item):
        """
        Insert an item to the heap, and maintain heap structure.
        :param item:
        :return:
        """
        self.heapList.append(item)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def push(self, item):
        """
        Do same thing as insert. Push an item into the heap and update the structure
        :param item:
        :return:
        """
        self.insert(item)

    def pop(self):
        """
        Pop the top item of the heap and update the heap to maintain heap strucure.
        :return:
        """
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def build(self, alist:list):
        """
        Use a list to initialize the heap.
        :param alist:
        :return:
        """
        if type(alist) != list:
            raise Exception("Given argument is not list")
        i = len(alist) // 2
        self.heapList = [0] + alist[:]
        self.currentSize = len(alist)
        while (i > 0):
            self.percDown(i)
            i = i - 1

    def size(self):
        """
        Return the size of the heap.
        :return int: size of the heap
        """
        return self.currentSize

    def empty(self):
        """
        Return true if heap is empty
        :return bool: is the heap empty.
        """
        return len(self.heapList) == 1

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i // 2]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def minChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i * 2] < self.heapList[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1
