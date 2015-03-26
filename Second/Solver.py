# coding: utf-8

# T-79.4101 Discrete Models and Search
# Aalto University

# Some demo code to print out a lp_solve-compatible encoding for
# the independent set problem for a given graph instance

from __future__ import print_function
from graph import Graph
import sys

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("Usage: python IndependentSetLP.py <instance>")
	else:
		# Read graph instance from given file
		g = Graph(filename=sys.argv[1])

		obj_func = "min: "
		constraints = ""
		variables = "bin "
		for n in range(len(g.nodes)):
			variables += "n"+str(n+1)+", "
		for e in g.edges:
			#objective function
			if e.interaction == -1:
				obj_func +=" +b"+str(e.source)+str(e.dest)+" -a"+str(e.source)+ str(e.dest)
			else:
							
				obj_func +=" -b"+str(e.source)+str(e.dest)+" +a"+str(e.source)+str( e.dest)
			
			#constraints
			constraints += "a"+str(e.source)+str(e.dest)+" = n"+str(e.source)+" +n"+str(e.dest)+";\nb"+str(e.source)+str(e.dest)+" = -1 + a"+str(e.source)+str(e.dest)+";\n"
			#variables
			variables += "a"+str(e.source)+str(e.dest)+", b"+str(e.source)+str(e.dest)+", "
		variables = variables[: -2]
		print(obj_func+";")
		print(constraints)			
		print(variables+";")

