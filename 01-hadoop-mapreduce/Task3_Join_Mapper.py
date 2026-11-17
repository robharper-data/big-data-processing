#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    records = line.split(',')
    if len(records) == 4: #There are 4 fields, it is a company record
        flag = '0' #This flag should ensure the taxi record would be first in the reducer, before the trips associated with the taxi
        try:
            taxi_id = records[0].strip()
            company = records[1].strip()
            print('%s\t%s\t%s' % (taxi_id,flag,company))
        except (IndexError, ValueError):
            continue  # Skip lines that don't parse properly
    elif len(records) == 8: #There are 8 fields, it is a trip record
        flag = '1' #Trip records for a taxi should be sorted after the taxi information
        try:
            trip_no = records[0].strip()
            taxi_id = records[1].strip()
            print('%s\t%s\t%s' % (taxi_id,flag,trip_no))
        except (IndexError, ValueError):
            continue  # Skip lines that don't parse properly
    else:
	    continue    # Skip lines that don't match expected formats

    #We want all the same taxis to go to the same reducer, but sorted with the flags


    