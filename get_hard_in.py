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
        return -1
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
            while edge in list(g.edges()) or edge in edges or edge[0] == edge[1]:
                a = random.choice(list(g.nodes()))
                b = random.choice(list(g.nodes()))
                edge = (a, b)
            # print(edge)
            edges.append(edge)
        g.add_edges_from(edges)
        new_diff = get_diff(g)
        print("Diff:", new_diff)
        if new_diff >= curr_diff:
            curr_diff = new_diff
            print("New diff:", curr_diff)
            print("New edges:", edges)
        else:
            g.remove_edges_from(edges)
            print("Failed update")
    return g


# for g in list(read_hard_file("hard_in4.txt")):
#     # x = get_diff(g)
#     enhance_g(g, 10)
# print([g.degree(x) for x in g.nodes()])
# if x > 3:
#     write_graph_to_file(g, f"diff={x}", f"hard_in{x}.txt")


if __name__ == "__main__":
    c = 0
    while True:
        try:
            n = 50
            # Normal distribution 1
            mu1 = 4
            sigma1 = 1

            # Normal distribution 2
            mu2 = n / 2
            sigma2 = n / 10

            # Combine the two distributions
            degrees = [int(x) for x in np.random.normal(mu1, sigma1, n // 2)]
            degrees += [int(x) for x in np.random.normal(mu2, sigma2, n // 2)]

            degrees = [x if x > 2 else 2 for x in degrees]
            degrees = [x if x < n // 2 else n // 2 for x in degrees]
            print(degrees)
            g = nx.havel_hakimi_graph(degrees)

            diff = get_diff(g)
            if diff:
                c += 1
                print("Diff:", diff)
                write_graph_to_file(g, f" diff={diff}", f"hard_in50{diff}.txt")
                print(f"wrote, {diff}")
        except Exception as e:
            print(f"Failed", e)
            continue
