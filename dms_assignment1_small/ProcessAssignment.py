# coding: utf-8

# This is some demo Python code for reading in a problem instance and
# initial assignment for the first programming assignment of T-79.4101
# Discrete Models and Search, written for Python 2.7.3
#
# Note: the main method here just reads in a problem instance file and the
# initial assignment, and then prints both of them to the specified output
# file.

from __future__ import print_function
import sys

# Just some useful exceptions to raise during parsing
class InstanceError(BaseException):
	pass

class AssignmentError(BaseException):
	pass

class InvalidArgumentException(ValueError):
	pass

class ProcessAssignment:
	"""Stores an instance of the process assignment program."""
	num_resources = 0
	num_machines = 0
	num_processes = 0
	num_services = 0
	num_locations = 0

	# The capacities and the requirements will be presented as lists of
	# tuples. Suppose there are three resources, and two machines. Then
	# the contents of machine_capacities could be [(2, 11, 4), (9, 33, 1)].
	machine_capacities = []
	soft_machine_capacities = []
	process_requirements = []

	# The following are just lists of integers
	machine_locations = []
	service_min_spreads = []
	process_services = []
	process_moving_costs = []

	# This is a list of machines, one for each process
	assignment = None

	def __init__(self, filename=None):
		if filename:
			self._read_instance_file(filename)

	def dump_instance(self, filename=None, mode='w'):
		"""Writes the current instance in human-readable format to 
                a given file or stdout."""

		if filename:
			if mode not in ['a', 'w']:
				raise InvalidArgumentException("Allowed modes are 'a' and 'w'")
			f = open(filename, mode)
		else:
			f = sys.stdout

		print("Problem instance:\n", file=f)
		print("  Resources: %4d" % self.num_resources, file=f)
		print("  Machines: %5d" % self.num_machines, file=f)
		print("  Processes: %4d" % self.num_processes, file=f)
		print("  Services: %5d" % self.num_services, file=f)
		print("  Locations: %4d" % self.num_locations, file=f)

		print("\n  Machine Capacities (soft/hard):\n", file=f)

		for machine in xrange(self.num_machines):
			print("    m: %d" % machine, file=f)
			capacities = [('%d/%d' % t).rjust(10) for t in zip(self.machine_capacities[machine], self.soft_machine_capacities[machine])]
			print("      %s" % "".join(capacities), file=f)

		print("\n  Machine Locations:\n", file=f)

		for machine in xrange(self.num_machines):
			print("    m: %d" % machine, file=f)
			print("        %4d" % self.machine_locations[machine], file=f)

		print("\n  Minimum Service Spreads:\n", file=f)

		for service in xrange(self.num_services):
			print("    s: %d" % service, file=f)
			print("        %4d" % self.service_min_spreads[service], file=f)

		print("\n  Process Requirements:\n", file=f)

		for process in xrange(self.num_processes):
			print("    p: %d" % process, file=f)
			requirements = [('%d' % req).rjust(6) for req in self.process_requirements[process]]
			print("      %s" % "".join(requirements), file=f)

		print("\n  Process Services:\n", file=f)

		for process in xrange(self.num_processes):
			print("    p: %d" % process, file=f)
			print("        %4d" % self.process_services[process], file=f)

		print("\n  Process Moving Costs:\n", file=f)

		for process in xrange(self.num_processes):
			print("    p: %d" % process, file=f)
			print("        %4d" % self.process_moving_costs[process], file=f)

		print("", file=f)

		if f is not sys.stdout:
			f.close()

	def _read_instance_file(self, filename):
		"""Parses an instance file and overwrites any saved values 
                with new data. Note that only very crude error checking is 
                performed here (concerning the values and the formatting of 
                the file). Most things will raise an exception, e.g. if the
		values in the file are not integer, or are outside the 
                allowed range."""
		with open(filename) as instancefile:
			# The first line contains the number of resources
			self.num_resources = int(instancefile.readline().strip())
			# The second line contains the number of machines
			self.num_machines = int(instancefile.readline().strip())

			if (self.num_resources < 1 or self.num_resources > 10):
				raise InstanceError("The number of resources is not within limits")

			if (self.num_machines < 1 or self.num_machines > 500):
				raise InstanceError("The number of machines is not within limits")

			# Initialize some lists (delete any previous data 
                        # that may have been there)
			self.machine_capacities = [0] * self.num_machines
			self.soft_machine_capacities = [0] * self.num_machines
			self.machine_locations = [0] * self.num_machines

			# debug
			print("LOG: read num_resources and num_machines")

			# Next num_machines lines contain the following things:
			# <location> <capacity for resource 
                        # i=1...num_resources> <soft capacity for resource 
                        # i=1...num_resources>
			for machine in xrange(self.num_machines):
				# Split the line at each space character to 
                                # form a list of values
				tokens = instancefile.readline().strip().split()

				if len(tokens) != (1 + 2 * self.num_resources):
					raise InstanceError("Wrong number of values (expected %d, found %d)" % (1 + 2 * num_resources, len(tokens)))

				# First, read the machine location
				location = int(tokens[0])

				if (location < 0 or location > self.num_machines):
					raise InstanceError("Invalid machine location: %d" % location)

				# Here, we're just updating the number of 
                                # locations as we observe more of them. 
                                # The assumption is of course that all 
                                # locations from 1 to n are in use, otherwise 
                                #the number wouldn't technically be accurate.
				if self.num_locations < location + 1:
					self.num_locations = location + 1

				self.machine_locations[machine] = location

				# Then the (hard) capacities
				self.machine_capacities[machine] = tuple([int(t) for t in tokens[1:self.num_resources+1]])
				# ...and the soft capacities
				self.soft_machine_capacities[machine] = tuple([int(t) for t in tokens[self.num_resources+1:]])

				# debug
			print("LOG: read machine locations and capacities")

			# The next line has the number of services
			self.num_services = int(instancefile.readline().strip())

			if (self.num_services < 1 or self.num_services > 2000):
				raise InstanceError("The number of services is not within limits")

			self.service_min_spreads = [0] * self.num_services

			# The next num_services lines contain the minimum 
                        # spreads for each service
			for service in xrange(self.num_services):
				min_spread = int(instancefile.readline().strip())

				if (min_spread < 0 or min_spread > self.num_locations):
					raise InstanceError("Invalid service spread value: %d" % min_spread)
				
				self.service_min_spreads[service] = min_spread

			# debug
			print("LOG: read service spreads")

			# The next line has the number of processes
			self.num_processes = int(instancefile.readline().strip())

			if (self.num_processes < 1 or self.num_processes > 2000):
				raise InstanceError("The number of processes is not within limits")

			self.process_services = [0] * self.num_processes
			self.process_requirements = [0] * self.num_processes
			self.process_moving_costs = [0] * self.num_processes

			# The next num_processes lines contain the 
                        # requirements for each process
			for process in xrange(self.num_processes):
				# Split the line at each space character to 
                                # form a list of values
				tokens = instancefile.readline().strip().split()

				if len(tokens) != (2 + self.num_resources):
					raise InstanceError("Wrong number of values (expected %d, found %d)" % (2 + num_resources, len(tokens)))

				# First, read the service this process 
                                # belongs to
				service = int(tokens[0])

				if (service < 0 or service > self.num_services):
					raise InstanceError("Invalid service value for process: %d" % service)

				self.process_services[process] = service

				# Then, read the requirements this process 
                                # has for each resource
				self.process_requirements[process] = tuple([int(t) for t in tokens[1:self.num_resources+1]])

				# The last value is the moving cost of the 
                                # process
				moving_cost = int(tokens[self.num_resources + 1])

				if (moving_cost < 0 or moving_cost > 1000):
					raise InstanceError("The moving cost is not within limits")

				self.process_moving_costs[process] = moving_cost

			# debug
			print("LOG: read processes")
			print("LOG: finished reading instance")

	def update_assignment(self, filename):
		"""Reads an assignment from a file, overwrites a previous assignment if one existed."""
		with open(filename) as assignmentfile:
			tokens = assignmentfile.readline().strip().split()

			if len(tokens) != self.num_processes:
				raise AssignmentError("Wrong number of assigned processes (expected %d, found %d)" % (self.num_processes, len(tokens)))

			self.assignment = [0] * self.num_processes

			# Parse the machine the process is assigned to
			for process in xrange(self.num_processes):
				self.assignment[process] = int(tokens[process])
		# debug
		print("LOG: finished reading assignment")
		
