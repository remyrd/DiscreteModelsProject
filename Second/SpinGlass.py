# coding: utf-8

# T-79.4101 Discrete Models and Search
# Aalto University

from __future__ import print_function
from graph import Graph
import sys

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("Usage: python SpinGlass.py <instance>")
	else:
		g = Graph(filename=sys.argv[1])

		obj_func = "min: "
		constraints = ""
		variables = "free "
		for n in range(len(g.nodes)):
			variables += "n"+str(n+1)+", "
		variables = variables[:-2]
		variables += ";\nint "
		for n in range(len(g.nodes)):
			variables += "x"+str(n+1)+", "
		for e in g.edges:
			i = str(e.source)
			j = str(e.dest)
			#objective function
			if e.interaction == -1: #different nodes --> x1*x2 ideally -1
				obj_func +=" -2a"+i+j+" +1"
			else:
							
				obj_func +=" +2a"+i+j+" -1"
			
			#constraints
			constraints += "a"+i+j+" = x"+i+" +x"+j+"-2b"+i+j+";\nb"+i+j+" < x"+i+";\nb"+i+j+" < x"+j+";\nb"+i+j+"> x"+i+"+ x"+j+" - 1;\nb"+i+j+">0;\n"
			variables+="a"+i+j+", b"+i+j+", "
		for n in range(len(g.nodes)):
			constraints += "x"+str(n+1)+">0;\n"
			constraints+="x"+str(n+1)+"<1;\n"
			constraints += "x"+str(n+1)+"= 0.5n"+str(n+1)+" + 0.5;\n"
		variables = variables[: -2]
		print(obj_func+";")
		print(constraints)			
		print(variables+";")

