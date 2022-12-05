from helper import *
from sat_sol import *
from combination_algorithm import *
import numpy as np


def get_diff(g):
    # Check valid
    mst = generate_random_spanning_tree(g)
    if not is_spanning_tree(g, mst):
        raise Exception("Invalid MST")
    print(g)
    start = time.time()
    opt = sat_solve(g, 0)
    end = time.time()
    print("SAT time:", end - start)
    if not opt:
        print("OPT FAILED")
        return -1
    start = time.time()
    basic = good_solve(g, opt)
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


def connect_unconnected(G):
    from itertools import combinations, groupby

    components = dict(enumerate(nx.connected_components(G)))
    components_combs = combinations(components.keys(), r=2)

    for _, node_edges in groupby(components_combs, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_comps = random.choice(node_edges)
        source = random.choice(list(components[random_comps[0]]))
        target = random.choice(list(components[random_comps[1]]))
        G.add_edge(source, target)


def generate_idea():
    # Create random sparse graph with 20 nodes
    g1 = nx.gnm_random_graph(12, 12)
    connect_unconnected(g1)

    g2 = nx.gnm_random_graph(12, 12)
    connect_unconnected(g2)

    # Make a graph connecting the two
    g = nx.disjoint_union(g1, g2)

    # Add edges between the two
    for i in range(12):
        g.add_edge(i, i + 12)

    g3 = random_graph_prob_edges(76, 0.3)

    g_prime = nx.disjoint_union(g, g3)

    # Add edges between the two
    for i in range(24, 100):
        g_prime.add_edge(i, (i - 23) // 6)

    # visualize_graph(g_prime)
    return g_prime


def bimodal(mu1, mu2, sigma1, sigma2, p, n):
    degrees = [
        int(x) for x in np.random.normal(mu1, sigma1, int(p * g.number_of_nodes()))
    ]
    degrees += [
        int(x) for x in np.random.normal(mu2, sigma2, n - int(p * g.number_of_nodes()))
    ]

    degrees = [x if x > 2 else 2 for x in degrees]
    degrees = [x if x < n // 2 else n // 2 for x in degrees]
    # print(degrees)

    if sum(degrees) % 2 == 1:
        degrees[0] += 1

    g = nx.configuration_model(degrees)

    # turn g into simple graph
    g = nx.Graph(g)
    g.remove_edges_from(nx.selfloop_edges(g))
    return g


def hypercube():
    g = nx.hypercube_graph(6)
    connect_unconnected(g)

    # Convert to undirected graph
    g_prime = nx.Graph()
    for s, t in g.edges():
        # convert s and t to strings
        s = int("".join(map(str, s)), 2)
        t = int("".join(map(str, t)), 2)

        g_prime.add_edge(s, t)
    print(g_prime.edges())
    g = g_prime


def random_tree(n):
    return nx.random_tree(n)


def obfuscate(tree):
    g = nx.Graph()
    g.add_nodes_from(tree.nodes())
    g.add_edges_from(tree.edges())

    leaves = [x for x in g.nodes() if g.degree(x) == 1]

    to_add = {}
    for leaf in leaves:
        # Get the parent of the leaf
        parent = [x for x in tree.neighbors(leaf)][0]
        to_add[leaf] = tree.degree(parent) - 1  # degree of leaf is 1

    possible_edges = list(itertools.combinations(leaves, 2))
    random.shuffle(possible_edges)

    for s, t in possible_edges:
        if to_add[s] and to_add[t]:
            g.add_edge(s, t)
            to_add[s] -= 1
            to_add[t] -= 1

    return g


if __name__ == "__main__":
    c = 0
    n = 100
    factor = 1

    # as a list comprehension
    samples = [x for x in range(150, 2000, 50)]

    samples = {x: 25 for x in samples}
    while True:
        try:
            # either 50 or 100
            n = random.choice([50, 100])
            factor = 1 / (100 / n)
            # n = 100
            # # Normal distribution 1
            # mu1 = 8
            # sigma1 = 3

            # # Normal distribution 2
            # mu2 = n / 4
            # sigma2 = n / 10

            # mu2 = mu1
            # sigma2 = sigma1
            # g = bimodal(mu1, mu2, sigma1, sigma2, 0.5, n)
            # g = nx.waxman_graph(100, 0.8)
            # g = generate_idea()
            # g = nx.relaxed_caveman_graph(10, 10, 0.1)

            # visualize_graph(g_prime)
            size_choice = random.choices(
                list(samples.keys()), weights=samples.values(), k=1
            )[0]
            size = size_choice * factor
            size = int(size)

            g = random_graph_num_edges(n, size)
            # g = random_graph_num_edges(100, random.randint(150, 1400))
            # if random.random() < 0.7:
            #     g = random_graph_num_edges(100, 500)
            t = bad_solve(g)
            # t = random_tree(100)
            # while num_leaves(t) < 80:
            #     t = random_tree(100)
            start_leaves = num_leaves(t)
            # print(num_leaves(t))

            g = obfuscate(t)
            st = good_solve(g, start_leaves - factor * 4)
            end_leaves = num_leaves(st)
            # print(num_leaves(st))
            # print("")
            diff = start_leaves - end_leaves

            # diff = get_diff(g)
            c += 1
            # print(size, factor*4)
            if diff > factor * 4 - 1:
                samples[size_choice] += int((diff - factor * 4 + 1) ** 2 * 3)
                print(
                    "Diff:",
                    diff,
                    "End leaves:",
                    end_leaves,
                    "Start leaves:",
                    start_leaves,
                )

                if diff > factor * 4:
                    write_graph_to_file(g, f"{c} in", f"hard_in{n}{diff}.txt")
                    write_graph_to_file(t, f"{c} out", f"hard_out{n}{diff}.txt")
                # print(f"wrote, {diff}")
            else:
                samples[size_choice] -= 1
                if sum(samples.values()) == 0:
                    samples = [x for x in range(150, 2000, 50)]
                    samples = {x: 25 for x in samples}
            if c % 1000 == 0:
                print("ONE THOUSAND:", c, samples)
        except Exception as e:
            print(f"Failed", e)
            continue
