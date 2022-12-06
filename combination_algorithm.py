from heuristics import *
from local_search import *
from helper import *
from strategic_oscilation import *
from genetic_algorithm_helpers import *
from sat_sol import *


def get_best_heuristic_solve(g):
    lst = []

    lst.append(solis_oba(g))

    shortest_paths = dict(nx.shortest_path_length(g))
    for starting_point in list(g.nodes()):
        # print(starting_point)
        lst.append(pure_greedy(g, starting_point))
        lst.append(bfs_spanning_tree(g, starting_point, random_bfs_order))
        lst.append(bfs_spanning_tree(g, starting_point, greedy_bfs_order))
        lst.append(
            greedy_distance_based(g, starting_point, lambda x: x, shortest_paths)
        )
        x = greedy_distance_based2(g, starting_point, lambda x: x, shortest_paths)
        lst.append(x)

    # Remove duplicates (isomorphic trees)
    # new_lst = []
    # for x in lst:
    #     if not any(nx.is_isomorphic(x, y) for y in lst):
    #         new_lst.append(x)

    # lst = new_lst
    sort_by_num_leaves(lst)
    # print([num_leaves(x) for x in lst])

    new_lst = []

    for g in lst[:5]:
        # print(g)
        # Get the leaf nodes
        leaves = [x for x in g.nodes() if g.degree(x) == 1]
        # Get the internal nodes
        internal = [x for x in g.nodes() if g.degree(x) > 1]

        new_leaves, new_inner = strategic_oscilation(g, leaves, internal, 0.005, 0.6)

        st = get_sol_from_inner_vertices(g, new_inner)

        one_local_search(g, st)

        new_lst.append(st)

    sort_by_num_leaves(new_lst)
    # print([num_leaves(x) for x in new_lst])

    return new_lst[0]


def get_basic_solve(g):
    return greedy_distance_based2(
        g, None, lambda x: x, dict(nx.shortest_path_length(g))
    )


def get_good_starts(g, opt=None, skip=1):
    lst = []

    lst.append(solis_oba(g))
    lst.append(pure_greedy(g))
    lst.append(greedy_distance_based2(g))

    if opt and max(num_leaves(x) for x in lst) >= opt:
        return lst

    shortest_paths = dict(nx.shortest_path_length(g))
    for starting_point in list(g.nodes())[::skip]:
        # lst.append(greedy_distance_based(g, starting_point))
        # lst.append(bfs_spanning_tree(g, starting_point, random_bfs_order))
        x = greedy_distance_based2(g, starting_point, lambda x: x, shortest_paths)
        lst.append(x)
        if opt and num_leaves(x) >= opt:
            break
        # y = greedy_distance_based(g, starting_point, lambda x: x, shortest_paths)
        # print(num_leaves(x), num_leaves(y), nx.is_isomorphic(x, y))
    return lst


def sort_by_num_leaves(lst):
    lst.sort(key=lambda x: num_leaves(x), reverse=True)


def test_heuristics(g, skip=10):
    lst = []

    # Add the algorithm name and result to the list as a tuple
    lst.append(("Solis-OBA", solis_oba(g)))
    lst.append(("Pure greedy", pure_greedy(g)))

    for starting_point in list(g.nodes())[::skip]:
        # lst.append(
        #     ("Greedy distance-based bfs", greedy_distance_based(g, starting_point))
        # )

        lst.append(
            (
                "Greedy distance-based length",
                greedy_distance_based(g, starting_point, lambda x: x),
            )
        )

        # lst.append(("Pure greedy", pure_greedy(g, starting_point)))

        # lst.append(
        #     (
        #         "BFS spanning tree with random order",
        #         bfs_spanning_tree(g, starting_point, random_bfs_order),
        #     )
        # )

        # lst.append(
        #     (
        #         "BFS spanning tree with greedy order",
        #         bfs_spanning_tree(g, starting_point, greedy_bfs_order),
        #     )
        # )

    # Sort the list by the number of leaves in the tree
    lst.sort(key=lambda x: num_leaves(x[1]), reverse=True)

    # # Check if any trees are not valid
    # for name, tree in lst:
    #     if not is_spanning_tree(g, tree):
    #         print("Invalid tree:", name)

    return lst


def genetic_solve(g, pop, iter, combines, mutation_rate, best=None):
    starts = get_good_starts(g)
    sort_by_num_leaves(starts)
    starts = starts[:pop]

    # Randomly choose 20 pairs of trees to combine (weight by number of leaves)
    for i in range(iter):
        pairs = []
        for _ in range(combines):
            pairs.append(
                random.choices(starts, weights=[num_leaves(x) for x in starts], k=2)
            )

        for pair in pairs:
            starts.append(combine1(g, [pair[0], pair[1]]))
            starts.extend(combine2(g, pair[0], pair[1]))

        # print(starts)
        sort_by_num_leaves(starts)
        # starts = starts[:pop]

        print("Iteration", i, "best:", num_leaves(starts[0]))
        # Mutate each tree
        for i in range(len(starts)):
            starts[i] = mutate(
                g, starts[i], int(mutation_rate * random.random() * len(g))
            )

        if any(not is_spanning_tree(g, x) for x in starts):
            print("Invalid tree")
            break

        if best:
            if num_leaves(starts[0]) == best:
                break
    return starts[0]


def bad_solve(g):
    return greedy_distance_based2(g)


def good_solve(g, opt=None):
    starts = get_good_starts(g, opt)
    # print(starts)
    sort_by_num_leaves(starts)
    if opt and num_leaves(starts[0]) >= opt:
        return starts[0]
    # return starts[0]
    # print("Best starts:", num_leaves(starts[0]), num_leaves(starts[1]))
    updated = [x if (x := one_local_search(g, start)) else g for start in starts]
    sort_by_num_leaves(updated)
    # print("Best updated:", num_leaves(updated[0]), num_leaves(updated[1]))
    return updated[0]


if __name__ == "__main__":
    for _ in range(10):
        g = random_graph_num_edges(50, 200)

        opt = sat_solve(g)
        # print(opt)
        print("OPTIMAL IS:", num_leaves(opt), is_spanning_tree(g, opt), "\n")
        # visualize_graph(opt)
        # lst = test_heuristics(g)
        # for x in lst:
        #     print(x[0], num_leaves(x[1]))
        # genetic_solve(g, 60, 20, 20, 0.1, num_leaves(opt))
        good_solve(g)

        print("\n\n")
