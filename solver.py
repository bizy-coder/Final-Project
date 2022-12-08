from functools import partial
from multiprocessing import Pool
from helper import *
from combination_algorithm import *
from sat_sol import *


def get_exact_sol(g):
    sat_solutions = sat_solve(g, n=1)
    # sat_leaves = -1
    # if sat_solutions:
    #     sat_leaves = num_leaves(sat_solutions)
    # st = get_sol_from_inner_vertices(g, )
    write_graph_to_file(g, f"", f"hard.in")
    write_graph_to_file(sat_solutions, f"", f"hard.out")

    return
    heuristic_solution = get_best_heuristic_solve(g)
    heuristic_leaves = num_leaves(heuristic_solution)

    return sat_leaves, heuristic_leaves


def get_info(in_file, out_file):
    # Read the input file
    g_in_lst = list(read_hard_file(in_file))
    g_out_lst = list(read_hard_file(out_file))

    # for index in indices:
    #     write_graph_to_file(g_in_lst[index], "", "hard.in")
    #     write_graph_to_file(g_out_lst[index], "", "hard.out")

    for g_in, g_out in zip(g_in_lst, g_out_lst):
        print("Optimal is", num_leaves(g_out))

        # Solve the problem
        # sat_solutions = sat_solve(g_in, n=1)
        # if sat_solutions:
        #     if type(sat_solutions) != list:
        #         sat_solutions = [sat_solutions]
        #     for sat_solution in sat_solutions:
        #         print(
        #             "SAT solution has",
        #             # sat_solution.edges(),
        #             num_leaves(sat_solution),
        #             "leaves",
        #         )
        #     # print(
        #     #     "SAT solutions",
        #     #     [num_leaves(sat_solution) for sat_solution in sat_solutions],
        #     # )
        # else:
        #     print("SAT solution is None")
        heuristic_solution = good_solve(g_in)
        print("Heuristic solution has", num_leaves(heuristic_solution), "leaves")
        print()


def solve(hard_in):
    prev = nx.Graph()
    hard = list(hard_in)
    print(len(hard))
    hard = hard
    try:
        for i, hard in enumerate(hard):
            if i != 96:
                if i == 95:
                    prev = hard
                continue
            if nx.is_isomorphic(prev, hard):
                print(hard)
                continue
            else:
                prev = hard
            sol = sat_solve(hard, n=1)
            if sol:
                print(i, num_leaves(sol))
                write_graph_to_file(
                    sol,
                    f"GRAPH NUMBER {i} WITH {len(hard.edges())} EDGES",
                    f"all_hard2.out",
                )
            else:
                print(i, "None")
    except Exception as e:
        print(f"ERROR ON GRAPH {i}:", e)


def spanning_tree_of(g1, g2):
    if len(g1.nodes()) != len(g2.nodes()):
        return False
    for edge in g1.edges():
        if edge not in g2.edges():
            return False
    return True


def solve3(prev_sol_file, hard_in):
    # prev = list(read_hard_file(prev_sol_file))
    # print(prev)
    hard = list(read_hard_file(hard_in))
    print(len(hard))
    skip = 113
    # hard = hard[1:]

    # try:
    for i, hard in enumerate(hard):
        if i <= skip:
            continue
        # for prev_sol in prev:
        #     # print(prev_sol, hard)
        #     if spanning_tree_of(prev_sol, hard):
        #         if num_leaves(prev_sol) >= num_leaves(
        #             good_solve(hard, opt=num_leaves(prev_sol))
        #         ):
        #             print(i, num_leaves(prev_sol))
        #             write_graph_to_file(
        #                 prev_sol,
        #                 f"GRAPH NUMBER {i} WITH {len(hard.edges())} EDGES",
        #                 f"all_hard3.out",
        #             )
        #             break
        else:
            print("starting graph", i)
            sol = sat_solve(hard, n=1)
            if sol:
                print(i, num_leaves(sol))
                write_graph_to_file(
                    sol,
                    f"GRAPH NUMBER {i} WITH {len(hard.edges())} EDGES",
                    f"all_hard3.out",
                )
            else:
                print(i, "None")
    # except Exception as e:
    #     print(f"ERROR ON GRAPH {i}:", e)


