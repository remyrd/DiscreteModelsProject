Solution checker for the first programming assignment of course T-79.4101
Discrete Models and Search.

_Update History_
* This is version 2.0. The only change with respect to the first version
  is that the checker now skips all lines in the output-solution file
  until the very last one. This change was done in order to conform to
  the update in the programming assignment instructions, according to
  which your program should append better feasible solutions as soon
  as they are found to the output file. In the case that this last line
  has missing values (e.g., because the program was interrupted before
  finishing to write the complete line), the previous line will be used.


Note: this checker is intended for validation of the solutions obtained
by your local search method, i.e., for helping you to debug your code.
It _must not_ be used inside your code as a part of the method itself!

Usage:

$# dmas_checker <instance file> <initial-solution file> <output-solution file>	

Note: this checker was tested on Aalto's linux login server
kosh.aalto.fi, which can be accessed remotely via ssh from anywhere
using the aalto account. Notice that it should be ok to use
kosh.aalto.fi for running the checker, but not your own (computing
intensive) programs. For this you should use either own machines or
those in the computer classrooms (e.g., Maarintalo).

Examples:

$# dmas_checker instance_1.txt initial_1.txt localsol_1.txt 
*** Solution checker for the 1st programming assignment DMAS ***
CapConst: 0 ConfConst: 0 SpreadConst: 0
LoadCost: 39984 ProcessMoveCost: 3252
Total cost: 43236 Total constraint violation: 0

This shows output for a feasible solution (all constraint violations are
zero) that achieves a total cost of 43236.

$# dmas_checker instance_1.txt initial_1.txt localsol_2.txt
 *** Solution checker for the 1st programming assignment DMAS ***
CapConst: 35513 ConfConst: 30 SpreadConst: 1
LoadCost: 88325 ProcessMoveCost: 3415
Total cost: 91740 Total constraint violation: 35544

This shows output for an infeasible solution for the same instance. Note
that the CapConst value is equal to the total amount of resource consumption
that exceeds the resource capacities, summed over all machines, processes
and resources. Similarly, the value ConfConst is equal to the total number
of conflicting processes summed over all machines and services (for a single
machine, it is the number of processes of the same service assigned to
the machine - 1, if positive). SpreadConst is total amount of missing
spread summed over all services (the number of locations a service would
need to additionally be run in in order to satisfy its minimum spread
constraint). 
