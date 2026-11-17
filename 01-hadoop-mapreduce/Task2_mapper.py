#!/usr/bin/env python3
import sys
from math import sqrt

# get initial medoids from a txt file and add them in an array
def getMedoids(filepath):

    """ 
    ==================== IMPORTANT INFO ====================
    This version of the program assumes that all medoids, 
    including those from initilization.txt, are one of the 
    dropoff coordinates in Trips.txt. So there's no special need 
    to deal with the medoids as an extra point. The medoid will 
    naturally come up while streaming the data, and have a 
    distance measure of 0 to itself.
    """
    medoids = [] # Empty list to store medoids

    with open(filepath) as fp:
        for line in fp:
            line = line.strip()
            try:
                cord = line.split('\t') # Split by tab
                medoids.append([float(cord[0]), float(cord[1])]) # Append as float coordinates
            except (ValueError, IndexError):
                continue
    
    return medoids # Return list of medoids

# Create clusters based on initial medoids
def createClusters(medoids):
    
    for line in sys.stdin:
        line = line.strip()
        values = line.split(',')

        try:
            dropoff_x = float(values[6])  # Get dropoff x coordinate
            dropoff_y = float(values[7])  # Get dropoff y coordinate
        except ValueError:
            continue
        
        min_dist = float('inf') # Initialize minimum distance to inf
        index = -1 # Initialize index of closest medoid


        # Find closest medoid to the point
        for i, medoid in enumerate(medoids):

            # Calculate Euclidean distance
            cur_dist = sqrt(pow(dropoff_x - medoid[0], 2) + pow(dropoff_y - medoid[1], 2)) 
            
            # Update minimum distance and index if current distance is smaller than min_dist
            if cur_dist < min_dist:  
                min_dist = cur_dist 
                index = i  


        if index != -1: #Print datapoint if associated with valid cluster index
            var = "%s\t%s\t%s" % (index, dropoff_x, dropoff_y)
            print(var)

if __name__ == "__main__":
    medoids = getMedoids('medoids.txt')
    createClusters(medoids)