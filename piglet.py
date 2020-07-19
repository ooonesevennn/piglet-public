import sys, argparse
from lib_piglet.domains.gridmap import gridmap, grid_action

def main(argv):

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()

    inputfile = ''
    outputfile = ''

    print('Input file is ', inputfile)

    ga = grid_action.grid_action();
    gm = gridmap.gridmap()
    gm.load(inputfile)
    gm.write()

    print("1,1")
    for move in gm.get_moves(1,1):
        move.print()

    print("2,2")
    for move in gm.get_moves(2,2):
        move.print()

    print("0,0")
    for move in gm.get_moves(0,0):
        move.print()
        
if __name__ == "__main__":
    main(sys.argv[1:])



