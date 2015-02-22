First set of instances for the first programming assignment.


This set of instances are of the size of 3 resources, 
20 machines and 60
processes. 
All processes have unit minimum spread, which effectively
disables 
all constraints SSCon. 
However, since all services have more than

one process, one still has to respect SCCon 
(in addition to MCCon
constraints).

This archive contains three types of files:


     * instance_k.txt:	    the problem instance
     
	* initial_k.txt:	    the initial assignment
  
   * initialcost_k.txt:   the cost of the initial assignment (MLCost(A_I))

     * localcost_k.txt:	    an upper bound on the optimal cost
       	
    (TotalCost(A_I,A_O)) that can be helpful for
		
 evaluating performance

where k=1,2,..,10.

