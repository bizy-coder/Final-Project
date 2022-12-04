from helper import *
from heuristics import *  # For testing

import itertools



def get_1_change(g, st):
    # Look at all possible edges that could be removed
    for node in g:
        # if it is a leaf in the spanning tree
        if st.degree(node) == 1:
            # Get the neighbor of the leaf
            neighbor = list(st.neighbors(node))[0]

            for v in g[node]:
                if v != neighbor and st.degree(v) > 1:
                    # If it increases the number of leaves, add it to the list of changes
                    if st.degree(neighbor) == 2:
                        # Remove the edge between the leaf and its neighbor
                        st.remove_edge(node, neighbor)
                        # Add the edge between the leaf and the new neighbor
                        st.add_edge(node, v)
                        return st
    return False

def one_local_search(g, st):
    flag = True
    while flag:
        flag = False
        # Get the 1-change
        new_st = get_1_change(g, st)
        if new_st:
            flag = True
            st = new_st
    return st

if __name__ == "__main__":
    g = random_graph_num_edges(10, 20)

    st = generate_random_spanning_tree(g)
    print(type(st), len(st.nodes()), len(st.edges()))
    print(num_leaves(st))

    # visualize_sol(g, st, True)

    st2 = one_local_search(g, st)
    print(type(st2), len(st2.nodes()), len(st2.edges()))
    print(num_leaves(st2))

    # visualize_sol(g, st2, True)

