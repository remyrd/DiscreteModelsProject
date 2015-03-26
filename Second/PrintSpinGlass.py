from __future__ import print_function
from graph import Graph
import sys

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("Usage: python PrintSpinGlass.py <instance>")
	else:
		g = Graph(filename=sys.argv[1])

		print("Spin glass with %d spins and %d interactions" % (len(g.nodes), len(g.edges)))
		print("interactions (edges and weights)")

		for e in g.edges:
			# Note: The attribute names "source", "dest", and "interaction"
			# exist because they are the labels in the input file.
			print("e%d  (%d->%d): %d" % (e.index, e.source, e.dest, e.interaction))
