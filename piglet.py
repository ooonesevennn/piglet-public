from lib_piglet.cli.cli_tool import *
from lib_piglet.cli.run_tool import *
import os
def main():

    args = parse_args()
    if args.problem == None and sys.stdin.isatty():
        print("err; You must provide a problem scenario file or provide problem through standard input", file = sys.stderr)
        print("piglet.py -h for help", file=sys.stderr)
        exit(1)

    header_readed = False
    if not sys.stdin.isatty():
        source = sys.stdin
    else:
        if not os.path.exists(args.problem):
            print("err; Given problem scenario file does not exist: {}".format(args.problem), file = sys.stderr)
            exit(1)
        source = open(args.problem)

    print_header()
    if args.output_file:
        out = open(args.output_file, "w+")
        out.write(csv_header())

    domain_type = None
    for line in source:
        content = line.strip().split()
        if len(content) == 0 or content[0] == "#":
            continue
        if not header_readed:
            if len(content) != 2 or content[0]!= "domain" or content[1] not in domain_types:
                print("err; The first line of input source must be domain type. eg. domain octile", file = sys.stderr)
                print("Supported domains are: [{}]".format(",".join(domain_types)), file = sys.stderr)
                exit(1)
            if content[1] == "n-puzzle":
                domain_type = DOMAIN_TYPE.n_puzzle
            elif content[1] == "grid4":
                domain_type = DOMAIN_TYPE.gridmap
            else:
                print("err; Unknown domain type: {}".format(content[1]),file=sys.stderr)
                exit(1)
            header_readed = True
            continue

        task = parse_problem(content, domain_type)
        search = run_task(task, args)
        print(statistic_string(args,search))
        if args.output_file:
            out.write(statistic_csv(args,search))

    if args.output_file:
        out.close()





        
if __name__ == "__main__":
    main()



