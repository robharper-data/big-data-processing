#!/usr/bin/env python3
import sys

""" Implemented as in-mapper combiner for local aggregation of trips per taxi company. """
mylist = []
for line in sys.stdin:
    line = line.strip()
    records = line.split('\t')
    company = records[0].strip() # Extract company name

    flag= False #flag to tell if a company is in the list
    for i in range(len(mylist)):
        if mylist[i][0] == company: # Company already in list
            mylist[i][1] += 1 # Increment count for that company
            flag = True #We found the company set to true
            break
    if not flag:
        # Add new entry: [company, count], because flag indicated the entry didn't exist
        mylist.append([company, 1])

for entry in mylist: # Emit key-value pairs
    company, count = entry
    print('%s\t%s' % (company, count))
    
    
   
        
    
    