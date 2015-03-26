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
import random
#from numpy import append

# Just some useful exceptions to raise during parsing
class InstanceError(BaseException):
	pass

class AssignmentError(BaseException):
	pass

class InvalidArgumentException(ValueError):
	pass

global_minima = 0

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
					raise InstanceError("Wrong number of values (expected %d, found %d)" % (1 + 2 * self.num_resources, len(tokens)))

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
					raise InstanceError("Wrong number of values (expected %d, found %d)" % (2 + self.num_resources, len(tokens)))

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
		
#======================================================================
# TODO 
#======================================================================	
	
def shared_processes(proc_assignment,target_element,target_list):
	"""Search for processes with a common element: The return list contains elements of the type index of target_list"""
	shared_processes = []
	for process in xrange(proc_assignment.num_processes):
		if target_list[process] == target_element:
			shared_processes.append(process)

	return shared_processes

def verify_service_spread(proc_assignment, process, machine):
	"""Verify if the minimum service spread is still OK when moving a process to a new machine"""
	shared_proc_service = shared_processes(proc_assignment, proc_assignment.process_services[process], proc_assignment.process_services) # processes with the same service
	if process in shared_proc_service:
		shared_proc_service.remove(process) # don't want to include process being evaluated since it moves
	location_list = [proc_assignment.machine_locations[machine]] # add the location of the instanced machine at the beginning because our process moves to it
	for proc in xrange(shared_proc_service.__len__()):
		if proc_assignment.machine_locations[proc_assignment.assignment[shared_proc_service[proc]]] not in location_list:# if we find a new location, add it to the list
			location_list.append(proc_assignment.machine_locations[proc_assignment.assignment[shared_proc_service[proc]]])
	return (location_list.__len__() >= proc_assignment.service_min_spreads[proc_assignment.process_services[process]])
	
def try_constraints(proc_assignment, process, machine):
	"""Try constraints for allowing a process into a machine"""
	# MCCon
	mccon = True
	machine_capacity = proc_assignment.machine_capacities[machine]
	local_process_cost = [0] * machine_capacity.__len__() #sum of the processes in a machine
	shared_proc_machine = shared_processes(proc_assignment, machine,proc_assignment.assignment)
	#print("processes in machine ",machine)
	#print("\t",shared_proc_machine)
	if process not in shared_proc_machine:
		shared_proc_machine.append(process) #include the process to be moved
	#print("\t",shared_proc_machine)
	for i in xrange(shared_proc_machine.__len__()):
		#print("process ",shared_proc_machine[i])
		for j in xrange(machine_capacity.__len__()):
			local_process_cost[j] += proc_assignment.process_requirements[shared_proc_machine[i]][j] #process i, resource j
			#print("\trequirement ",j,"\t",proc_assignment.process_requirements[i][j])
			#print("\t\tlocal_process_cost ",local_process_cost)
	for j in xrange(machine_capacity.__len__()):
		#print("machine ",machine,"\n\tlocal process cost ",local_process_cost[j],"\n\tmachine_capacity ",machine_capacity[j])
		#print("before the evaluation ",local_process_cost," ",machine_capacity)
		#print("soft capacity constraints?? ", proc_assignment.soft_machine_capacities[machine])
		if local_process_cost[j] > machine_capacity[j]:
			#print("MCCon not met!!")
			mccon = False
			#print ("MCCon unsatisfied for ", process," in machine ",machine)
			return False
	
	# SCCon
	sccon = True
	shared_proc_machine = shared_processes(proc_assignment, machine,proc_assignment.assignment)
	for i in xrange(shared_proc_machine.__len__()):
		if proc_assignment.process_services[process] == proc_assignment.process_services[shared_proc_machine[i]]:
			sccon = False
			#print ("SCCon unsatisfied for ",process," in machine ",machine)
			return False 
	# SSCon	
	sscon = True
	if proc_assignment.service_min_spreads[proc_assignment.process_services[process]]>1 : # is it necessary?
		sscon = verify_service_spread(proc_assignment, process, machine)
		if sscon == False :
			#print ("SSCon unsatisfied for ",process," in machine ",machine)
			return False
	
	return (mccon & sccon & sscon)	

