import networkx as nx

""""
algoritme om te gebruiken:
Maak een volledige partitie P van de nodes.
voor alle paren deelverzamelingen:
    merge ze
    als de subgrafen van alle deelverzamelingen in de partitie nog steeds planair zijn
        ga de recursie in
    anders
        unmerge ze
        thickness_until_now = min(thickness_until_now, size_of(P) )
"""


def thickness(g):
    if is_planar(g):
        return 1

    partition = [[node] for node in g.nodes]
    thickness_until_now = len(partition)  # the cardinality of the partition
    return recursive_thickness(partition, thickness_until_now)


def recursive_thickness(partition, thickness_until_now):
    for s1 in partition:  # s stands for subset, it is a subset of the graph
        for s2 in partition:
            if s1 != s2:
                s_new = s1 + s2
                if is_planar(g.subgraph(s_new)):
                    partition.remove(s1)
                    partition.remove(s2)
                    partition.append(s_new)
                    recursive_thickness(partition, thickness_until_now)
                    partition.remove(s_new)
                    partition += [s1, s2]
                else:
                    thickness_until_now = min(thickness_until_now, len(partition))  # Omdat we al hebben gecheckt of de
                    # graaf panair is, weten we zeker dat dit statement sowieso 1 keer uitgevoerd wordt.
                    # Als we dat niet zouden checken, en de graaf zou planair zijn, dan wordt de thickness gelijk aan
                    # het aantal nodes in de graaf.

    return thickness_until_now


# a stub, needs to be implemented, possibly in another file/module/unit
def is_planar(g):
    return False


def test_thickness(g):
    print("thickness: " + str(thickness(g)))


if __name__ == "__main__":
    print("hello world")
    g = nx.Graph()
    g.add_edge(1, 2)
    g.add_node("kaas")
    test_thickness(g)
