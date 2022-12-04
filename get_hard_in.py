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


for g in list(read_hard_file("test.txt"))[1:]:
    x = get_diff(g)
    print([g.degree(x) for x in g.nodes()])
    if x > 3:
        write_graph_to_file(g, f"diff={x}", f"hard_in{x}.txt")


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