def get_unsolved(sol_file, hard_file):
    nums = []
    with open(sol_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "#" in line:
                # Get 48 from - 100 99#GRAPH NUMBER 48 WITH 99 EDGES
                num = int(line.split("#")[1].split()[2])
                nums.append(num)
    # get first line of hard file
    with open(hard_file, "r") as f:
        first_line = int(f.readline())

    # Get missing numbers from nums
    missing = [i for i in range(first_line) if i not in nums]

    hard = list(read_hard_file(hard_file))
    # unsolved = [hard[i] for i in range(0, 100)]
    print("here")
    unsolved = [(i, hard[i]) for i in missing]
    return unsolved


def visualize_unsolved(unsolved):
    for hard_instance in unsolved:
        visualize_graph(hard_instance[1])


def visualize_first_solutions(unsolved):
    for hard in unsolved:
        print("starting")
        x = get_first_solution(hard[1])
        # visualize_graph(x)
        visualize_sol(hard[1], x, True)


# Run sat solve on all unsolved graphs in parallel, using 1 thread per graph
def sat_solve_all(unsolved):
    unsolved = [x[1] for x in unsolved]
    print(unsolved)
    best_sat_solve = partial(sat_solve, n=1, mod=1)
    with Pool(len(unsolved)) as p:
        print("here")
        solutions = p.map(best_sat_solve, unsolved)
        return solutions


def solve_component_graph(prob):
    orig = prob.copy()
    # necessary = []
    # for prob in unsolved:
    #     print("Prob is", prob[0])
    #     prob = prob[1]
    #     for node in prob.nodes():
    #         g_prime = prob.copy()
    #         g_prime.remove_node(node)
    #         if not nx.is_connected(g_prime):
    #             print(node)
    # print("Prob is", prob[0])
    # prob = prob[1]
    lst = []
    for node in prob.nodes():
        g_prime = prob.copy()
        g_prime.remove_node(node)
        if not nx.is_connected(g_prime):
            print(node)
            lst.append(node)

    removed_edges = []
    for node in lst:
        removed_edges.extend(list(prob.edges(node)))
        prob.remove_node(node)

    inner = []
    for i, comp in enumerate(nx.connected_components(prob)):
        comp = prob.subgraph(comp).copy()
        # print(comp, comp.edges())

        comp_prime = comp.copy()
        for node in lst:
            for edge in removed_edges:
                if edge[0] == node and edge[1] in comp.nodes():
                    comp_prime.add_edge(edge[1], node)
                elif edge[1] == node and edge[0] in comp.nodes():
                    comp_prime.add_edge(edge[0], node)

        new_graph = nx.Graph()
        for edge in comp_prime.edges():
            new_graph.add_edge(edge[0] - 10 * i, edge[1] - 10 * i)

        # print(new_graph.edges())
        # visualize_graph(new_graph)

        sol = sat_solve(new_graph)
        # err
        # relabel nodes
        # mapping = {node: i for i, node in enumerate(comp_prime.nodes())}
        # comp_prime = nx.relabel_nodes(comp_prime, mapping)

        # sol = sat_solve(comp_prime, n=1, mod=1)
        # # get inner nodes
        # # map back
        inner_nodes = [node + 10 * i for node in sol.nodes() if sol.degree(node) > 1]

        # inverse_map = {v: k for k, v in mapping.items()}
        # inner_nodes = [inverse_map[node] for node in inner_nodes]

        inner.extend(inner_nodes)

    print(inner)


def visualize_first_solution(prob):
    x = get_first_solution(prob[1])
    comp = list(nx.connected_components(x))
    print(len(prob[1].edges()), num_leaves(x), len(comp), min([len(c) for c in comp]))
    visualize_graph(x)
    # visualize_graph(x)
    # visualize_sol(prob[1], x)
    # visualize_sol(prob[1], x, True)


def heuristic_solving(unsolved):
    unsolved = [x[1] for x in unsolved]
    with Pool(len(unsolved)) as p:
        print("here")
        solutions = p.map(get_best_heuristic_solve, unsolved)
        return solutions


if __name__ == "__main__":
    # solve3("all_hard3.out", "all_hard3.in")

    unsolved = get_unsolved("all_hard3.out", "all_hard3.in")
    # # visualize_first_solutions(unsolved)
    # # print(unsolved)
    # # visualize_unsolved([unsolved[-2]])
    # # x = sat_solve(unsolved[-2], n=1, mod=1)
    # # print(x.edges())conda
    # unsolved = get_unsolved("all_hard3.out", "all_hard3.in")
    # for i in range(2, 6):
    #     visualize_first_solution(unsolved[i])
    # heuristic_solving(unsolved)
    # x=get_basic_solve(unsolved[1][1])
    # print(num_leaves(x))
    # visualize_first_solution(unsolved[1])
    # visualize_first_solution(unsolved[2])
    # visualize_first_solution(unsolved[3])
    # visualize_first_solution(unsolved[4])
    # visualize_first_solution(unsolved[0])
    # print(sat_solve_all([unsolved[1]]))
    # prob = unsolved[2][1]
    # solve_component_graph(prob)
    prob = list(read_hard_file("all_hard3.in"))[84]
    solve_component_graph(prob)

    pass
