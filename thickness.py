import networkx as nx
import planarity_test
import math
import copy


def thickness(g):
    return thickness_bisection(g)

""""
Thickness merge algoritme:
Hieronder is het eerste algoritme dat wij hebben bedacht voor het bepalen van de thickness. De intuitie van dit
algoritme is om een volledige partitie van de edges te maken en ze voorzichtig samen te voegen.

Een schets van het thickness merge algoritme:
Maak een volledige partitie P van de edges.
voor alle paren deelverzamelingen in P:
    merge ze
    als de subgraaf gegenereerd door de nieuwe subset van edges planair is
        ga de recursie in
    anders
        unmerge ze
        thickness_until_now = min(thickness_until_now, size_of(P) )

Alle paren subsets worden met elkaar gemerged. Dit gebeurt ook nog recursief. Hierdoor krijgen we een gigantische
complexiteit. Uit een paar grove inschattingen die we op klad hebben gemaakt, schatten we in dat de complexiteit in
de orde van e*(e!)^2(e^4 + planarity(n)) ligt, waarbij e het aantal edges is, n het aantal nodes en planarity(n) de
complexiteit van het planarity_test algoritme bij n nodes is. Zodra de thickness van een graaf groter dan 1 is, is het
met de implementatie van dit algoritme al praktisch onmogelijk om de thickness te bepalen. Het is daardoor ook
onmogelijk om deze implementatie te testen.
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
    # print(len(partition), end="")
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

"""
Thickness bisection algoritme:
Dit algoritme probeert de thickness te achterhalen met gebruik van een methode die lijkt op de bisection method
(https://en.wikipedia.org/wiki/Bisection_method).

e           thickness is smaller than this
e-1         thickness is smaller than this
e-2 max,    thickness could be smaller than this, a partition of this size with all subgraphs planar has been found
.    |
.    V
.        <- avg
.    ^
.    |
3   min     thickness is larger than this
2           thickness is larger than this
1           thickness is larger than this

Een schets van het thickness bisection algoritme:
Set min to 0
Set max to round_up(nr-of-edges/8) (K_5 and K_3_3 have 10 resp 9 edges, so if you have 8 or less edges per subgraph,
                                    it is certainly planar)
while min + 1 != max
    avg = average(min,max)
    for all partitions of edges of size avg:
        if all subgraphs in the partition are planar
            set max to avg
            break from the for loop
    if all partitions of size cur appear to have a subgraph which is non-planar
        set min to avg
return max
"""


def thickness_bisection(g):
    if planarity_test.is_planar(g):  # shortcut if graph is planar
        return 1

    minn = 0
    maxx = math.ceil(g.number_of_edges()/8)
    while minn + 1 != maxx:
        avg = math.floor((minn + maxx)/2)
        if thickness_could_be(avg, g):
            maxx = avg
        else:
            minn = avg
    return maxx


def thickness_could_be(part_size, g):
    for partition in partition_gen(g.edges().copy(), part_size):
        all_planar = True
        for s in partition:
            g2 = nx.Graph()
            g2.add_edges_from(s)  # todo: possibly implement dynamic programming
            if not planarity_test.is_planar(g2):
                all_planar = False
                break
        if all_planar:
            return True
    return False

"""
Om alle k-partities van een verzameling te genereren, maken we gebruik van een pythongenerator. Het genereren van de
partities gaat volgens dezelfde strategie als het bepalen van het stirlinggetal van de tweede soort, zie
https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind#Recurrence_relation
"""


def partition_gen(s, k):  # s is a set, k is the number of sets(I call them parts) in the yielded partition
    assert len(s) >= k > 0
    if k == 1:  # if we need only 1 part
        yield [copy.deepcopy(s)]
    elif len(s) == k:  # if there are as much parts as elements in the set
        yield [[elem] for elem in s]
    else:
        elem = s.pop()  # there are two possibilities for elem to appear in the partition: as sole part or
        # as one of the other k parts:
        for partition in partition_gen(s, k-1):
            partition.append([elem])
            yield partition
        for partition in partition_gen(s, k):
            for s2 in partition:
                s2.append(elem)
                yield copy.deepcopy(partition)
                s2.remove(elem)
        s.append(elem)


def stirling(n, k):  # usefull to test the partition generator
    if n == 0 and k == 0:
        return 1
    elif n == 0 or k == 0:
        return 0
    else:
        return k * stirling(n - 1, k) + stirling(n - 1, k - 1)

if __name__ == "__main__":
    gr = nx.complete_bipartite_graph(2,3)
    gr2 = nx.complete_graph(9)
    print("hi")
    print(thickness_bisection(gr))
K4 = nx.complete_graph(4)
K5 = nx.complete_graph(5)
K8 = nx.complete_graph(8)
K_3_3 = nx.complete_bipartite_graph(3,3)
W7 = nx.wheel_graph(7)


""" OUTDATED hier had ik een verkeerde interpretatie van de thickness
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