#=================================== 
# TODO 
#===================================	
	
	def probe_neighbor(self):
		
		#see what is the least moving cost, then swap processes machines if possible
		min_move_cost = index_of.min(self.process_moving_costs) #process with least moving cost
		print ("the minimum cost machine is ", min_move_cost)
		
		
	def test_constraints(self, process_a, process_b):
		# SCCon
		sccon = (self.process_services[process_a] != self.process_services[process_b])
		# SSCon	
	
#====================================

def dump_assignment(assignment, filename=None, mode='w'):
	"""Writes an assignment in human-readable format to a given file or 
        stdout."""

	if filename:
		if mode not in ['a', 'w']:
			raise InvalidArgumentException("Allowed modes are 'a' and 'w'")
		f = open(filename, mode)
	else:
		f = sys.stdout

	print("Assignment (process -> machine):\n", file=f)

	for process in xrange(len(assignment)):
		print("  %4d -> %d" % (process, assignment[process]), file=f)

	print("", file=f)
	if f is not sys.stdout:
		f.close()


if __name__ == "__main__":
	if len(sys.argv) not in [3, 4]:
		print("Usage: python processassignment.py <instance_file> <initial_solution_file> [<output_file>]")
	else:
		# Read the instance and the assignment and initialise a new 
                # ProcessAssignment object
		try:
			assignment = ProcessAssignment(filename=sys.argv[1])
		except BaseException, e:
			print("Could not initialize a ProcessAssignment.", file=sys.stderr)
			print(repr(e), file=sys.stderr)
			sys.exit(1)

		try:
			assignment.update_assignment(filename=sys.argv[2])
		except BaseException, e:
			print("Could not load the initial assignment.", file=sys.stderr)
			print(repr(e), file=sys.stderr)
			sys.exit(1)
		assignment.probe_neighbor()
		# Print a representation of the instance and the assignment 
                # to the given <output_file>
		if len(sys.argv) == 3:
			# Print to stdout
			outfile = None
		else:
			outfile = sys.argv[3]
		assignment.dump_instance(filename=outfile)
		dump_assignment(assignment.assignment, filename=outfile, mode='a')

