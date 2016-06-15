'''
Author: Ko-Shin Chen
Algorithmic Thinking (Part 1)
Application 2: Analysis of a Computer Network
'''

import random
import timeit
import UPATrial
import providedModule2 as provided
import Project_2 as Proj2


def make_complete_graph(n):
    '''
    This function generates a complete graph with
    n vertices.
    '''
    
    graph = {}
    all_vertex = set(range(n))
    
    for v in all_vertex:
        copy_vertex = all_vertex.copy()
        copy_vertex.remove(v)
        graph[v] = set(copy_vertex)
        
    return graph



def er_graph(n,p):
    '''
    This function grnerates ER graph with n vertices. 
    '''
    graph = {}

    for i in range(n):
        graph[i] = set([])

    for i in range(n-1):
        for j in range(i+1, n):
            a = random.random()
            if a < p:
                graph[i].add(j)
                graph[j].add(i)

    return graph



def upa_graph(n,m):
    '''
    This function generates UPA graph with n vertices
    starting from a complete graph with m vertices.
    '''
    graph = make_complete_graph(m)
    trial = UPATrial.UPATrial(m)

    for i in range(m,n):
        nbds = trial.run_trial(m)
        graph[i] = nbds

        for j in nbds:
            graph[j].add(i)
            
    return graph



#########################################################

'''
Question 1
'''

network = provided.load_graph(provided.NETWORK_URL)

#Calculate average degree M for netwoek.

all_vertices = network.keys()
degree = 0
for v in all_vertices:
    degree += len(network[v])

print degree/(1239.0 * 2)


N = 1239 #Number of vertices in network
P = 0.00397 #Used to generate ER graph so that the number of edges is near 3047
M = 2 #Average degree of network

def random_order(ugraph):
    order = ugraph.keys()
    random.shuffle(order)

    return order

 
graph = network
order = random_order(graph)
print Proj2.compute_resilience(graph, order)


#########################################################

'''
Question 3
'''

def fast_targeted_order(ugraph):
    graphCopy = provided.copy_graph(ugraph)
    n = len(graphCopy.keys())
    DegreeSet = {}
    
    for k in range(n):
        DegreeSet[k] = set([])

    for i in range(n):
        d = len(graphCopy[i])
        DegreeSet[d].add(i)

    L = []

    for k in range(n):
        while len(DegreeSet[n-1-k]) != 0:
            u = DegreeSet[n-1-k].pop()
            nbd = graphCopy[u]
            
            for v in nbd:
                d = len(graphCopy[v])
                DegreeSet[d].remove(v)
                DegreeSet[d-1].add(v)
                graphCopy[v].remove(u)

            L.append(u)
            graphCopy.pop(u, None)

    return L
 

#Find Running Time

Time = []

for n in range(10, 1000, 10):
    graph = upa_graph(n,5)

    start = timeit.default_timer()
    provided.targeted_order(graph)
    stop = timeit.default_timer()

    Time.append(stop - start)

print Time


#########################################################

'''
Question 4
'''

graph = upa_graph(N,M)
order = provided.targeted_order(graph)
print Proj2.compute_resilience(graph, order)