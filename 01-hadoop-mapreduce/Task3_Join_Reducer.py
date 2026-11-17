#!/usr/bin/env python3
import sys

current_taxi = None
current_company = None

""" This reducer assumes the first line it receives is a taxi record and subsequent lines are trip records for that taxi."""


for line in sys.stdin:
    line = line.strip()
    records = line.split('\t')

    if records[1].strip() == '0': #This is a taxi record
        try:
            current_taxi = records[0].strip() # Skip lines that don't parse properly
            current_company = records[2].strip()
        except (IndexError, ValueError):
            continue  
    elif records[1] == '1': #This is a trip record
        if records[0].strip() != current_taxi:
            continue #The taxi should be the same as the previous, if not skip as theres a problem
        print('%s\t%s' % (current_company, '1')) #Emit company and count of 1 for that trip