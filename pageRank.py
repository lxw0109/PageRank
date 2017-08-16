import math, random, sys, csv
import operator

import matplotlib.pyplot as plt
import networkx as nx

from utils import parse, print_results

# lxw Modification
"""
def rank(graph, node):
    #V
    nodes = graph.nodes()
    #|V|
    nodes_sz = len(nodes)
    #I
    neighbs = graph.neighbors(node)
    #d
    rand_jmp = random.uniform(0, 1)

    ranks = []
    # ranks.append((1 / nodes_sz))
    ranks.append(1 / nodes_sz)

    d = 0.85

    for n in nodes:
        rank = (1-rand_jmp) * (1/nodes_sz)
        trank = 0
        for nei in neighbs:
            trank += (1/len(neighbs)) * ranks[len(ranks)-1]
        rank = rank + (d * trank)
        ranks.append(rank)
"""


class PageRank:
    def __init__(self, graph, directed):
        self.graph = graph
        self.V = len(self.graph)
        self.d = 0.85    # For d, which is the probability that the user will randomly go to a different page, we chose .85 which is what the book had as the probability for d.
        self.directed = directed
        self.ranks = dict()

    def show_graph(self, sorted_r):
        """
        :param sorted_r: SORTED
        <class 'list'>: [('Connecticut', 0.08394732421875001), ('Buffalo', 0.07670273437500001), ('Ball State', 0.049429687500000014), ('Northeastern', 0.0346875), ('Syracuse', 0.033492187500000006), ('Central Michigan', 0.018750000000000003), ('Ohio', 0.018750000000000003), ('UC Davis', 0.018750000000000003)]
        """
        # nx.draw_networkx(self.graph)
        pos = nx.spring_layout(self.graph)
        node_list = [item[0] for item in sorted_r]
        node_size = [item[1] * 10000 for item in sorted_r]
        # print(node_list)
        # print(node_size)
        # print(self.graph.nodes(data=True))
        # print(sorted_r)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=node_list, node_size=node_size)
        nx.draw_networkx_edges(self.graph, pos, width=1)
        labels = {item[0]: "{0}\n{1:.6f}".format(item[0], item[1]) for item in sorted_r}
        nx.draw_networkx_labels(self.graph, pos, labels=labels)
        plt.show()

    def rank(self):
        # print(type(graph))    # <class 'networkx.classes.digraph.DiGraph'>
        # print(len(graph))    # 8
        # print(graph.number_of_nodes())  # 8
        # print(graph.number_of_edges())  # 14
        for key, node in self.graph.nodes(data=True):    # key: "Ball State", node: {}
            if self.directed:
                self.ranks[key] = 1/float(self.V)    # 全部赋值为初始值： 1/14 = 0.07142857142857142
            else:
                self.ranks[key] = node.get('rank')

        for _ in range(20):
            for key, node in self.graph.nodes(data=True):    # key: "Ball State", node: {}
                rank_sum = 0
                # lxw Modification
                # curr_rank = node.get('rank')  # useless?
                if self.directed:
                    neighbors = self.graph.out_edges(key)    # neighbors: [('Ball State', 'Northeastern'), ('Ball State', 'Central Michigan')]
                    for n in neighbors:
                        outlinks = len(self.graph.out_edges(n[1]))    # self.graph.out_edges(n[1]): [('Northeastern', 'UC Davis')]
                        if outlinks > 0:
                            rank_sum += (1 / float(outlinks)) * self.ranks[n[1]]
                else: 
                    neighbors = self.graph[key]
                    for n in neighbors:
                        if self.ranks[n] is not None:
                            outlinks = len(self.graph.neighbors(n))
                            rank_sum += (1 / float(outlinks)) * self.ranks[n]
            
                # The actual page rank computation
                self.ranks[key] = ((1 - float(self.d)) * (1/float(self.V))) + self.d * rank_sum

        return p


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Expected input format: python pageRank.py <data_filename> <directed OR undirected>')
    else:
        filename = sys.argv[1]
        isDirected = False
        if sys.argv[2] == 'directed':
            isDirected = True

        graph = parse(filename, isDirected)
        p = PageRank(graph, isDirected)
        p.rank()

        # lxw Modification
        # sorted_r = sorted(p.ranks.iteritems(), key=operator.itemgetter(1), reverse=True)    # Python2
        # sorted_r = sorted(p.ranks.items(), key=operator.itemgetter(1), reverse=True)    # Python3
        sorted_r = sorted(p.ranks.items(), key=lambda item:item[1], reverse=True)    # Python3: seemed OK.
        p.show_graph(sorted_r)

        for tup in sorted_r:
            print('{0:30}:{1:10}'.format(str(tup[0]), tup[1]))

        """
        for node in graph.nodes():
            print(node + rank(graph, node))
            neighbs = graph.neighbors(node)
            print(node + " " + str(neighbs))
            print(random.uniform(0,1))
        """

