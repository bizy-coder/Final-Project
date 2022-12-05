from helper import *
from heuristics import *

"""
Algorithm from:
https://link.springer.com/chapter/10.1007/978-3-319-24598-0_29#Sec4
"""


def drop(v, leaves, inner):
    # Add v to S'
    inner.add(v)

    # Remove v from S
    leaves.remove(v)


def add(v, leaves, inner):
    # Remove v from S'
    inner.remove(v)

    # Add v to S
    leaves.add(v)


def strategic_oscilation(g, leaves=None, inner=None, k_step=0.01, k_max=1):
    if leaves is None:
        leaves, inner = pure_greedy(g)
    leaves, inner = set(leaves), set(inner)
    k = k_step

    # print(valid(g, leaves, inner, debug=True))

    last_leaves = leaves.copy()
    last_inner = inner.copy()

    while k <= k_max:
        delta_plus = set()
        delta_minus = set()
        for _ in range(int(k * len(inner))):
            v = random.choice(list(inner))
            add(v, leaves, inner)
            delta_plus.add(v)

        while not valid(g, leaves, inner):
            v = select_greedy(leaves, g, leaves, inner)
            drop(v, leaves, inner)
            delta_minus.add(v)

        if len(leaves) > len(last_leaves):
            k = k_step
            last_inner = inner.copy()
            last_leaves = leaves.copy()
        else:
            k = k + k_step
            # print(leaves)
            leaves = last_leaves.copy()
            # print(len(leaves))
            inner = last_inner.copy()

    return leaves, inner


if __name__ == "__main__":
    n, m = 100, 1000

    g = random_graph_num_edges(n, m)

    for _ in range(100):
        sol_init, _ = pure_greedy(g)
        sol = strategic_oscilation(g, 0.001, 1)

        print(nx.is_connected(sol))
        # visualize_sol(g, sol)
