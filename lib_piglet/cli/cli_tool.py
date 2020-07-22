# cli/cli_tools.py
# This module provides tools for cli interface
#
# @author: mike
# @created: 2020-07-19

import sys, argparse, os
from enum import IntEnum


# Describe parameters in arg parser result. For IDE convenient.
class args_interface:
    problem: str
    framework: str
    strategy: str
    time_limit: int
    output_file: str
    scenario: str
    depth_limit:int


# Describe domain type enum
class DOMAIN_TYPE(IntEnum):
    gridmap = 0
    n_puzzle = 1


# Describe task class.
class task:
    domain: str
    domain_type: int
    start_state = None
    goal_state = None


framework_choice = ["tree",
                    "graph",
                    "iterative-depth"
                    ]

strategy_choice = ["breath",
                   "depth",
                   "uniform",
                   "a-star",
                   "greedy-best"
                    ]
domain_types = ["grid4",
                 "n-puzzle"
                 ]

statistic_template = "{0:15}| {1:10}| {2:10}| {3:10}| {4:10}| {5:10}| {6:10}| {7:10}| {8:10}| {9:10}| {10:20}| {11:20}"
csv_template = '"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}"\n'



statistic_header = [
    "Framework",
    "Strategy",
    "Status",
    "Cost",
    "Depth",
    "Nodes(exp)",
    "Nodes(gen)",
    "Runtime",
    "start",
    "goal",
    "Problem",
    "Solution"
]


# Print statistic header to screen
def print_header():
    print(statistic_template.format(*statistic_header))


# @return str Statistic header in csv format
def csv_header():
    return csv_template.format(*statistic_header)


# statistic to string
# @return str A string of statistic information
def statistic_string(args,search):
    if args.solution:
        return statistic_template.format(str(args.framework), args.strategy,
                                         *[str(x) for x in search.get_statistic()],
                                         str(search.solution_))
    return statistic_template.format(str(args.framework), args.strategy,
                                     *[str(x) for x in search.get_statistic()],"Hidden")


# statistic to csv
# @return str A csv format string of statistic information
def statistic_csv(args,search):
    if args.solution:
        return csv_template.format(str(args.framework), args.strategy,
                                         *[str(x) for x in search.get_statistic()],
                                         search.solution_)
    return csv_template.format(str(args.framework), args.strategy,
                                     *[str(x) for x in search.get_statistic()], "Hidden")

# Parse arguments from cli interface
# @return argument object
def parse_args():
    parser = argparse.ArgumentParser(description="""
     This is piglet commandline interface. You can use piglet-cli run a variety search algorithms. 
     A problem scenario file must be provided with -p, unless you problems are passed in through stdin.
     The framework is graph search on default. You can switch to tree search by -f tree.
     The strategy is uniform-cost search by default. You can switch to breath first, depth first or A-star by -s.
     """)

    parser.add_argument("-p","--problem", type=str, default=None,
                        help='Specify the problem scenario file. A problem scenario file  ', metavar="/Path/to/scenario_file")

    parser.add_argument("-f", '--framework', type=str, default="graph",
                        choices=framework_choice,
                        help='Specify the search framework you want to use. \
                         Supported frameworks are: [{}].'.format(", ".join(framework_choice)),
                        metavar="graph")

    parser.add_argument("-s", '--strategy', type=str, default=["uniform"],
                        choices=strategy_choice,
                        help='Specify the search strategy you want to use.\
                          Supported strategies are: [{}]. If using strategy "depth" and framework "iterative-depth",\
                           a maximum depth limit also need to be specified after "depth".'.format(", ".join(strategy_choice)), metavar="uniform")

    parser.add_argument("-t", '--time-limit', type=int, default=sys.maxsize,
                        help='Specify the time-limit for the search. (seconds)', metavar=30)

    parser.add_argument("-o", "--output-file", type=str, default=None,
                        help="Output results to a file")

    parser.add_argument("--solution", default=False,action="store_true",
                        help="Print/write solution")


    args , unknown = parser.parse_known_args()
    args:args_interface = args
    args.depth_limit = None
    if args.framework == "iterative-depth":
        if args.strategy != "a-star" and args.strategy != "depth":
            print("err; With iterative-deepening search, the strategy can only be depth or a-star ", file = sys.stderr)
            exit(1)
        if args.strategy == "depth":
            if len(unknown) == 0 or not unknown[0].isnumeric():
                print("err; With iterative-deepening depth first search, you must specify a maximum depth limit followed by 'depth'.", file=sys.stderr)
                exit(1)
            args.depth_limit = int(unknown[0])
    return args


# Parse individual problem to task
# @param problem. A list of scenario entry
# @return task A task object
def parse_problem(problem: list,domain_type:int):
    ta = task()
    ta.domain_type = domain_type
    if domain_type == DOMAIN_TYPE.n_puzzle:
        try:
            ta.domain = int(problem[0])
        except:
            print("err; Cannot convert {} to puzzle width".format(problem[0]),file=sys.stderr)
            exit(1)
        ta.start_state = problem[1].split(",")
    elif domain_type == DOMAIN_TYPE.gridmap:
        ta.domain = problem[1]
        if len(problem) < 9:
            print("err; the length of an entry of grid problem should be 9. Check the sample grid scenario format",file=sys.stderr)
            exit(1)
        try:
            ta.start_state = (int(problem[4]), int(problem[5]))
            ta.goal_state = (int(problem[6]), int(problem[7]))
        except:
            print("err; Cannot convert {} {} {} {} to coordinates".format(*problem[4:8]),file=sys.stderr)
            exit(1)
    else:
        print("err; Unknown domain type", file=sys.stderr)
        exit(1)
    return ta








