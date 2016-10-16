import networkx as nx

'''
This algorithm is stolen from https://www.cs.umd.edu/class/fall2005/cmsc451/biconcomps.pdf, and explained here: http://www.cs.cmu.edu/afs/cs/academic/class/15451-s15/LectureNotes/lecture09.pdf
'''

def OutputComp(stack,u,v):#returns a biconnected component
	result = []
	e = stack.pop()
	result.append(e)
	while e!=(u,v):
		e = stack.pop()
		result.append(e)
	return result
	
def DFSVisit(G,count,stack,visited,parent,d,low,u,result = []):#performs a dfs on the given node
	count+=1
	visited[u] = True
	d[u] = count
	low[u] = count
	for v in G.neighbors(u):
		if not visited[v]:
			stack.append((u,v))
			parent[v] = u
			count = DFSVisit(G,count,stack,visited,parent,d,low,v,result)
			if(low[v] >= d[u]):
				result.append(OutputComp(stack,u,v))
			
			low[u] = min(low[u],low[v])
		else:
			if not parent[u]==v and d[v]<d[u]:
				stack.append((u,v))
				low[u] = min(low[u],d[v])
	
	
	return count

def convert_to_graphs(edges_list):#converts a list of collections of edges into a list of graphs
	result_graphs = []
	for x in edges_list:
		G = nx.Graph()
		G.add_edges_from(x)
		result_graphs.append(G)
	return result_graphs
	

def BiconnectedComponents(G):
	count = 0
	stack=[]
	visited = [False]*(max(G.nodes())+1)
	parent = [0]*(max(G.nodes())+1)
	d = [0]*(max(G.nodes())+1)
	low = [0]*(max(G.nodes())+1)
	result = []

	for u in G.nodes():
		if not visited [u]:
			count = DFSVisit(G,count,stack,visited,parent,d,low,u,result)
	return convert_to_graphs(result)#the output of the DFS is a list of edges, and we need to convert those to graphs