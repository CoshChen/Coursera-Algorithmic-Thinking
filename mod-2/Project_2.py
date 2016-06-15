'''
Author: Ko-Shin Chen
Algorithmic Thinking (Part 1)
Project 2: Connected Components and Graph Resilience
'''

import poc_queue

def bfs_visited(ugraph, start_node):
    '''
    The function returns a set of nodes which 
    can be traveled from start_node.
    '''
    ver_q = poc_queue.Queue()
    visited = set([start_node])
    ver_q.enqueue(start_node)
    
    while(ver_q.__len__() > 0):
        ver_j = ver_q.dequeue()
        if len(ugraph[ver_j]) > 0:
            for nbd_j in ugraph[ver_j]:
                if nbd_j not in visited:
                    visited.add(nbd_j)
                    ver_q.enqueue(nbd_j)
                
    return visited



def cc_visited(ugraph):
    '''
    The function returns a list of components in ugraph.
    '''
    remaining = set(ugraph.keys())
    comp = []
    
    while(len(remaining) > 0):
        ver_i = remaining.pop()
        comp_i = bfs_visited(ugraph, ver_i)
        comp.append(comp_i)
        remaining.difference_update(comp_i)
        
    return comp



def largest_cc_size(ugraph):
    '''
    The function returns the maximum size of 
    the component in ugraph.
    '''
    comp = cc_visited(ugraph)
    max_num = 0
    
    for comp_i in comp:
        if len(comp_i) > max_num:
            max_num = len(comp_i)
            
    return max_num



def compute_resilience(ugraph, attack_order):
    '''
    The function returns a list whose k-th element is 
    the size of the largest component after removing
    the first k nodes in attack_order
    '''
    comp_size = []
    comp_size.append(largest_cc_size(ugraph))
    
    for node_i in attack_order:
        for nbd_i in ugraph[node_i]:
            ugraph[nbd_i].remove(node_i)
            
        ugraph.pop(node_i, None)
        
        comp_size.append(largest_cc_size(ugraph))
        
    return comp_size