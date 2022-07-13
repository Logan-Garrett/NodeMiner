import csv
import random
from datetime import time, date, datetime
import time
import networkx as nx
import math
import matplotlib.pyplot as plt
import community as community_louvain
from matplotlib import cm
from networkx import circular_layout
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import numpy as np
import sys
sys.setrecursionlimit(100000)


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
    # i = 0
    file_choice = ["coronavirus_comment_data", "conspiracy_comment_data", "askReddit_comment_data"]
    # this fix
    # while i < len(file_choice):
    file = open(file_choice[0] + ".csv", "r")
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
    node_one = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    node_two = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
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
    node_one = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    node_two = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    w_list = []
    hop_list = []
    prehop_list = []
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
                for i in range(1):
                    walk_length = recursive_call(g.copy(), n, m, 0)
                    walk_list.append(walk_length)
                # print(n, m, sum(walk_list)/len(walk_list))
                y = sum(walk_list) / len(walk_list)
                prehop_list.append(y)
                hop_list.append(prehop_list)
                prehop_list = []

                # print(hop_list)

    named_tuple = time.localtime()
    time_string = time.strftime("%H:%M:%S", named_tuple)
    filename = time_string + '_' + 'file' + ".csv"
    with open(filename, 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(hop_list)

    # for h in hop_list:
    #     print(h)


def grapher_circ():
    node_one = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    node_two = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
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
            g.add_edge(node_one[i], x, weight=w_list[j])
            print(w_list[j])
            j += 1
        i += 1
    # print(g.number_of_nodes())
    # print(g.number_of_edges())
    # colors = nx.get_edge_attributes(g, 'color').values()
    weights = nx.get_edge_attributes(g, 'weight').values()
    pos = circular_layout(g)
    nx.draw(g, pos, width=list(weights), with_labels=True, node_color='lightblue')
    plt.show()


def lou_weight_nodes():
    node_one = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    node_two = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    w_list = []
    g = nx.Graph()
    g.add_nodes_from(node_one)
    i = 0
    j = 0
    while i < len(node_one):
        for x in node_two:
            w = data_miner(node_one[i], x)
            y = data_miner(x, node_one[i])
            if w != 1:
                z = (w + y)/2
                w_list.append(z)
            else:
                continue
            g.add_edge(node_one[i], x, weight=w_list[j])
            # print(w_list[j])
            j += 1
        i += 1
    # weights = nx.get_edge_attributes(g, 'weight').values()
    pos = nx.spring_layout(g)
    # partition = community_louvain.best_partition(g)
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels)
    # nx.draw_networkx_labels(g, pos=pos)
    # nx.draw_networkx_nodes(g, pos, partition.keys(), node_size=12, node_color=list(partition.values()))
    # nx.draw_networkx_edges(g, pos, width=list(weights), alpha=1.0)
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


def lou_weight_graph():
    node_one = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    node_two = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    # w_list = []
    # v_list = []
    z_list = []
    # find new graph
    g = nx.Graph()
    # g = nx.karate_club_graph()
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
                # try just w again
                z = (w + v)/2
                z_list.append(z)
            else:
                continue
            g.add_edge(node_one[i], x, weight=z_list[j])
            # g.add_edge(node_one[i], x, weight=z_list[j])
            print(z_list[j])
            # print(v_list[j])
            j += 1
        i += 1
    # print(z_list)
    weights = nx.get_edge_attributes(g, 'weight').values()
    pos = nx.spring_layout(g)
    partition = community_louvain.best_partition(g, resolution=4)
    cmap = cm.get_cmap('viridis', max(partition.values())+1)
    nx.draw_networkx_labels(g, pos=pos)
    nx.draw_networkx_nodes(g, pos, partition.keys(), cmap=cmap, node_size=42, node_color=list(partition.values()))
    nx.draw_networkx_edges(g, pos, width=list(weights), alpha=0.5)
    # print(G.number_of_nodes())
    # print(G.number_of_edges())
    plt.show()


