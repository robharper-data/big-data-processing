#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    records = line.split('\t') #This reducer simply recieves the sorted companies and emits them, with some exception handling for safety.
    company = records[0].strip()
    try:
        num_of_trips = int(records[2].strip())
    except (IndexError, ValueError):
        continue 
    print('%s\t%s' % (company, num_of_trips))