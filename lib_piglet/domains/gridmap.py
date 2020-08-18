# gridmap
# 
# Reads and writes 2d grid maps.
#  -----> y
# |
# |
# V x
# For gridmap, state is pair of (x,y) tuple
# @author: dharabor
# @created: 2020-07-14
#

import sys, math


class gridmap:
    map: list
    height_: int
    width_: int
    map_size_: int
    domain_file_: str
    
    def __init__(self,filename: str):
        self.map_ = []
        self.height_ = int(0)
        self.width_ = int(0)
        self.map_size_ = int(0)
        self.load(filename)

    # Load map in the map instance
    # @param filename The path to map file.
    def load(self, filename: str):
        self.domain_file_ = filename
        map_fo = open(filename, "r")

        if(self.__parse_header(map_fo) == -1):
            raise Exception("err; invalid map header")

        self.map_ = [ ([None] * int(self.width_)) for x in range(0,int(self.height_)) ]

        i = 0
        while(True):
            char = map_fo.read(1)
            if not char:
                break
            if(char == '\n'):
                continue

            y = int(i % int(self.width_))
            x = int(i / int(self.width_))
            if(char == '.'):
                self.map_[x][y] = True
            else:
                self.map_[x][y] = False
            i += 1

    # Write map tp a file
    def write(self):

        print("type octile")
        print("height " + str(self.height_))
        print("width " + str(self.width_))
        print("map")
 
        for x in range(0, int(self.height_)):
            for y in range(0, int(self.width_)):
                if(self.map_[x][y] == True):
                    print('.', end="")
                else:
                    print('@', end="")
            print()

    # tells whether the tile at location @param index is traversable or not
    # @return True/False
    def get_tile(self, loc: tuple):
        x = loc[0]
        y = loc[1]
        if(x < 0 or x >= self.height_ or y < 0 or y >= self.width_):
            return False
        return self.map_[x][y]

    def __parse_header(self, map_fo):

        tmp = map_fo.readline().strip().split(" ")
        if(tmp[0] != "type" and tmp[1] != "octile"):
            print("not octile map")
            return -1
    
        for i in range(0, 2):
            tmp = map_fo.readline().strip().split(" ")
            if tmp[0] == "height" and len(tmp) == 2:
                self.height_ = int(tmp[1])
            elif tmp[0] == "width" and len(tmp) == 2:
                self.width_ = int(tmp[1])
            else:
                return -1

        tmp = map_fo.readline().strip()
        if(tmp != "map"):
            return -1

    def __str__(self):
        return self.domain_file_