def elbow_grapher():
    node_one = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    node_two = ["america",
        "believe",
        "children",
        "companies",
        "country",
        "covid",
        "days",
        "death",
        "died",
        "different",
        "free",
        "friends",
        "fuck",
        "gets",
        "government",
        "hate",
        "hell",
        "help",
        "instead",
        "kids",
        "lets",
        "life",
        "little",
        "live",
        "love",
        "money",
        "need",
        "news",
        "people",
        "problem",
        "public",
        "seems",
        "sick",
        "side",
        "state",
        "stupid",
        "taking",
        "time",
        "trying",
        "vaccine",
        "work",
        "world",
        "year"]
    w_list = []
    v_list = []
    # z_list = []
    i = 0
    j = 0
    while i < len(node_one):
        for x in node_two:
            w = data_miner(node_one[i], x)
            v = data_miner(x, node_two[i])
            if w != 1:
                w_list.append(w)
                v_list.append(v)
                # try just w again
                # z = np.array(list(zip(w_list, v_list))).reshape(len(w_list), 2)
                # z_list.append(z)
                # X = np.array(list(zip(w_list, v_list))).reshape(len(w_list), 2)
            else:
                continue
            j += 1
        i += 1
    x1 = np.array(w_list)
    x2 = np.array(v_list)
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
    # graphs on diagram to show clustering
    # plt.plot()
    # plt.xlim([0.00000000000000000, 1])
    # plt.ylim([0.00000000000000000, 1])
    # plt.title('Dataset')
    # plt.scatter(w_list, v_list)
    # plt.show()
    distortions = []
    inertias = []
    mapping1 = {}
    mapping2 = {}
    K = range(1, 10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
        inertias.append(kmeanModel.inertia_)
        mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0]
        mapping2[k] = kmeanModel.inertia_
    # Distortion graph
    # plt.plot(K, distortions, 'bx-')
    # plt.xlabel('Values of K')
    # plt.ylabel('Distortion')
    # plt.title('The Elbow Method using Distortion')
    # plt.show()
    # inertia graph
    plt.plot(K, inertias, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method using Inertia')
    plt.show()


def compare_hop_dist():
    with open('conspiracy_hopper_data.csv') as conspiracy_file:
        reader = csv.reader(conspiracy_file)
        conspiracy_list = list(reader)
    with open('coronavirus_hopper_data.csv') as corona_file:
        reader = csv.reader(corona_file)
        corona_list = list(reader)
    with open('askReddit_hopper_data.csv') as ask_file:
        reader = csv.reader(ask_file)
        ask_list = list(reader)
    i = 0
    while i < len(corona_list):
        cc_list = []
        cc = corona_list[i] - conspiracy_list[i]
        cc_list.append(cc)
        print(cc_list)
        i += 1
    while i < len(corona_list):
        ca_list = []
        ca = corona_list[i] - ask_list[i]
        ca_list.append(ca)
        print(ca_list)
        i += 1
    while i < len(conspiracy_list):
        coa_list = []
        coa = conspiracy_list[i] - ask_list[i]
        coa_list.append(coa)
        print(coa_list)
        i += 1


# choose whichever is needed
if __name__ == "__main__":
    # this allows you to choose two words and find the frequency
    # data_miner(input1, input2)

    # this allows you to find the hopping distance a list of nodes
    node_hopper()

    # this is for when you have a list of nodes, and you need to cycle through them
    # node_cycler()

    # This is used to find the weights of the lines for the diagram
    # lou_weight_graph()

    # this graphs in a circle and shows every line with the ability to show in colors
    # grapher_circ()

    # This is used to find the distance of the nodes based on matplot graph and weighted communities of nodes
    # lou_weight_nodes()

    # elbow grapher
    # elbow_grapher()

    # compares the diff reddits in terms of data
    # compare_hop_dist()
    # pass
