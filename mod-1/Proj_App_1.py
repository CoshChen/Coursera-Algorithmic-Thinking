"""
Author: Ko-Shin Chen
Algorithmic Thinking (Part 1)
Project 1: Degree Distributions for Graphs
Application 1: Analysis of Citation Graphs
"""

#Example Graphs
EX_GRAPH0 = {0: set([1,2]), 1: set([]), 2: set([])}

EX_GRAPH1 = {0: set([1,4,5]), 1:set([2,6]), \
             2:set([3]), 3:set([0]), 4: set([1]), \
             5: set([2]), 6: set([])}

EX_GRAPH2 = {0: set([1,4,5]), 1:set([2,6]), \
             2:set([3,7]), 3:set([7]), 4: set([1]), \
             5: set([2]), 6: set([]),\
             7: set([3]), 8: set([1,2]),\
             9: set([0,3,4,5,6,7])}

def make_complete_graph(num_nodes):
    """
    This function generate the complete directed graph with
    the given number of vertices.
    """
    
    comp_graph = {}
    all_vertex = set(range(num_nodes))
    
    for dumy_vertex in all_vertex:
        copy_vertex = all_vertex.copy()
        copy_vertex.remove(dumy_vertex)
        comp_graph[dumy_vertex] = set(copy_vertex)
        
    return comp_graph


def compute_in_degrees(digraph):
    """
    This function returns in-degrees for each vertex for 
    the given directed graph
    """
    
    in_degree = {}
    all_vertex = digraph.keys()
    
    for dummy_vertex in all_vertex:
        in_degree[dummy_vertex] = 0
        
    for dummy_vertex in all_vertex:
        for dummy_element in digraph[dummy_vertex]:
            in_degree[dummy_element] += 1
            
    return in_degree


def in_degree_distribution(digraph):
    """
    This function returns in-degree distribution for 
    the given directed graph
    """
    
    in_degree = compute_in_degrees(digraph)
    all_vertex = in_degree.keys()
    degree_dist = {}
    
    for dummy_vertex in all_vertex:
        degree_value = in_degree[dummy_vertex]
        
        if degree_dist.has_key(degree_value):
            degree_dist[degree_value] += 1
        else:
            degree_dist[degree_value] = 1
            
    return degree_dist
    
    
##############################################################
# For Application

import alg_load_graph
import alg_dpa_trial

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
citation_graph = alg_load_graph.load_graph(CITATION_URL)

cite_dist = in_degree_distribution(citation_graph)

"""
Question 3
"""
all_vertex = citation_graph.keys()
out_degree = 0
for dummy_vertex in citation_graph.keys():
    out_degree += len(citation_graph[dummy_vertex])

ave_out = out_degree/27770.0    
print ave_out


"""
Question 4
"""
m = 13
n = 27770

dpa_graph = make_complete_graph(m)
trial = alg_dpa_trial.DPATrial(m)

for index in range(m,n):
    nbd = trial.run_trial(m)
    dpa_graph[index] = nbd
    
dpa_dist = in_degree_distribution(dpa_graph)
