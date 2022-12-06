from helper import *
from combination_algorithm import *
from sat_sol import *


def get_exact_sol(g):
    sat_solutions = sat_solve(g, n=1)
    sat_leaves = -1
    if sat_solutions:
        sat_leaves = num_leaves(sat_solutions)
    
    heuristic_solution = get_best_heuristic_solve(g)
    heuristic_leaves = num_leaves(heuristic_solution)
    
    return sat_leaves, heuristic_leaves
        

def solve(in_file, out_file):
    # Read the input file
    g_in_lst = list(read_hard_file(in_file, 18))[3:]
    g_out_lst = list(read_hard_file(out_file, 18))[3:]

    for g_in, g_out in zip(g_in_lst, g_out_lst):
        print("Optimal is", num_leaves(g_out))

        # Solve the problem
        sat_solutions = sat_solve(g_in, n=1)
        if sat_solutions:
            if type(sat_solutions) != list:
                sat_solutions = [sat_solutions]
            for sat_solution in sat_solutions:
                print(
                    "SAT solution has",
                    # sat_solution.edges(),
                    num_leaves(sat_solution),
                    "leaves",
                )
            # print(
            #     "SAT solutions",
            #     [num_leaves(sat_solution) for sat_solution in sat_solutions],
            # )
        else:
            print("SAT solution is None")
        heuristic_solution = get_best_heuristic_solve(g_in)
        print("Heuristic solution has", num_leaves(heuristic_solution), "leaves")
        print()


if __name__ == "__main__":
    solve("hard_in1005.txt", "hard_out1005.txt")
