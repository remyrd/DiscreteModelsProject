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

		# Variables n1, n2, n3... for the nodes
		# n1 = 0 means node 1 is *not* in the independent set
		# n1 = 1 means node 1 *is* in the independent set

		# We want to maximise the size of the independent set
		nodelist = ["n%d" % node.index for node in g.nodes]
		# This will print out the line max: n1 + n2 + n3 + ...;
		line = "max: %s;" % " + ".join(nodelist)
		print(line)

		# Independence constraint: no two nodes chosen may be connected by an edge
		for edge in g.edges:
			print("n%d+n%d <= 1;" % (edge.source, edge.dest))

		# All variables are binary
		line = "bin %s;" % ", ".join(nodelist)
		print(line)

		# Or alternatively, without using binary variables:

		# The values must be between 0 and 1
		# lp_solve automatically assumes the variables to be non-negative, so we
		# just need to specify the upper bound here
		#for var in nodelist:
		#	print("%s <= 1;" % (var))

		# Additionally, all variables must be integers
		#line = "int %s;" % ", ".join(nodelist)
		#print(line)

