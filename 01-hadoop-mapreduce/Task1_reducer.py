#!/usr/bin/env python3
import sys

# Initialize variables to track current taxi and trip
current_taxi = None
current_trip = None
current_max = 0
current_min = float('inf')
current_total = 0
current_count = 0

# Read input from standard input (output from mapper)
for line in sys.stdin:
    line = line.strip()
    
    # Parse the input from mapper
    try:
        taxi, trip, max_fare, min_fare, total_fare, count = line.split('\t')
        max_fare = float(max_fare)
        min_fare = float(min_fare)
        total_fare = float(total_fare)
        count = int(count)
    except ValueError:
        continue

    # If the current taxi and trip match the previous, update stats        
    if current_taxi == taxi and current_trip == trip:
        current_count += count
        current_total += total_fare
        current_max = max(current_max, max_fare)
        current_min = min(current_min, min_fare)    
    # If they don't match, output the details for the current taxi and trip
    else:
        if current_taxi and current_trip:
            avg = current_total/current_count
            print('%s\t%s\t%s\t%s\t%s\t%s' % (current_taxi,current_trip,current_count, round(current_max,2),round(current_min,2),round(avg,2)))
        
    # Update current taxi and trip details
        current_taxi = taxi
        current_trip = trip
        current_count = count
        current_total = total_fare
        current_max = max_fare
        current_min = min_fare

# Output the last taxi and trip details
if current_taxi is not None and current_trip is not None:
    avg = current_total/current_count
    print('%s\t%s\t%s\t%s\t%s\t%s' % (current_taxi,current_trip,current_count, round(current_max,2),round(current_min,2),round(avg,2)))