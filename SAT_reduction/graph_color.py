#!/usr/bin/env python3

## Default executable of a SAT solver (do not change this)
defSATsolver="z3"

## Change this to an executable SAT solver if z3 is not in your PATH or else
## Example (Linux): SATsolver="/home/user/z3-4.13/bin/z3"
## You can also include command-line options if necessary
SATsolver=defSATsolver

import sys
from subprocess import Popen
from subprocess import PIPE
import re
import random
import os
import shutil

gbi = 0
varToStr = ["invalid"]
graph = {}
k = 0
nodes_list = []
node_to_index = {}
def read_graph(file_name):
    global k
    global graph
    global nodes_list
    global node_to_index
    raw_graph = open(file_name, "r").read()
    raw_graph = raw_graph.split("\n")
    if len(raw_graph[0].split()) != 2:
        print("wrong header for input file : <number of nodes> <number of colors>")
        sys.exit(1)
    k = int(raw_graph[0].split()[1])
    raw_graph = raw_graph[1:]
    for line in raw_graph:
        line = line.split()
        graph[line[0]] = set(line[1:])
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







def printClause(cl):
    print(map(lambda x: "%s%s" % (x < 0 and eval("'-'") or eval ("''"), varToStr[abs(x)]) , cl))

def gvi(name):
    global gbi
    global varToStr
    gbi += 1
    varToStr.append(name)
    return gbi

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


## Main function to compute the clauses from the variables.
def genNodesConstr(vars):

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
            for c_j in range(c_i+1,k):
                clauses.append([-vars["P%d_k%d" % (p, c_i)], -vars["P%d_k%d" % (p, c_j)]])

    # not-adjacent color constraint
    for p_i in range(len(nodes_list)):
        for n in graph[nodes_list[p_i]]:
            for c_i in range(k):
                clauses.append([-vars["P%d_k%d" % (p_i, c_i)], -vars["P%d_k%d" % (node_to_index[n], c_i)]])

    return clauses

# A helper function to print the cnf header
def printHeader(rules):
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

# This function is invoked when the python script is run directly and not imported
if __name__ == '__main__':
    path = shutil.which(SATsolver.split()[0])
    if path is None:
        if SATsolver == defSATsolver:
            print("Set the path to a SAT solver via SATsolver variable on line 9 of this file (%s)" % sys.argv[0])
        else:
            print("Path '%s' does not exist or is not executable." % SATsolver)
        sys.exit(1)

    # This is for reading in the arguments.
    if len(sys.argv) != 2:
        print("Usage: %s <file name>" % sys.argv[0])
        sys.exit(1)

    file_name = sys.argv[1]

    read_graph(file_name)

    vars = gen_vars()

    rules = genNodesConstr(vars)
    #
    head = printHeader(rules)
    rls = printCnf(rules)

    # here we create the cnf file for SATsolver
    fl = open("tmp_prob.cnf", "w")
    fl.write("\n".join([head, rls]) + "\n")
    fl.close()

    # this is for runing SATsolver
    ms_out = Popen([SATsolver + " tmp_prob.cnf"], stdout=PIPE, shell=True).communicate()[0]

    res = ms_out.decode('utf-8')
    print(res)
    res = res.strip().split('\n')

    # if it was satisfiable, we want to have the assignment printed out
    if res[0] == "s SATISFIABLE":
        # First get the assignment, which is on the second line of the file, and split it on spaces
        # Read the solution
        lines = res
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
            print("satisfiable", solution)
        else:
            print("unsatisfiable")

