from heuristics import *
from local_search import *
from helper import *
from strategic_oscilation import *
from genetic_algorithm_helpers import *
from sat_sol import *


def get_all_starts(g):
    lst = []

    lst.append(solis_oba(g))
    lst.append(pure_greedy(g))

    for starting_point in g.nodes:
        lst.append(greedy_distance_based(g, starting_point))
        lst.append(bfs_spanning_tree(g, starting_point, random_bfs_order))
        lst.append(bfs_spanning_tree(g, starting_point, greedy_bfs_order))

    return lst


def sort_by_num_leaves(lst):
    lst.sort(key=lambda x: num_leaves(x), reverse=True)


def test_heuristics(g):
    lst = []

    # Add the algorithm name and result to the list as a tuple
    lst.append(("Solis-OBA", solis_oba(g)))
    # lst.append(("Pure greedy", pure_greedy(g)))

    for starting_point in list(g.nodes()):
        lst.append(
            ("Greedy distance-based bfs", greedy_distance_based(g, starting_point))
        )

        lst.append(
            (
                "Greedy distance-based length",
                greedy_distance_based(g, starting_point, lambda x: x),
            )
        )

        lst.append(("Pure greedy", pure_greedy(g, starting_point)))

        lst.append(
            (
                "BFS spanning tree with random order",
                bfs_spanning_tree(g, starting_point, random_bfs_order),
            )
        )

        lst.append(
            (
                "BFS spanning tree with greedy order",
                bfs_spanning_tree(g, starting_point, greedy_bfs_order),
            )
        )

    # Sort the list by the number of leaves in the tree
    lst.sort(key=lambda x: num_leaves(x[1]), reverse=True)

    # Check if any trees are not valid
    for name, tree in lst:
        if not is_spanning_tree(g, tree):
            print("Invalid tree:", name)

    return lst


if __name__ == "__main__":
    for _ in range(10):
        g = random_graph_num_edges(100, 500)

        opt = sat_solve(g)
        # print(opt)
        print("OPTIMAL IS:", num_leaves(opt), is_spanning_tree(g, opt), "\n")
        # visualize_graph(opt)
        lst = test_heuristics(g)
        for x in lst:
            print(x[0], num_leaves(x[1]))

        print("\n\n")
