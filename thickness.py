import networkx as nx
import planarity_test
import math
import copy


def thickness(g):
    return thickness_idontknowname(g)

"""
Dit algoritme probeert de thickness te achterhalen met gebruik van een soort bisection method
(https://en.wikipedia.org/wiki/Bisection_method).

e           thickness is smaller than this
e-1         thickness is smaller than this
e-2 max,    thickness could be smaller than this, a partition of this size with all subgraphs planar has been found
.    |
.    V
.
.    ^
.    |
3   min     thickness is larger than this
2           thickness is larger than this
1           thickness is larger than this

Set min to 1
Set max to round_up(nr-of-edges/8) (K_5 and K_3_3 have 10 resp 9 edges, so if you have 8 edges, it is certainly planar)

while min + 1 != max
    avg = average(min,max)
    for all partitions of edges of size avg:
        if all subgraphs in the partition are planar
            set max to avg
            break from the for loop
    if all partitions of size cur appear to have a subgraph which is non-planar
        set min to avg
return min
"""


def thickness_idontknowname(g):
    minn = 1
    maxx = g.number_of_edges()
    # maxx = math.ceil(g.number_of_edges()/8)  # todo: uncomment this optimization if it works
    while minn + 1 != maxx:
        avg = math.floor((minn + maxx)/2)
        if thickness_could_be(avg, g):
            maxx = avg
        else:
            minn = avg
    return maxx


def thickness_could_be(part_size, g):
    for partition in partition_gen(g.nodes().copy(), part_size):
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


class Partitions:
    def f(self):
        pass


# just to practice: determine all k-partitions of a set s
def all_k_partitions_of(s, k):
    assert len(s) >= k > 0
    if k == 1:  # if we need only 1 part
        return [[copy.deepcopy(s)]]
    elif len(s) == k:  # as much parts as elements in the set
        return [[[elem] for elem in s]]
    else:
        elem = s.pop()  # there are two possibilities for elem to appear in the partition: as sole part or
        # as one of the other k parts:
        result = []
        for partition in all_k_partitions_of(s, k - 1):
            partition.append([elem])
            result.append(partition)
        for partition in all_k_partitions_of(s, k):
            for s2 in partition:
                s2.append(elem)
                result.append(copy.deepcopy(partition))
                s2.remove(elem)
        s.append(elem)
        return result


# Werkt! :D
def partition_gen(s, k):  # s is a set, k is the number of sets(I call them parts) in the yielded partition
    assert len(s) >= k > 0
    if k == 1:  # if we need only 1 part
        yield [copy.deepcopy(s)]
    elif len(s) == k:  # as much parts as elements in the set
        yield [[elem] for elem in s]
    else:
        elem = s.pop()  # there are two possibilities for elem to appear in the partition: as sole part or
        # as one of the other k parts(see https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind#Recurrence_relation):
        for partition in partition_gen(s, k-1):
            partition.append([elem])
            yield partition
        for partition in partition_gen(s, k):
            for s2 in partition:
                s2.append(elem)
                yield copy.deepcopy(partition)
                s2.remove(elem)
        s.append(elem)


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
    # print(len(partition), end="")
    for s1 in partition:  # s stands for subset, it is a subset of the graph
        for s2 in partition:
            if s1 != s2:
                s_new = s1 + s2
                planar = None
                hashh = 0
                for index,edge in g.edges():
                    if edge in s_new:
                        hashh += (1 << index)

                if hashh in d:
                    planar = d[hashh]
                else:
                    g2 = nx.Graph()
                    g2.add_edges_from(s_new)
                    planar = planarity_test.is_planar(g2)
                    d[hashh] = planar

                if planar:
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


d = dict()


def stirling(n, k):
    if n == 0 and k == 0:
        return 1
    elif n == 0 or k == 0:
        return 0
    else:
        return k * stirling(n - 1, k) + stirling(n - 1, k - 1)

if __name__ == "__main__":
    for index, p in enumerate(partition_gen(['a','b','c','d','e'], 3)):
        print(p)
    # gr = nx.complete_graph(5)
    # print(thickness_merge(gr))
    # ll = all_k_partitions_of(['a','b','c','d','e'], 3)
    # for pp in ll:
    #     print(pp)
    # print(len(ll))
    # print(stirling(5, 3))


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