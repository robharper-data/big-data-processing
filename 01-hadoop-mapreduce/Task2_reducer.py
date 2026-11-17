#!/usr/bin/env python3
"""reducer.py"""


import sys
from math import sqrt

def PAM_Update(cluster_list):

    best_dist = float('inf')
    new_medoid = None
    #2 loops, 2 compare each point in the list to the other points
    for i, point in enumerate(cluster_list):
        total_dist = 0.0 #Initialise total distance variable
        for j, other_point in enumerate(cluster_list):
            if i != j: #Make sure we don't calculate distance to itself
                dist = sqrt(pow(point[0] - other_point[0], 2) + pow(point[1] - other_point[1], 2)) #Calculate euclidean distance
                total_dist += dist #Sum the total distance
                if total_dist >= best_dist: #Early stop if the total distance becomes larger than the best distance
                    break
        """
        The best value is the minimum average distance, which is the same as the minimum total distance, 
        because the average would be calculated with the same denominator of n-1, wiith n being the length of the list
        """            
        if total_dist < best_dist: 
            best_dist = total_dist #Update the best distance
            new_medoid = point #Point with the best distance should become the new medoid
    return new_medoid 

def calculateNewMedoids():
    current_medoid = None
    current_o = ()

    for line in sys.stdin: #Stream input

        # parse the input of mapper
        medoid_index, x, y = line.split('\t')

        # convert x and y (currently a string) to float
        try:
            x = float(x)
            y = float(y)
        except ValueError:
            continue

        
        if current_medoid == medoid_index: #If the current medoid is the same as the one just parsed, add the datapoint to the cluster list
            cluster_list.append((x, y))
        else:
            if current_medoid: #If the current_medoid exists, the cluster list should be complete.
                new_medoid = PAM_Update(cluster_list) #calculate the new medoid from the full list of points associated with a cluster
                print('%s\t%s' % (new_medoid[0], new_medoid[1])) #Print the new medoid


            cluster_list = [] #initialise the list for a cluster
            current_medoid = medoid_index #Update the current cluster index
            current_o = (x, y) #append the first data point to the cluster list
            cluster_list.append(current_o)
    
        # print last cluster's medoids
    if current_medoid is not None and cluster_list:
        new_medoid = PAM_Update(cluster_list)
        print('%s\t%s' % (new_medoid[0], new_medoid[1]))

if __name__ == "__main__":
    calculateNewMedoids()