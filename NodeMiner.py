import random
import networkx as nx
import math
import matplotlib.pyplot as plt
import community as community_louvain
from networkx import circular_layout
# import numpy as np


def normalize(edges):
    total_weight = 0
    for word, data in edges.items():
        total_weight = total_weight + data['weight']
    for word, data in edges.items():
        edges[word]['weight'] = edges[word]['weight'] / total_weight
    return edges


def upper_bound(edges):
    ordered_list = []
    for word, data in edges.items():
        ordered_list.append([word, data['weight']])
    ordered_list = sorted(ordered_list, key=lambda x: x[1])
    total = 0
    for i in range(len(ordered_list)):
        ordered_list[i][1] = ordered_list[i][1] + total
        total = ordered_list[i][1]
    return ordered_list


def recursive_call(g, node_one, word, walk_length):
    e = (g.adj[node_one]).copy()
    e = normalize(e)
    if walk_length >= len(e)*len(e):
        return walk_length
    ls = upper_bound(e)
    r = random.random()
    for m in ls:
        if r < m[1]:
            if m[0] == word:
                return walk_length
            else:
                return recursive_call(g, m[0], word, walk_length + 1)


def data_miner(node1, node2):
    file = open("conspiracy_comment_data.csv", "r")
    # setting the flag to false
    # setting index to start on first one
    index = 0
    # setting count at 0 to find data at start
    count_both = 0
    count_single = 0
    for line in file:
        index += 1
    # checks to see if both are met and if so flips flag and counts
        if node1 in line and node2 in line:
            count_both += 1
        if node1 in line:
            count_single += 1
    # print(count_both / count_single)
    return count_both / count_single


def node_cycler():
    # list can be changed whenever
    # pulled from data in another document
    node_one = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    node_two = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    i = 0
    # edit length to depend on node wanted
    while i < len(node_one):
        for x in node_two:
            # print(data_miner(node_one[i], x))
            # print(node_two[i], "|", x, data_miner(node_two[i], x))
            print("node1 is", node_two[i], "and node2 is", x, "and they occurred", data_miner(node_two[i], x))
        i += 1


# finds distance between nodes
def node_hopper():
    node_one = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    node_two = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    w_list = []
    g = nx.DiGraph()
    g.add_nodes_from(node_one)
    i = 0
    j = 0
    while i < len(node_one):
        for x in node_two:
            w = data_miner(node_one[i], x)
            if w != 1:
                w_list.append(w)
            else:
                continue
            g.add_edge(node_one[i], x, weight=w_list[j])
            # print(i, j, w_list[j])
            j += 1
        i += 1
    for n in node_one:
        for m in node_two:
            walk_list = []
            if n != m:
                for i in range(1000):
                    walk_length = recursive_call(g.copy(), n, m, 0)
                    walk_list.append(walk_length)
                print(n, m, sum(walk_list)/len(walk_list))


def grapher_circ():
    node_one = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    node_two = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    w_list = []
    c_list = ['red', 'blue', 'green', 'orange', 'yellow', 'indigo', 'violet', 'black', 'grey', 'magenta', 'lightblue', 'cyan']
    g = nx.Graph()
    g.add_nodes_from(node_one)
    i = 0
    j = 0
    while i < len(node_one):
        for x in node_two:
            w = data_miner(node_one[i], x)
            if w != 1:
                w_list.append(w)
            else:
                continue
            g.add_edge(node_one[i], x, color=c_list[i], weight=w_list[j])
            print(w_list[j])
            walk_length = recursive_call(g, node_one[i], "fuck", 0)
            print(walk_length)
            j += 1
        i += 1
    # print(g.number_of_nodes())
    # print(g.number_of_edges())
    colors = nx.get_edge_attributes(g, 'color').values()
    weights = nx.get_edge_attributes(g, 'weight').values()
    pos = circular_layout(g)
    nx.draw(g, pos, edge_color=list(colors), width=list(weights), with_labels=True, node_color='lightblue')
    plt.show()


def lou_length_nodes():
    node_one = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    node_two = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    w_list = []
    g = nx.Graph()
    g.add_nodes_from(node_one)
    i = 0
    j = 0
    while i < len(node_one):
        for x in node_two:
            w = data_miner(node_one[i], x)
            if w != 1:
                w_list.append(w)
            else:
                continue
            g.add_edge(node_one[i], x, weight=w_list[j])
            print(w_list[j])
            j += 1
        i += 1
    weights = nx.get_edge_attributes(g, 'weight').values()
    pos = nx.spring_layout(g)
    partition = community_louvain.best_partition(g)
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels)
    nx.draw_networkx_labels(g, pos=pos)
    nx.draw_networkx_nodes(g, pos, partition.keys(), node_size=12, node_color=list(partition.values()))
    nx.draw_networkx_edges(g, pos, width=list(weights), alpha=1.0)
    # finds the lengths
    # using E algorithm
    lengths = {}
    for edge in g.edges():
        start_node = edge[0]
        end_node = edge[1]
        lengths[edge] = round(math.sqrt(((pos[end_node][1]-pos[start_node][1])**2)+((pos[end_node][0]-pos[start_node][0])**2)), 2)
    # print(lengths)
    i = 1
    for key in lengths:
        print(i, end="")
        print(key, lengths[key])
        i += 1
    # print(g.number_of_nodes())
    # print(g.number_of_edges())
    plt.show()


def lou_weight_comm():
    node_one = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    node_two = ["covid", "fuck", "government", "mask", "money", "news", "old", "public", "time", "vaccine", "work", "years"]
    # w_list = []
    # v_list = []
    z_list = []
    g = nx.Graph()
    g.add_nodes_from(node_one)
    i = 0
    j = 0
    while i < len(node_one):
        for x in node_two:
            w = data_miner(node_one[i], x)
            v = data_miner(x, node_two[i])
            if w != 1:
                # w_list.append(w)
                # v_list.append(v)
                z = (w + v)/2
                z_list.append(z)
            else:
                continue
            g.add_edge(node_one[i], x, weight=z_list[j])
            # print(w_list[j])
            # print(v_list[j])
            j += 1
        i += 1
    # print(z_list)
    weights = nx.get_edge_attributes(g, 'weight').values()
    pos = nx.spring_layout(g)
    partition = community_louvain.best_partition(g)
    nx.draw_networkx_labels(g, pos=pos)
    nx.draw_networkx_nodes(g, pos, partition.keys(), node_size=12, node_color=list(partition.values()))
    nx.draw_networkx_edges(g, pos, width=list(weights), alpha=1.0)
    # print(G.number_of_nodes())
    # print(G.number_of_edges())
    plt.show()


# choose whichever is needed
if __name__ == "__main__":
    # data_miner(input1, input2)
    # node_hopper()
    # node_cycler()
    # lou_weight_comm()
    # grapher_circ()
    # lou_length_nodes()
    pass