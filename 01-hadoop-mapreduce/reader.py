#!/usr/bin/env python3
from Task2_mapper import getMedoids
 
if __name__ == "__main__":
    medoids = getMedoids('medoids.txt')
    medoids1 = getMedoids('medoids1.txt')
   
    if medoids == medoids1:
        print(1)
    else:
        print(0)
