#!/usr/bin/env python3
import sys

for line in sys.stdin: #Stream data
    line = line.strip()
    records = line.split('\t') #Retrieve company and trip no's
    company = records[0].strip() #Get company
    try:
        num_of_trips = int(records[1].strip())   #Number of trips should be an integer, if not, skip
    except (IndexError, ValueError):
        continue 
    if num_of_trips < 1500: #Bin the company trips in ranges, so that they get sent to different reducers using the hash function.             
        flag = '0'
        print('%s\t%s\t%s' % (company,flag,num_of_trips)) #The bin thresholds were decided based on the dataset we are working with. Each reducer should get a roughly equal amound of companies
    elif num_of_trips < 1800 and num_of_trips >= 1500:
        flag = '1'
        print('%s\t%s\t%s' % (company,flag,num_of_trips))
    else:
        flag = '2'
        print('%s\t%s\t%s' % (company,flag,num_of_trips))