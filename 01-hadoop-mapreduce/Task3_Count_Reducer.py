#!/usr/bin/env python3
import sys

current_count = 0 # Initialize count
current_company = None # Initialize current company

for line in sys.stdin:
    line = line.strip()
    records = line.split('\t') # Extract company and count from input (mapper output)
    company = records[0].strip()
    try:
        count = int(records[1].strip())
    except (IndexError, ValueError): # Handle missing or invalid count
        continue
    if current_company == company: # If same company, aggregate count
        current_count += count
    else:
        if current_company is not None:
            print('%s\t%s' % (current_company, current_count)) # Emit company and its count
        current_company = company #Set values for first instance
        current_count = count

if current_company is not None:
    print('%s\t%s' % (current_company, current_count)) # Emit last company and its count