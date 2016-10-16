import networkx as nx
import planarity_test


def thickness(g):
    return thickness_merge(g)

""""
Dit algoritme(ik noem het het merge algoritme) is erg ingewikkeld. Het is ontiegelijk langzaam en ik weet geeneens of
het werkt voor grafen met een thickness groter dan 1. Misschien zitten er fouten in het algoritme of in de implementatie
Het idee van dit algoritme was om een volledige partitie van de edges te maken en ze voorzichtig samen te voegen.

merge algoritme:
Maak een volledige partitie P van de edges.
voor alle paren deelverzamelingen:
    merge ze
    als de subgraaf gegenereerd door de nieuwe subset van edges planair is
        ga de recursie in
    anders
        unmerge ze
        thickness_until_now = min(thickness_until_now, size_of(P) )
"""


def thickness_merge(g):
    if planarity_test.is_planar(g):
        return 1

    partition = [[edge] for edge in g.edges()]
    thickness_until_now = len(partition)  # the cardinality of the partition
    return recursive_thickness(g, partition, thickness_until_now)


def recursive_thickness(g, partition, thickness_until_now):
    p2 = partition.copy()  # we cant add and delete things to the partition while iterating, so we need a copy
    # of the partition for that
    # print(partition)
    for s1 in partition:  # s stands for subset, it is a subset of the graph
        for s2 in partition:
            if s1 != s2:
                s_new = s1 + s2
                g2 = nx.Graph()
                g2.add_edges_from(s_new)
                if planarity_test.is_planar(g2):
                    p2.remove(s1)
                    p2.remove(s2)
                    p2.append(s_new)
                    thickness_until_now = recursive_thickness(g, p2, thickness_until_now)
                    p2.remove(s_new)
                    p2.append(s1)
                    p2.append(s2)
                else:
                    thickness_until_now = min(thickness_until_now, len(partition))  # Omdat we al hebben gecheckt of de
                    # graaf panair is, weten we zeker dat dit statement sowieso 1 keer uitgevoerd wordt.
                    # Als we dat niet zouden checken, en de graaf zou planair zijn, dan wordt de thickness gelijk aan
                    # het aantal nodes in de graaf.
    return thickness_until_now


if __name__ == "__main__":
    graph = nx.complete_bipartite_graph(3, 3)
    print(thickness(graph))

""" OUTDATED
A worst-case time complexity analysis of the thickness
define a_k as the worst-case number of operations in recursive_thickness if the partition size is k.
n denotes the number of elements of the graph
planarity(i) denotes the complexity of the planarity check (planarity_test.is_planar) of a graph with i nodes

We need to determine a recursive formula for a_k:

def recursive_thickness(partition, thickness_until_now):
    for s1 in partition:  		=> k times
        for s2 in partition:				=> k times
            if s1 != s2:					=> condition is false in k out of k*k times,
												does not contribute to the complexity
                s_new = s1 + s2				=> n   (1)
                if planarity_test.is_planar(g.subgraph(s_new)): => planarity(n) + n^4  (2)
                    partition.remove(s1)		=> k  (3)
                    partition.remove(s2)		=> k-1
                    partition.append(s_new)		=> 1
                    thickness_until_now = recursive_thickness(partition, thickness_until_now) => a_(k-1)
                    partition.remove(s_new)		=> k-1
                    partition.append(s1)		=> 1
                    partition.append(s2)		=> 1
                else:
                    thickness_until_now = min(thickness_until_now, len(partition)) => 1  (3)
	return thickness_until_now

# Footnotes:
(1): the union of s1 and s2 can be at most n elements. These
		needs to be copied, so complexity of n
(2): you need to compare at most n^2 edges of the subgraph
		with n^2 edges of the original graph, so complexity
		of n^4(probably)
(3): see https://wiki.python.org/moin/TimeComplexity for complexity of 'x in s', append,
		remove and len

so:
a_k = k + (k*k-k)*(n + planarity(n) + n^4 + k + (k-1)*2 + a_(k-1) + 3 for k > 1
	the first k is for when the condition in the first if is false

a_1 = constant. If the partition size is 1, both loop bodies are executed once. The condition
in the first if statement results to false, because the partition has only one element. So
the thickness_until_now is directly returned

so a_n is of the same complexity order as the sequence b_n satisfying:
b_1 = 1
b_k = k^2*(planarity(n) + n^4 + k + b_(k-1)) for k > 1

We can prove with induction to k that
c_k = k*(k!)^2(n^4 + planarity(n)) + k^2(k!)^2
is an upper bound for this sequence

Now we can determine the complexity of thickness:

def thickness(g):
    if planarity_test.is_planar(g):	=> planarity(n)
        return 1		=> 1

    partition = [[node] for node in g.nodes]	=> n
    thickness_until_now = len(partition)  		=> 1
    return recursive_thickness(partition, thickness_until_now)  => a_n

this is planarity(n) + a_n + n + 2 = planarity(n) + n*(n!)^2(n^4 + planarity(n)) + n^2(n!)^2 + n + 2
operations, so we get a worst-case complexity of:
n*(n!)^2(n^4 + planarity(n))

"""