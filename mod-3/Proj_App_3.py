'''
Author: Ko-Shin Chen
Algorithmic Thinking (Part 2)
Project 3: Closest Pairs and Clustering Algorithms
Application 3: Comparison of Clustering Algorithms
'''

import math

import random
import timeit
import matplotlib.pyplot as plt

import alg_cluster

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a 
    list.

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices 
           for two clusters.
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
            cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the 
            clusters cluster_list[idx1] and cluster_list[idx2] have minimum 
            distance dist.       
    """
    
    if len(cluster_list) < 2: 
        return (float('+inf'), -1, -1)
    
    dist_min = float('inf')
    idx1 = -1
    idx2 = -1
    
    for idx_i in range(0, len(cluster_list)-1):
        for idx_j in range(idx_i + 1, len(cluster_list)):
            dist = pair_distance(cluster_list, idx_i, idx_j)[0]
            if dist_min > dist:
                dist_min = dist
                idx1 = idx_i
                idx2 = idx_j
    
    return (dist_min, idx1, idx2)



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal 
           positions of their centers are in ascending order.
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the 
            clusters cluster_list[idx1] and cluster_list[idx2] have minimum 
            distance dist.       
    """
    
    size = len(cluster_list)
    
    if size < 4: 
        return slow_closest_pair(cluster_list)
    
    half = int(math.ceil(size/2.0))
    left_list = cluster_list[:half]
    right_list = cluster_list[half:]
    
    left_result = fast_closest_pair(left_list)
    right_result = fast_closest_pair(right_list)
    
    if left_result[0] < right_result[0]:
        result = left_result
    else:
        result = (right_result[0], right_result[1]+half, right_result[2]+half)
    
    #Start to calculate the distance between left group and right group
    horiz_center = 0.5*(cluster_list[half - 1].horiz_center() + cluster_list[half].horiz_center())
    center_result = closest_pair_strip(cluster_list, horiz_center, result[0])
    
    if center_result[0] < result[0]:
        return center_result
    else:
        return result



def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
           horiz_center is the horizontal position of the strip's vertical 
           center line half_width is the half the width of the strip 
           (i.e; the maximum horizontal distance that a cluster can lie from 
           the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the 
            clusters cluster_list[idx1] and cluster_list[idx2] lie in the 
            strip and have minimum distance dist.       
    """
    
    center_index = []
    
    for idx in range(0, len(cluster_list)):
        if math.fabs(horiz_center - cluster_list[idx].horiz_center()) <= half_width:
            center_index.append(idx)
    
    dist_min = float('inf')
    idx1 = -1
    idx2 = -1
    
    size = len(center_index)
    if size < 2: 
        return (dist_min, idx1, idx2)
        
    center_index.sort(key = lambda idx: cluster_list[idx].vert_center())
    
    for idx_i in range(0, size - 1):
        for idx_j in range(idx_i + 1, min(idx_i + 4, size)):
            dist = pair_distance(cluster_list, center_index[idx_i], center_index[idx_j])[0]
            
            if dist < dist_min:
                dist_min = dist
                idx1 = min(center_index[idx_i], center_index[idx_j])
                idx2 = max(center_index[idx_i], center_index[idx_j])
                   

    return (dist_min, idx1, idx2)
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    size = len(cluster_list)
    
    if size == 0:
        return []
            
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        pair = fast_closest_pair(cluster_list)
        point1 = cluster_list[pair[1]]
        cluster_list[pair[2]].merge_clusters(point1)
        cluster_list.remove(point1)
        
    return cluster_list


######################################################################
# Code for k-means clustering
def find_index(cluster, centers):
    """
    Halper function used in kmeans_clustering.
    Find the index of centers that is nearest to the cluster 
    """
    
    dist_min = 'inf'
    index = -1
    
    for idx in range(0, len(centers)):
        dist = cluster.distance(centers[idx])
        
        if dist < dist_min:
            dist_min = dist
            index = idx
    
    return index
        

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    size = len(cluster_list)
    copy_list = [cluster.copy() for cluster in cluster_list]
    copy_list.sort(key = lambda cluster: -1*cluster.total_population())
    # position initial clusters at the location of clusters with largest populations
    centers = copy_list[:num_clusters]
    
    for _ in range(0, num_iterations):
        cluster_set = [alg_cluster.Cluster(set(), 0, 0, 0, 0) for _ in range(num_clusters)]
        
        for idx_j in range(0,size):
            index = find_index(cluster_list[idx_j], centers)
            cluster_set[index].merge_clusters(cluster_list[idx_j])
      
        for idx_k in range(0, num_clusters):
            centers[idx_k] = cluster_set[idx_k].copy()
                   
    return centers
    

######################################################################
# Application

def gen_random_clusters(num_clusters):
    cluster_list = []
    while len(cluster_list) != num_clusters:
        x_pos = random.uniform(-1, 1)
        y_pos = random.uniform(-1, 1)
        cluster_list.append(alg_cluster.Cluster(set(), x_pos, y_pos, 0, 0))
        
    return cluster_list
    
time_slow = []
time_fast = []

for size in range(2,201):
    cluster_list = gen_random_clusters(size)
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    
    start = timeit.default_timer()
    slow_closest_pair(cluster_list)
    stop = timeit.default_timer()
    
    time_slow.append(stop-start)
    
    start = timeit.default_timer()
    fast_closest_pair(cluster_list)
    stop = timeit.default_timer()
    
    time_fast.append(stop-start)

x_val = range(2,201)
plt.plot(x_val, time_slow, '-b', label='slow_closest_pair')
plt.plot(x_val, time_fast, '-r', label='fast_closest_pair')
plt.title('Running Times in Desktop Python')
plt.xlabel('Size of Cluster List')
plt.ylabel('Time (sec)')
plt.legend(loc='upper left')
plt.show()


def compute_distortion(cluster_list, cluster_table):
    distortion = 0
    
    for cluster in cluster_list:
        distortion += cluster.cluster_error(cluster_table)
        
    return distortion