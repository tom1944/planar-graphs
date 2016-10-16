import biconnected_components as bicon
import networkx as nx
import itertools
from operator import itemgetter

def merge_nodes(G,u,v):#merges two nodes
	for x in G.neighbors(u):
		G.remove_edge(*(u,x))
		if x==v:
			continue
		if not G.has_edge(*(v,x)) and not G.has_edge(*(x,v)):
			G.add_edge(*(v,x))
	G.remove_node(u)

def is_K5_possible(G):#check whether we have enough edges and vertices left to construct K5
	K5 = nx.complete_graph(5)
	return len(G.nodes())>=len(K5.nodes()) and len(G.edges())>=len(K5.edges())
def is_K33_possible(G):#check whether we have enough edges and vertices left to construct K33
	K33 = nx.complete_multipartite_graph(3,3)
	return len(G.nodes())>=len(K33.nodes()) and len(G.edges())>=len(K33.edges())
	
'''
this function contains an optimalization based on these theorems for planar graphs: e <= 3v-6, and e <= 2v-3 if the graph doesnt contain any cycles of length three
Due to the fact that a nonplanar graph always contains either K5 or K33, and a graph for which e <= 3v - 6 doesn't hold is nonplanar, we should start looking for a minor 
containg a forbidden minor by first checking the minors in which the the difference between e and 3v-6 is as small as possible. This is done by first merging the nodes 
which have the largest set of unshared neighbors. By doing this, we are apt to find a forbidden minor faster than without this optimalization, but will still need as much
time as before to proof that a graph is planar.
'''
def get_possible_edge_contractions(G):#returns a list of possible contractions in a given graph
	possible = []
	for x in G.nodes():
		for y in G.neighbors(x):
			x_neig = G.neighbors(x)
			y_neig = G.neighbors(y)
			intersect = len(x_neig)-len(list(set(x_neig).intersection(y_neig)))
			possible.append(((x,y),intersect))
	return sorted(possible,key=itemgetter(1))
	

def contains_forbidden_subgraph(G):#checks whether a graph has a forbidden subgraph
	K5 = nx.complete_graph(5)
	K33 = nx.complete_multipartite_graph(3,3)
	
	GM = nx.algorithms.isomorphism.GraphMatcher(G,K5)
	if nx.is_isomorphic(G,K5) or GM.subgraph_is_isomorphic():
		return True
	GM = nx.algorithms.isomorphism.GraphMatcher(G,K33)
	if nx.is_isomorphic(G,K33) or GM.subgraph_is_isomorphic():
		return True
		
	return False
	

'''
This function recursively checks whether or not a given graph is planar. It returns True if the graph has either too few nodes or vertices to have either K5 or K33 as minors
and returns false if it does. Even though a minor is created by deleting edges or vertices and contracting edges, we only need to focus on contracting edges because we can
check the subgraphs, which are created by deleting edges and vertices with the networkx library.
'''
def is_planar_simple(G, merge = [],already_checked = []):#this is the recursive functions which checks whether a given graph is planar
	
	for x in already_checked:#check whether we might have already checked an isomorph of the current graph
		if nx.is_isomorphic(G,x):
			return True
			
	if not is_K5_possible(G) and not is_K33_possible(G):#if we have too few nodes or vertices to make either K5 or K33, the current graph is planar
		return True
		
	if contains_forbidden_subgraph(G):#if we have a forbidden subgraph, the graph is not planar
		return False
		
	already_checked.append(G)#make sure we only check this graph once
	
	possible_contractions = get_possible_edge_contractions(G)#get a list of possible contractions, ordered so that the contractions which are most likely to give a graph with a forbidden subgraph are checked first
	for x in possible_contractions:
		H = G.copy()
		to_merge,val = x
		
		merge.append(to_merge)
		merge_nodes(H,*to_merge)
		
		if not is_planar_simple(H,merge,already_checked):
			return False
			
		merge.pop()
	return True
'''
This function first splits the graph into its biconnected components, and then checks whether each biconnected component is planar
'''
def is_planar(G,merge = []):#main function, if you wish to see which merges were done to get a minor containg a forbidden subgraph, pass a list to 'merge'
	biconnected_components = bicon.BiconnectedComponents(G)
	for H in biconnected_components:
		if not is_planar_simple(H,merge):
			return False
	return True