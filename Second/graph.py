# coding: utf-8

# T-79.4101 Discrete Models and Search
# Aalto University

# This module contains some helper code to read DIMACS files. You may assume
# that the automated checker has an equivalent module named graph.py available.









"""
It shouldn't be necessary to read and understand the source code in this file
(but then, it's not very long).

For examples, you could instead read IndependentSetLP.py and PrintSpinGlass.py.
"""










class GraphFileFormatError(ValueError):
	pass


class Graph:

	def __init__(self, filename):
		"""
		Parameters
		----------
		filename : Name of a graph file in (extended) DIMACS format.
		"""

		self._nodes = []
		self._edges = []

		self._nodes_tuple = None
		self._edges_tuple = None

		with open(filename) as f:
			line = f.readline()

			# First line tells us if the file uses standard or extended DIMACS format
			tokens = line.split()
			if len(tokens) == 4 and tokens[0] == "p" and tokens[1] == "edge":
				# Normal DIMACS format
				fileformat = "normal"
			elif tokens[0] == "c" and tokens[1] == "f":
				# Extended DIMACS format
				fileformat = "extended"
				# Skip the first " "
				quote_tokens = line.split('"')
				# c f int int " " "label1 label2 ..."
				# Note: this supports the all-lowercase ASCII labels as used by
				# the input files for the Discrete Models and Search course assignment.
				# More generally, the labels should be valid Python attribute names.
				label_str = quote_tokens[3]
				self._labels = label_str.split()
			else:
				raise GraphFileFormatError("Unknown graph file format")

			# Additionally, the number of nodes/edges is given on the first line
			num_nodes = int(tokens[2])
			num_edges = int(tokens[3])

			if num_nodes < 0:
				raise GraphFileFormatError("Negative number of nodes")
			if num_edges < 0:
				raise GraphFileFormatError("Negative number of edges")

			# Add enough nodes
			for i in xrange(1, num_nodes+1):
				self._nodes.append(Node(index=i))

			# There is a line for each edge
			# In the "normal" format, the line contains the source and the destination node indices
			# In the "extended" format, the numbers may be arbitrarily labeled and there is actually
			# no clear connection to the nodes of the graph, so we will just introduce a new (integer)
			# property for each label. For an example, see PrintSpinGlass.py.
			for edge_index in xrange(1, num_edges+1):
				line = f.readline()
				edge = self._parse_edge(line, edge_index, fileformat)
				if edge:
					self._edges.append(edge)
				else:
					raise GraphFileFormatError("Could not parse edge line")

	def _parse_edge(self, line, index, fileformat="normal"):
		# Note: this code assumes that all values are integers.
		tokens = line.split()

		if tokens[0] == 'e':
			if fileformat == "normal":
				if len(tokens) != 3:
					raise GraphFileFormatError("Invalid edge line: %s" % line)
				return Edge(index, source=int(tokens[1]), dest=int(tokens[2]))

			elif fileformat == "extended":
				if len(tokens) != len(self._labels) + 1:
					raise GraphFileFormatError("Invalid edge line (extended format): %s" % line)
				# Generate dictionary where the values on this edge line are associated
				# with the appropriate labels from earlier
				d = {}
				for i in xrange(len(self._labels)):
					d[self._labels[i]] = int(tokens[i+1])
				return Edge(index, **d)

	@property
	def nodes(self):
		"""Return a tuple of nodes in this graph."""
		if self._nodes_tuple is None:
			self._nodes_tuple = tuple(self._nodes)
		return self._nodes_tuple

	@property
	def edges(self):
		"""Returns a tuple of edges in this graph."""
		if self._edges_tuple is None:
			self._edges_tuple = tuple(self._edges)
		return self._edges_tuple


class Node(object):
	def __init__(self, index):
		"""
		Parameters
		----------
		index : int
			Node index. Must be unique in the graph.
		"""
		self._index = int(index)

	@property
	def index(self):
		"""Return the index of this Node, unique in the graph and set at creation time.

		Example:
		>>> node = Node(index=999)
		>>> node.index
		999
		>>> node.index = 1000
		AttributeError: can't set attribute
		"""
		return self._index


class Edge(object):
	def __init__(self, index, **kwargs):
		self._index = int(index)
		self.__dict__.update(kwargs)

	@property
	def index(self):
		return self._index
