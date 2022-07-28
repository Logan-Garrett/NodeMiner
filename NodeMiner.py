import csv
import random
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from matplotlib import cm
from networkx import circular_layout
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
    file = open(file_choice[2] + ".csv", "r")
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
            if data_miner(node_two[i], x) != 1.0:
                print(node_two[i], x, data_miner(node_two[i], x))
                # print(node_two[i], x)
            # print("node1 is", node_two[i], "and node2 is", x, "and they occurred", data_miner(node_two[i], x))
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
                for i in range(500):
                    walk_length = recursive_call(g.copy(), n, m, 0)
                    walk_list.append(walk_length)
                print(n, m, sum(walk_list)/len(walk_list))
                y = sum(walk_list) / len(walk_list)
                prehop_list.append(n)
                prehop_list.append(m)
                prehop_list.append(y)
                hop_list.append(prehop_list)
                prehop_list = []

                # print(hop_list)

    # named_tuple = time.localtime()
    # time_string = time.strftime("%H:%M:%S", named_tuple)
    # filename = time_string + '_' + 'file' + ".csv"
    name = "date_name"
    filename = name + "_data" + ".csv"
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
    partition = community_louvain.best_partition(g)
    cmap = cm.get_cmap('viridis', max(partition.values())+1)
    nx.draw_networkx_labels(g, pos=pos)
    nx.draw_networkx_nodes(g, pos, partition.keys(), cmap=cmap, node_size=42, node_color=list(partition.values()))
    nx.draw_networkx_edges(g, pos, width=list(weights), alpha=0.5)
    # print(G.number_of_nodes())
    # print(G.number_of_edges())
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
    cc_list = []
    ca_list = []
    cona_list = []
    i = 0
    j = 0
    while i < len(corona_list):
        precc_list = []
        c = float(corona_list[i][j]) - float(conspiracy_list[i][j])
        precc_list.append(c)
        cc_list.append(precc_list)
        print(c)
        i += 1
        precc_list = []
        filename = "CoronavirusMinusConspiracy_data" + ".csv"
        with open(filename, 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(cc_list)
    # cona - askReddit
    i = 0
    j = 0
    while i < len(conspiracy_list):
        precona_list = []
        c = float(conspiracy_list[i][j]) - float(ask_list[i][j])
        precona_list.append(c)
        cona_list.append(precona_list)
        print(c)
        i += 1
        precona_list = []
        filename = "ConspiracyMinusAskReddit_data" + ".csv"
        with open(filename, 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(cona_list)
    # Corona - askReddit
    i = 0
    j = 0
    while i < len(corona_list):
        preca_list = []
        c = float(corona_list[i][j]) - float(ask_list[i][j])
        preca_list.append(c)
        ca_list.append(preca_list)
        print(c)
        i += 1
        preca_list = []
        filename = "CoronaMinusAskReddit_data" + ".csv"
        with open(filename, 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(ca_list)

    # print(cc_list)


# choose whichever is needed
if __name__ == "__main__":
    # this allows you to choose two words and find the frequency
    # data_miner(input1, input2)

    # this allows you to find the hopping distance a list of nodes
    # node_hopper()

    # this is for when you have a list of nodes, and you need to cycle through them
    node_cycler()

    # This is used to find the weights of the lines for the diagram
    # lou_weight_graph()

    # this graphs in a circle and shows every line with the ability to show in colors
    # grapher_circ()


    # compares the diff reddits in terms of data
    # compare_hop_dist()
    # pass
