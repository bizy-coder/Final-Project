from helper import *
from sat_sol import *
from combination_algorithm import *


def get_diff(g):
    # Check valid
    mst = generate_random_spanning_tree(g)
    if not is_spanning_tree(g, mst):
        raise Exception("Invalid MST")
    print(g)
    start = time.time()
    opt = sat_solve(g)
    end = time.time()
    print("SAT time:", end - start)
    if not opt:
        print("OPT FAILED")
        return
    start = time.time()
    basic = basic_solve(g)
    end = time.time()
    print("Basic time:", end - start)
    return num_leaves(opt) - num_leaves(basic)


def enhance_g(g, k):
    curr_diff = get_diff(g)
    while len(g.edges()) < 2000:
        # Generate 10 random edges
        edges = []
        for _ in range(k):
            edge = list(g.edges())[0]
            while edge not in g.edges() and edge not in edges and edge[0] != edge[1]:
                a = random.choice(list(g.nodes()))
                b = random.choice(list(g.nodes()))
                edge = (a, b)
                edges.append(edge)
        g.add_edges_from(edges)
        new_diff = get_diff(g)
        if new_diff >= curr_diff:
            curr_diff = new_diff
            print("New diff:", curr_diff)
            print("New edges:", edges)
        else:
            g.remove_edges_from(edges)
    return g


for g in list(read_hard_file("hard_in4.txt"))[1:]:
    # x = get_diff(g)
    enhance_g(g, 20)
    # print([g.degree(x) for x in g.nodes()])
    # if x > 3:
    #     write_graph_to_file(g, f"diff={x}", f"hard_in{x}.txt")


# if __name__ == "__main__":
#     for g in list(read_hard_file("test.txt"))[1:]:
#         write_graph_to_file(g, f"diff={x}", f"hard_in{x}.txt")
# c = 0
# while True:
#     try:
#         nums, desc = random_distribution_choice(50)
#         nums = [max(2, math.ceil(x / 2)) for x in nums]
#         g = nx.random_degree_sequence_graph(nums)

#         diff = get_diff(g)
#         if diff:
#             c += 1
#             write_graph_to_file(
#                 g, f"desc={desc}; diff={diff}", f"hard_in50{diff}.txt"
#             )
#             print(f"wrote, {diff}")
#     except Exception as e:
#         print(f"Failed", e)
#         continue
