import os
import pyscipopt as scip
import time

def solve_continuous_knapsack(wmax, items, type):
    # Create a new SCIP instance
    prob = scip.Model("Continuous Knapsack")

    # Add variables
    x = {}
    for i, (v, w) in enumerate(items):
        x[i] = prob.addVar(vtype=type, name=f"x_{i}", lb=0.0, ub=1.0)  # Bound the variables between 0 and 1

    # Add constraint: total weight <= wmax
    prob.addCons(scip.quicksum(w * x[i] for i, (v, w) in enumerate(items)) <= wmax)

    # Set objective: maximize total value
    prob.setObjective(scip.quicksum(v * x[i] for i, (v, w) in enumerate(items)), "maximize")

    # Start measuring time
    start_time = time.time()

    # Solve the problem
    prob.optimize()

    # Stop measuring time
    end_time = time.time()

    # Get solution
    solution = {}
    for i, (v, w) in enumerate(items):
        solution[i] = x[i].getLPSol()
    if type == "C":
        print("Continuous Knapsack Problem:")
    else:
        print("Binary Knapsack Problem:")
    return prob.getObjVal(), solution, end_time - start_time

def read_knapsack_instance(file_path):
    items = []
    with open(file_path, 'r') as file:
        n, wmax = map(int, file.readline().split())
        for line in file:
            v, w = map(int, line.split())
            items.append((v, w))
    return n, wmax, items

def main():
    # Get the path of the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the file path
    file_name = "knapPI_1_500_1000_1.txt"  # Assuming the file extension is .txt
    file_path = os.path.join(current_directory, file_name)
    
    n, wmax, items = read_knapsack_instance(file_path)
    
    # Solve knapsack problem C for continuous, B for binary
    # type = "C"
    type = "B"
    obj_val, solution, solve_time = solve_continuous_knapsack(wmax, items, type)

    print("Optimal objective value:", obj_val)
    print("Solution (fraction of each item):", solution)
    print("Time taken to solve:", solve_time, "seconds")


if __name__ == "__main__":
    main()
