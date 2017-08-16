#!/usr/bin/env python3
# coding: utf-8
# File: directed_pageRank.py
# Author: lxw
# Date: 8/16/17 11:25 AM

import sys

import matplotlib.pyplot as plt
import networkx as nx

from utils import parse


class PageRankDirected:
    def __init__(self, graph):
        self.graph = graph
        self.V = len(self.graph)
        self.d = 0.85  # For d, which is the probability that the user will randomly go to a different page, we chose .85 which is what the book had as the probability for d.
        self.ranks = dict()

    def show_graph(self, sorted_r):
        """
        :param sorted_r: SORTED
        <class 'list'>: [('Connecticut', 0.08394732421875001), ('Buffalo', 0.07670273437500001), ('Ball State', 0.049429687500000014), ('Northeastern', 0.0346875), ('Syracuse', 0.033492187500000006), ('Central Michigan', 0.018750000000000003), ('Ohio', 0.018750000000000003), ('UC Davis', 0.018750000000000003)]
        """
        # nx.draw_networkx(self.graph)
        pos = nx.spring_layout(self.graph)
        node_list = [item[0] for item in sorted_r]
        node_size = [item[1]* 20000 for item in sorted_r]
        # print(node_list)
        # print(node_size)
        # print(self.graph.nodes(data=True))
        # print(sorted_r)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=node_list, node_size=node_size)
        nx.draw_networkx_edges(self.graph, pos, width=1)
        labels = {item[0]:"{0}\n{1:.6f}".format(item[0], item[1]) for item in sorted_r}
        nx.draw_networkx_labels(self.graph, pos, labels=labels)
        plt.show()

    def rank(self):
        # print(type(self.graph))    # <class 'networkx.classes.digraph.DiGraph'>
        # print(len(self.graph))    # 8
        # print(self.graph.number_of_nodes())  # 8
        # print(self.graph.number_of_edges())  # 7
        # print(self.graph.edges())  # [('Northeastern', 'Ball State'), ('Northeastern', 'Syracuse'), ('Ball State', 'Buffalo'), ('Central Michigan', 'Ball State'), ('Buffalo', 'Connecticut'), ('Ohio', 'Buffalo'), ('UC Davis', 'Northeastern')]
        for key, node in self.graph.nodes(data=True):  # key: "Ball State", node: {}
            self.ranks[key] = 1 / float(self.V)  # 全部赋值为初始值： 1/8 = 0.125

        for _ in range(100):
            for key, node in self.graph.nodes(data=True):  # key: "Northeastern", node: {}
                rank_sum = 0
                # neighbors = self.graph.out_edges(key)  # neighbors: [('Northeastern', 'Ball State'), ('Northeastern', 'Syracuse')]
                predecessors = self.graph.predecessors(key)    # predecessors: ['UC Davis']
                for n in predecessors:
                    outlinks = self.graph.out_degree(n)
                    if outlinks > 0:
                        rank_sum += (1 / float(outlinks)) * self.ranks[n]

                # The actual page rank computation
                self.ranks[key] = (1 - float(self.d)) * (1 / float(self.V)) + self.d * rank_sum


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # print('Expected input format: python pageRank.py <data_filename> <directed OR undirected>')
        print("Expected input format: python directed_pageRank.py <data_filename>")
    else:
        filename = sys.argv[1]
        isDirected = True
        graph = parse(filename, isDirected)
        p = PageRankDirected(graph)
        p.rank()

        # sorted_r = sorted(p.ranks.iteritems(), key=operator.itemgetter(1), reverse=True)    # Python2
        # sorted_r = sorted(p.ranks.items(), key=operator.itemgetter(1), reverse=True)    # Python3
        sorted_r = sorted(p.ranks.items(), key=lambda item: item[1], reverse=True)  # Python3: seemed OK.
        # p.ranks.items(): [('Northeastern', 0.0346875), ('Ball State', 0.049429687500000014), ('Central Michigan', 0.018750000000000003), ('Buffalo', 0.07670273437500001), ('Ohio', 0.018750000000000003), ('Connecticut', 0.08394732421875001), ('Syracuse', 0.033492187500000006), ('UC Davis', 0.018750000000000003)]
        p.show_graph(sorted_r)

        for tup in sorted_r:
            print('{0:30}:{1:10}'.format(str(tup[0]), tup[1]))
