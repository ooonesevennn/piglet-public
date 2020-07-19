from lib_piglet.domains.gridmap import gridmap, grid_action
from lib_piglet.cli.cli_tool import *
from lib_piglet.cli.run_tool import *
import os
def main():

    args = parse_args()
    if args.problem == None and args.scenario == None:
        raise Exception("You must provide a problem file or a scenario file")

    tasks = []
    if args.problem != None:
        tasks.append(parse_problem(args.problem))
    else:
        tasks = parse_scenario(args.scenario)

    print("Framework:\t", args.framework)
    print("Strategy:\t", " ".join(args.strategy))
    print_header()
    if args.output_file:
        out = open(args.output_file,"w+")
        out.write(csv_header())
    for t in tasks:
        search = run_task(t,args)
        search.print_statistic()
        if args.output_file:
            out.write(csv_template.format(*[str(x) for x in search.get_statistic()]))

    if args.output_file:
        out.close()





        
if __name__ == "__main__":
    main()