def local_cost_delta(proc_assignment, process, machine):
	"""Calculates the cost difference for moving a process to a new machine.
	Positive -> bad, new configuration costs more
	Negative -> good, new configuration costs less"""

	moving_cost = proc_assignment.process_moving_costs[process]
	total_cost = moving_cost
	
	machineload_cost_old = [0] * proc_assignment.machine_capacities[0].__len__()
	machineload_cost_new = [0] * proc_assignment.machine_capacities[0].__len__()
	process_cost = proc_assignment.process_requirements[process]
	shared_proc_machine_old = shared_processes(proc_assignment, proc_assignment.assignment[process],proc_assignment.assignment) #processes in the old machine
	shared_proc_machine_new = shared_processes(proc_assignment, machine, proc_assignment.assignment) #processes in the new machine
	
	#costs in new and old machine before moving process
	for i in xrange(shared_proc_machine_old.__len__()):
		for j in xrange(proc_assignment.machine_capacities[0].__len__()):
			machineload_cost_old[j] += proc_assignment.process_requirements[shared_proc_machine_old[i]][j]
	for i in xrange(shared_proc_machine_new.__len__()):
		for j in xrange(proc_assignment.machine_capacities[0].__len__()):
			machineload_cost_new[j] += proc_assignment.process_requirements[shared_proc_machine_new[i]][j]

	#check if soft capacities lower limit is reached
	for j in xrange(proc_assignment.machine_capacities[0].__len__()):
		if (machineload_cost_old[j]-process_cost[j])>proc_assignment.soft_machine_capacities[proc_assignment.assignment[process]][j]: #assigment[process] = old machine
			#don't remove too much cost, only until soft capacities limit
			total_cost -= machineload_cost_old[j] - proc_assignment.soft_machine_capacities[proc_assignment.assignment[process]][j]
		else:
			#soft capacities not reached, remove whole cost
			total_cost -= process_cost[j]
	
	#check if soft capacities upper limit is reached
	for j in xrange(proc_assignment.machine_capacities[0].__len__()):
		if machineload_cost_new[j] > proc_assignment.soft_machine_capacities[machine][j]:
			total_cost += process_cost[j]
		else:
			total_cost += machineload_cost_new[j] + process_cost[j] - proc_assignment.soft_machine_capacities[machine][j]
	
	return total_cost
	
def global_cost(proc_assignment, original_assignment):
	
	move_cost = 0
	
	for process in xrange(proc_assignment.num_processes):
		if proc_assignment.assignment[process] != original_assignment.assignment[process]:
			move_cost += proc_assignment.process_moving_costs[process]
	
	load_cost = 0
	
	for machine in xrange(proc_assignment.num_machines):
		shared_machine_proc = shared_processes(proc_assignment, machine, proc_assignment.assignment)
		machine_load_cost = [0] * proc_assignment.num_resources
		for process in xrange(shared_machine_proc.__len__()):
			for resource in xrange(proc_assignment.num_resources):
				machine_load_cost[resource] += proc_assignment.process_requirements[shared_machine_proc[process]][resource]
		for resource in xrange(proc_assignment.num_resources):
			if machine_load_cost[resource] > proc_assignment.soft_machine_capacities[machine][resource]:
				load_cost += machine_load_cost[resource] - proc_assignment.soft_machine_capacities[machine][resource]
	
	return move_cost + load_cost

def randomize(proc_assignment, iterations, cost_reduction):
	"""Look iterations times for a random couple of process -> machine with constraints satisfiable.
		if it is possible, move the instance to that neighbor."""
	changes = 0
	while changes < iterations:
		rand_process = random.randint(0,proc_assignment.num_processes-1)
		rand_machine = random.randint(0,proc_assignment.num_machines-1)
		if try_constraints(proc_assignment, rand_process, rand_machine):
			proc_assignment.assignment[rand_process] = rand_machine
			cost_reduction += local_cost_delta(proc_assignment, rand_process, rand_machine)
			changes += 1
	#print("we are dealing now with\n",proc_assignment.assignment)
	dump_real_assignment(proc_assignment.assignment, filename = "dms_assignment1_small/test_file")
	return cost_reduction	
		
					
	
