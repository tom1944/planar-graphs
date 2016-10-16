"""Usage: easy_planar_test.py M N OUTPUT
"""
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')  # nopep8
import matplotlib.pyplot as plt
import planarity
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    M = int(arguments['M'])
    N = int(arguments['N'])
    output = arguments['OUTPUT']

    G = nx.gnm_random_graph(M, N)

    try:
        print("Graph is planar")
        planarity.draw(G)
        plt.axis('off')
        plt.savefig(output)
    except:
        print("Graph not planar!")
        nx.draw_random(G)
        plt.axis('off')
        plt.savefig(output)
