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


framework_choice = ["tree-search",
                    "graph-search",
                    "uniform-cost-search"
                    ]

strategy_choice = ["best-first",
                   "dfs",
                   "bfs",
                    ]
domain_types = ["octile",
                 "n-puzzle"
                 ]

statistic_template = "{0:10}| {1:10}| {2:10}| {3:10}| {4:10}| {5:10}| {6:10}| {7:10}| {8:10} "
csv_template = '"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}"\n'



statistic_header = [
    "Status",
    "Cost",
    "Depth",
    "Nodes(exp)",
    "Nodes(gen)",
    "Runtime",
    "start",
    "goal",
    "Problem"]


# Print statistic header to screen
def print_header():
    print(statistic_template.format(*statistic_header))


# @return str Statistic header in csv format
def csv_header():
    return csv_template.format(*statistic_header)

# Parse arguments from cli interface
# @return argument object
def parse_args():
    parser = argparse.ArgumentParser(description="""
     This is piglet commandline interface. You can use piglet-cli run a variety search algorithms.
     """)
    parser.add_argument("-p", "--problem", type=str, nargs="*",default=None,
                         help = "Specify the problem to solve. You should provide a domain file. \
                            Support domain file include N-puzzle file and gridmap file.\
                            For grid map problem, also provide start coordinate (eg. 11,14 ) and goal coordinate.")

    parser.add_argument("-scen","--scenario", type=str, default=None,
                        help='Specify the scenario file. A scenario file  ', metavar="/path/to/scenario-file")

    parser.add_argument("-f", '--framework', type=str, default="uniform-cost-search",
                        choices=framework_choice,
                        help='Specify the search framework you want to use. \
                         Supported frameworks are: [{}]'.format(", ".join(framework_choice)),
                        metavar="tree-search")

    parser.add_argument("-s", '--strategy', type=str, default=["best-first"],
                        nargs="*",
                        choices=strategy_choice,
                        help='Specify the search strategy you want to use.\
                          Supported strategies are: [{}]'.format(", ".join(strategy_choice)), metavar="best-first")

    parser.add_argument("-t", '--time-limit', type=int, default=sys.maxsize,
                        help='Specify the time-limit for the search. (seconds)', metavar=30)

    parser.add_argument("-o", "--output-file", type=str, default=None,
                        help="Output results to a file")

    args: args_interface = parser.parse_args()
    return args


# Parse scenario file.
# @param file Path to scenario file
# @return [task] A list of tasks.
def parse_scenario(file):
    if not os.path.exists(file):
        raise FileNotFoundError("Can't find scenario file: {}".format(file))
    file = open(file)
    header = file.readline().strip().split()
    tasks = []
    for line in file:
        content = line.strip().split()
        if len(content)==0:
            continue
        ta = parse_problem(content)
        tasks.append(ta)
    return tasks


# Parse individual problem to task
# @param problem
# @return task A task object
def parse_problem(problem):
    ta = task()
    ta.domain = problem[0]

    if not os.path.exists(ta.domain):
        raise FileNotFoundError("Problem file")
    with open(ta.domain) as f:
        header = f.readline().strip().split()
        if len(header) != 2 or header[0] != "type" or header[1] not in domain_types:
            raise TypeError("Can't recognize the type of this domain file. Supported domain type are: [{}]".format(
                ", ".join(domain_types)))

        if header[1] == "n-puzzle":
            ta.domain_type = DOMAIN_TYPE.n_puzzle
        elif header[1] == "octile":
            ta.domain_type = DOMAIN_TYPE.gridmap
            start = problem[1].split(",")
            goal = problem[2].split(",")
            if len(start) != 2 or len(goal) != 2:
                raise Exception("wrong format for start and goal location")
            try:
                ta.start_state = tuple(int(x) for x in start)
                ta.goal_state = tuple(int(x) for x in goal)
            except:
                raise ValueError("Start or goal is not number")
    return ta








