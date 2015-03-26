
/*
 * This is some demo Java code for reading in a problem instance and
 * initial assignment for the first programming assignment of T-79.4101
 * Discrete Models and Search. 
 *
 * Note: the main method here just reads in the problem instance file and
 * the initial assignment and then prints both to the output file.
 */


import java.io.*;
import java.util.StringTokenizer;
import java.util.Vector;

class ProcessAssignment  {

    // number of resources (N_R)
    static int numResources = 0;

    // number of machines (N_M)
    static int numMachines = 0;

    // number of processes (N_P)
    static int numProcesses = 0;

    // number of services (N_S)
    static int numServices = 0;

    // number of locations (N_L)
    static int numLocations = 0;

    static Vector< Vector<Integer> > machineCapacities = new Vector< Vector< Integer > >();
    static Vector< Vector<Integer> > softMachineCapacities = new Vector< Vector< Integer > >();
    static Vector< Integer > machineLocations = new Vector< Integer >();
    static Vector< Integer > serviceMinSpreads = new Vector< Integer >();
    static Vector< Integer > processServices = new Vector< Integer >();
    static Vector< Vector<Integer> > processRequirements = new Vector< Vector< Integer > >();
    static Vector< Integer > processMovingCosts = new Vector< Integer >();

    static Vector< Integer > initialAssignment = new Vector< Integer >();

    // helper function for asserting that input values are in correct range
    // and other checks work out
    private static void assertCondition(boolean condition) {
	if(!condition) {
	    System.out.println("assert violated!");
	    System.exit(0);
	}
    }

    // reads in an instance file
    // Note: this is a very crude method of reading the input file!
    // (meaning there is only very basic checking for errors)
    private static void readInstanceFile(String fileName) {
	try{
	    FileInputStream fstream = new FileInputStream(fileName);
	    DataInputStream in = new DataInputStream(fstream);
	    BufferedReader br = new BufferedReader(new InputStreamReader(in));
	    String strLine;
	    
	    numResources = Integer.parseInt(br.readLine());
	    assertCondition(1 <= numResources && numResources <= 10);

	    numMachines = Integer.parseInt(br.readLine());
	    assertCondition(1<= numMachines && numMachines <= 500);

	    System.out.println("LOG: numResources and numMachines");

	    for(int m=0;m<numMachines;m++) {
		StringTokenizer st = new StringTokenizer(br.readLine());

		machineCapacities.add(new Vector< Integer >());
		softMachineCapacities.add(new Vector< Integer >());

		// read in location of machine m
		int location_m = Integer.parseInt(st.nextToken());
		assertCondition(0<= location_m && location_m < numMachines);

		if(numLocations < location_m + 1)
		    numLocations = location_m + 1;

		machineLocations.add(new Integer(location_m));

		// read in machine capacities (for MCCon)
		for(int r=0;r<numResources;r++) {
		    machineCapacities.get(m).add(new Integer(Integer.parseInt(st.nextToken())));
		}

		// read in soft machine capacities (for MLCost)
		for(int r=0;r<numResources;r++) {
		    softMachineCapacities.get(m).add(new Integer(Integer.parseInt(st.nextToken())));
		}
	    }

	    System.out.println("LOG: read machines");

	    numServices = Integer.parseInt(br.readLine());
	    assertCondition(1<= numServices && numServices <= 2000);

	    for(int s=0;s<numServices;s++) {
		// read in minSpread of service s
		int minSpread_s = Integer.parseInt(br.readLine());
		assertCondition(0<= minSpread_s && minSpread_s <= numLocations);

		serviceMinSpreads.add(new Integer(minSpread_s));
	    }

	    System.out.println("LOG: read services");

	    numProcesses = Integer.parseInt(br.readLine());
	    assertCondition(1<= numProcesses && numProcesses <= 2000);

	    for(int p=0;p<numProcesses;p++) {
		StringTokenizer st = new StringTokenizer(br.readLine());

		// read in service of process p
		int service_p = Integer.parseInt(st.nextToken());
		assertCondition(0<= service_p && service_p < numServices);

		processServices.add(new Integer(service_p));

		processRequirements.add(new Vector<Integer>(numResources));

		// read in process requirements
		for(int r=0;r<numResources;r++) {
		    processRequirements.get(p).add(new Integer(Integer.parseInt(st.nextToken())));
		}

		int processMovingCost_p = Integer.parseInt(st.nextToken());
		assertCondition(0<= processMovingCost_p && processMovingCost_p <= 1000);

		processMovingCosts.add(new Integer(processMovingCost_p));
	    }

	    System.out.println("LOG: read processes");
	    System.out.println("LOG: read ALL");
	    

	    //Close the input stream
	    in.close();
	} catch (Exception e){//Catch exception if any
	    System.err.println("ERROR: " + e.toString());
	}
    }

