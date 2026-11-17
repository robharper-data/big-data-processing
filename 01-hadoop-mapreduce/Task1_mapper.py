#!/usr/bin/env python3
import sys

mylist = [] #List for the combiner

for line in sys.stdin: #Stream the data line-by-line
    line = line.strip()
    records = line.split(',') #Get the comma seperated values, should be a list
    try:
        taxi_id = records[1].strip() #Make sure data types can be parsed
        fare = float(records[2])
        distance = float(records[3])
    except (IndexError, ValueError):
        continue  # Skip lines that don't parse properly

    # Determine trip type
    if distance < 100:    
        trip_type = 'short'
    elif distance < 200:
        trip_type = 'medium'
    else:
        trip_type = 'long'

    key = f"{taxi_id.strip()}_{trip_type.strip()}" #Combine taxi id and trip type into a single string to simplify processing

    flag = False #Flag for checking if the key exists in the combiner list
    for i in range(len(mylist)): #Iterate through combiner list until the key is found, and if found, update the entry.
        if mylist[i][0] == key:
            # Update existing entry
            mylist[i][1] = max(mylist[i][1], fare)      # max fare
            mylist[i][2] = min(mylist[i][2], fare)      # min fare
            mylist[i][3] += fare                        # total fare
            mylist[i][4] += 1                           # count
            flag = True
            break

    if not flag: #If the taxi_id and trip_type key didn't exist in the list yet.
        # Add new entry: [key, max_fare, min_fare, total_fare, count]
        mylist.append([key, fare, fare, fare, 1]) 

# Emit final results
for entry in mylist:
    key, max_fare, min_fare, total_fare, count = entry
    taxi_id, trip_type = key.split('_') #Re-split the taxi and trip
    line = f"{taxi_id}\t{trip_type}\t{max_fare}\t{min_fare}\t{total_fare}\t{count}"
    print(line)