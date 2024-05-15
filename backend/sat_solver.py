import sys
from subprocess import Popen, PIPE
import re

# Global variables
gbi = 0
varToStr = ["invalid"]
graph = {}
k = 0
nodes_list = []
node_to_index = {}


def read_graph(file_name):
    global k, graph, nodes_list, node_to_index
    raw_graph = open(file_name, "r").read()
    raw_graph = raw_graph.split("\n")
    if len(raw_graph[0].split()) != 2:
        print("wrong header for input file : <number of nodes> <number of colors>")
        sys.exit(1)
    k = int(raw_graph[0].split()[1])
    raw_graph = raw_graph[1:]
    for line in raw_graph:
        if not line:
            continue
        line = line.split()
        n = str(line[0])
        if n in graph:
            graph[n].update(line[1:])
        else:
            graph[n] = set(line[1:])
        for v in line[1:]:
            v = str(v)
            if v in graph:
                graph[v].add(line[0])
            else:
                graph[v] = set(line[0])

    nodes_list = list(graph.keys())
    nodes_list.sort()
    for n in range(len(nodes_list)):
        node_to_index[nodes_list[n]] = n


def gen_vars():
    varMap = {}

    # Insert here the code to add mapping from variable numbers to readable variable names.
    # A single variable with a human readable name "var_name" is added, for instance, as follows:
    #    varMap["var_name"] = gvi("var_name")

    for p in range(len(graph.keys())):
        for c in range(k):
            vs = "P%d_k%d" % (p, c)
            varMap[vs] = gvi(vs)
    return varMap


def generate_constraint(vars):
    clauses = []

    # at least one color constraint
    for p in range(len(nodes_list)):
        node_colors = []
        for c in range(k):
            node_colors.append(vars["P%d_k%d" % (p, c)])
        clauses.append(node_colors)

    # at most one color constraints
    for p in range(len(nodes_list)):
        for c_i in range(k):
            for c_j in range(c_i + 1, k):
                clauses.append([-vars["P%d_k%d" % (p, c_i)], -vars["P%d_k%d" % (p, c_j)]])

    for p_i in range(len(nodes_list)):
        for n in graph[nodes_list[p_i]]:
            for c_i in range(k):
                clauses.append([-vars["P%d_k%d" % (p_i, c_i)], -vars["P%d_k%d" % (node_to_index[n], c_i)]])

    return clauses


def run_sat_solver(sat_solver_path, constraint, head, rls):
    # here we create the cnf file for SATsolver
    fl = open("tmp_prob.cnf", "w")
    fl.write("\n".join([head, rls]) + "\n")
    fl.close()

    # this is for runing SATsolver
    ms_out = Popen([sat_solver_path + " tmp_prob.cnf"], stdout=PIPE, shell=True).communicate()[0]

    res = ms_out.decode('utf-8')
    print(res)
    res = res.strip().split('\n')
    return res


def decode_solution(output):
    lines = output
    if lines[0] == "s SATISFIABLE":
        solution = {}
        assignment = map(int, lines[1].split()[1:-1])
        for var in assignment:
            if var > 0:
                var_name = varToStr[abs(var)]
                match = re.match(r"P(\d+)_k(\d+)", var_name)
                if match:
                    node_index, color_index = map(int, match.groups())
                    node_name = nodes_list[node_index]
                    solution[node_name] = color_index
        return "satisfiable", solution
    else:
        return "unsatisfiable", {}


# A helper function to print the cnf header
def printHeader(rules, vars):
    global gbi
    global varToStr
    n = len(rules)
    str = ""
    for p in range(len(graph.keys())):
        for c in range(k):
            str += "c %s ~  P%d_k%d ~ %d\n" % (nodes_list[p], p, c, vars["P%d_k%d" % (p,c)])
    for cl in rules:
        print("c ", end='')
        for l in cl:
            print(("!" if (l < 0) else " ") + varToStr[abs(l)], "", end='')
        print("")
    print("")
    str += "p cnf %d %d" % (gbi, n)
    return str


# A helper function to print a set of clauses cls
def printCnf(cls):
    return "\n".join(map(lambda x: "%s 0" % " ".join(map(str, x)), cls))


def printClause(cl):
    print(map(lambda x: "%s%s" % (x < 0 and eval("'-'") or eval("''"), varToStr[abs(x)]), cl))


def gvi(name):
    global gbi
    global varToStr
    gbi += 1
    varToStr.append(name)
    return gbi


def solve_sat_problem(file_name, sat_solver_path="z3"):
    read_graph(file_name)
    vars = gen_vars()
    rules = generate_constraint(vars)
    head = printHeader(rules, vars)
    rls = printCnf(rules)
    output = run_sat_solver(sat_solver_path, rules, head, rls)
    status, solution = decode_solution(output)
    return status, solution
