'''
Author: Ko-Shin Chen
Algorithmic Thinking (Part 1)
Project 1: Degree Distributions for Graphs
'''

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
    '''
    This function generate the complete directed graph with
    the given number of vertices.
    '''
    
    comp_graph = {}
    all_vertex = set(range(num_nodes))
    
    for dumy_vertex in all_vertex:
        copy_vertex = all_vertex.copy()
        copy_vertex.remove(dumy_vertex)
        comp_graph[dumy_vertex] = set(copy_vertex)
        
    return comp_graph


def compute_in_degrees(digraph):
    '''
    This function returns in-degrees for each vertex for 
    the given directed graph
    '''
    
    in_degree = {}
    all_vertex = digraph.keys()
    
    for dummy_vertex in all_vertex:
        in_degree[dummy_vertex] = 0
        
    for dummy_vertex in all_vertex:
        for dummy_element in digraph[dummy_vertex]:
            in_degree[dummy_element] += 1
            
    return in_degree


def in_degree_distribution(digraph):
    '''
    This function returns in-degree distribution for 
    the given directed graph
    '''
    
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