    // reads in the initial process to machine assignment
    // note: should be called after function readInstanceFile()
    static void readInitialAssignment(String fileName) {
	try{
	    FileInputStream fstream = new FileInputStream(fileName);
	    DataInputStream in = new DataInputStream(fstream);
	    BufferedReader br = new BufferedReader(new InputStreamReader(in));
	    StringTokenizer st = new StringTokenizer(br.readLine());

	    assert(st.countTokens() == numProcesses);

	    for(int p=0;p<numProcesses;p++)
		initialAssignment.add(new Integer(Integer.parseInt(st.nextToken())));

	    //Close the input stream
	    in.close();
	} catch (Exception e){//Catch exception if any
	    System.err.println("ERROR: " + e.toString());
	}
    }

    // dumps the instance to the screen
    private static void dumpProblem() {
	System.out.println("Problem instance:");
	System.out.println("  Resources: "+numResources);
	System.out.println("  Machines: "+numMachines);
	System.out.println("  Processes: "+numProcesses);
	System.out.println("  Services: "+numServices);
	System.out.println("  Locations: "+numLocations);

	System.out.println("  MachineCapacities: (format: m(achine) capacities soft/hard)");

	for(int m=0;m<numMachines;m++) {
	    System.out.println("    m: "+m);
	    System.out.print("       ");

	    for(int r=0;r<numResources;r++) {
		System.out.print(softMachineCapacities.get(m).get(r)+"/"+machineCapacities.get(m).get(r));
		
		if(r<numResources-1)
		    System.out.print(", ");
		else
		    System.out.println("");
	    }
	}

	System.out.println("  MachineLocations: (format: m(achine) l(ocation))");
	
	for(int m=0;m<numMachines;m++)
	    System.out.println("    m: "+m+ " l: "+machineLocations.get(m));

	System.out.println("  Services spreadMin: (format: s(ervice) (spread)M(in))");

	for(int s=0;s<numServices;s++)
	    System.out.println("    s: "+s+ " M: "+serviceMinSpreads.get(s));

	System.out.println("  ProcessRequirements: (format: p(rocess) requirements)");

	for(int p=0;p<numProcesses;p++) {
	    System.out.println("    p: "+p);
	    System.out.print("       ");

	    for(int r=0;r<numResources;r++) {
		System.out.print(processRequirements.get(p).get(r));
		
		if(r<numResources-1)
		    System.out.print(", ");
		else
		    System.out.println("");
	    }
	}

	System.out.println("  ProcessServices: (format: p(rocess) s(ervice)))");

	for(int p=0;p<numProcesses;p++)
	    System.out.println("    p: "+p+" s: "+processServices.get(p));

	System.out.println("  ProcessMovingCosts: (format: p(rocess) (pm)c)");

	for(int p=0;p<numProcesses;p++)
	    System.out.println("    p: "+p+" c: "+processMovingCosts.get(p));

    }

    // dumps the given assignment to the screen
    private static void dumpAssignment(Vector< Integer > assignment) {
	for(int p=0;p<assignment.size();p++)
	    System.out.println("  " + p + " -> " + assignment.get(p));
    }

    // main function
    public static void main(String args[]) {
	if(args.length != 3) {
	    System.out.println("ERROR: usage: ");
	    System.out.println("java ProcessAssignment <instance_file> <initial_solution_file> <output_file>");
	} else {
	    readInstanceFile(args[0]);
	    dumpProblem();
	    readInitialAssignment(args[1]);
	    System.out.println("InitialAssignment: (format: process -> machine)");
	    dumpAssignment(initialAssignment);
	}
    }
}