def probe_neighbor(proc_assignment, original_assignment):
	"""see what is the least moving cost, then swap processes machines if possible: steepest descent"""
	global global_minima
	#process with least moving cost specified? if not, find one
	cost_reduction = 0
	global_minima = global_cost(original_assignment, original_assignment) #calculate the original cost
	while True:
		blacklist = [0] * proc_assignment.num_processes
		recursions = 0
		costs = 0
	
		while (recursions<proc_assignment.num_processes-1):# & (costs != []):
		
			candidate_machines = []
			costs = []
			#print("run ",recursions)
			
			#look for the least moving cost process excluding the already moved processes
			if blacklist == [0] * proc_assignment.num_processes:
				min_move_cost_proc = proc_assignment.process_moving_costs.index(min(proc_assignment.process_moving_costs))
				blacklist[min_move_cost_proc] = 1
			else:
				minimal = 1234
				for process in xrange(proc_assignment.process_moving_costs.__len__()):
					if (proc_assignment.process_moving_costs[process] <= minimal) & (blacklist[process]==0):
						minimal = proc_assignment.process_moving_costs[process]
						min_move_cost_proc = process
				blacklist[min_move_cost_proc] = 1
			
			#try constraints/cost for all machines where min_move_cost_proc can go
			#print("currently evaluating ",proc_assignment.assignment)
			for machine in xrange(proc_assignment.num_machines):
				if try_constraints(proc_assignment, min_move_cost_proc, machine):
					if local_cost_delta(proc_assignment, min_move_cost_proc, machine)<0:
						candidate_machines.append(machine)
						costs.append(local_cost_delta(proc_assignment, min_move_cost_proc,machine))
			#print("we found ",candidate_machines.__len__()," candidates! process ",min_move_cost_proc," can go to machines ",candidate_machines)
			#print("the costs are ",costs)
	
				
			# candidate_machines --> [1, 3, 5, 9] the ones that passed the constraints
			# costs --> [-25, -58, -220, -98] keep only the negatives -> usefull solutions
			
			#info required to dump
			if len(sys.argv) == 3:
				# Print to stdout
				outfile = None
			else:
				outfile = sys.argv[3]
			
			
			if costs.__len__()>0:
				best_machine = candidate_machines[costs.index(min(costs))]
				#print(min_move_cost_proc," will move to ",best_machine)
				proc_assignment.assignment[min_move_cost_proc] = best_machine
				cost_reduction += min(costs) #update the local cost delta
			
			
			#if there's a better neighbor, move to it, otherwise we found a local minima
			if global_cost(proc_assignment, original_assignment) < global_minima:
				global_minima = global_cost(proc_assignment, original_assignment)
				print("New minima ",global_minima)
				dump_real_assignment(proc_assignment.assignment, filename = outfile)
			
			recursions += 1
		
	
	
		cost_reduction = randomize(proc_assignment, 2*proc_assignment.num_processes, cost_reduction)





#=======================================================================

def dump_real_assignment(assignment, filename=None, mode='w'):
	if filename:
		if mode not in ['a', 'w']:
			raise InvalidArgumentException("Allowed modes are 'a' and 'w'")
		f = open(filename, mode)
	else:
		f = sys.stdout

	for i in xrange(assignment.__len__()):
		print(assignment[i], file=f, end=" ")
	
	if f is not sys.stdout:
		f.close()
		
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
			original = ProcessAssignment(filename=sys.argv[1])
		except BaseException, e:
			print("Could not initialize a ProcessAssignment.", file=sys.stderr)
			print(repr(e), file=sys.stderr)
			sys.exit(1)

		try:
			assignment.update_assignment(filename=sys.argv[2])
			original.update_assignment(filename=sys.argv[2])
		except BaseException, e:
			print("Could not load the initial assignment.", file=sys.stderr)
			print(repr(e), file=sys.stderr)
			sys.exit(1)

# TODO ===============================================
		probe_neighbor(assignment, original)
		
# ====================================================		
		# Print a representation of the instance and the assignment 
        # to the given <output_file>
		#if len(sys.argv) == 3:
		#	# Print to stdout
		#	outfile = None
		#else:
		#	outfile = sys.argv[3]
		assignment.dump_instance(filename="dms_assignment1_small/human")
		#dump_assignment(assignment.assignment, filename=outfile, mode='a')

