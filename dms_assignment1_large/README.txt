Second set of instances for the first programming assignment.

This set of instances are of the size of 4 resources, 250 machines and 800
processes. Some of the services have non-unit minimum spread, which means
that constraints SSCon have to be respected in addition to SCCon and MCCon.

This archive contains three types of files:

     * instance_k.txt:	    the problem instance
     * initial_k.txt:	    the initial assignment
     * initialcost_k.txt:   the cost of the initial assignment (MLCost(A_I))
     * localcost_k.txt:	    an upper bound on the optimal cost
       			    (TotalCost(A_I,A_O)) that can be helpful for
			    evaluating performance

where k=1,2,..,10.
