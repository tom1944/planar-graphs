#!/usr/bin/python3
"""Usage: cli.py M N OUTPUT
"""
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')  # nopep8
import matplotlib.pyplot as plt
import planarity
import planarity_test as p
from docopt import docopt

import planarity_test

def draw(G, output):
    planarity.draw(G)
    plt.axis('off')
    plt.savefig(output)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    M = int(arguments['M'])
    N = int(arguments['N'])
    output = arguments['OUTPUT']
    # G = nx.complete_multipartite_graph(M, N)
    # G = nx.complete_graph(M)
    G = nx.gnm_random_graph(M, N)

    if planarity_test.is_planar(G):
        print("Graph is planar")
        try:
            draw(G, output)
            print("Planar graph drawn!")
        except:
            print("Could not draw a planar graph...")
            nx.draw_random(G)
            plt.axis('off')
            plt.savefig(output)
    else:
        if planarity.is_planar(G):
            draw(G, output)
            print("Graph is unexpectedly planar...")
        else:
            nx.draw_random(G)
            plt.axis('off')
            plt.savefig(output)
            print("Graph is not planar!")
