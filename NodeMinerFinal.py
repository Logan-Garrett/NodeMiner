# take the two words you want compared
# opens the file you want to scan

def data_miner(node1, node2):
    # change for whatever you need
    file = open("coronavirus_comment_data.csv", "r")
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
    while i < len(node_two):
        for x in node_one:
            print("node1 is", node_two[i], "and node2 is", x, "and they occurred", data_miner(node_two[i], x))
        i += 1


node_cycler()
