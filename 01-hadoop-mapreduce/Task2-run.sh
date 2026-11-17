#!/bin/bash

v=$(python task2_init.py)
i=1

echo "PAM clustering started"
echo "Maximum iterations: $v"

while :; do
    echo "Iteration: $i"

    hadoop fs -rm -r -f /mapreduce-output$i
    hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -D mapred.text.key.partitioner.options=-k1 \
    -file medoids.txt \
    -file ./Task2_mapper.py \
    -mapper ./Task2_mapper.py \
    -file ./Task2_reducer.py \
    -reducer ./Task2_reducer.py \
    -input /Input/Trips.txt \
    -output /mapreduce-output$i \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
        
    rm -f medoids1.txt
    hadoop fs -getmerge /mapreduce-output$i/part* medoids1.txt
        
    echo "Medoids for iteration $i"
    cat medoids1.txt
    echo ""

    seeiftrue=$(python reader.py)
        
    if [ "$seeiftrue" = "1" ] || [ "$i" -eq "$v" ]; then
        echo "Stopping at iteration: $i"
        
        # Copy final result to required output location
        hadoop fs -rm -r -f /Output/Task2
        hadoop fs -mkdir -p /Output
        hadoop fs -cp /mapreduce-output$i /Output/Task2
        
        # Final Cleanup
        rm -f medoids.txt
        rm -f medoids1.txt
        rm -f .medoids.txt.crc
        rm -f .medoids1.txt.crc
        hadoop fs -rm -r -f /mapreduce-output$i
        break
    else
        echo "Not converged after iteration: $i"
        echo "Continuing to next iteration ..."
        
        # Update medoids for next iteration
        rm -f medoids.txt
        hadoop fs -getmerge /mapreduce-output$i/part* medoids.txt
        
        # Clean up this iteration's output (keep storage tidy)
        hadoop fs -rm -r -f /mapreduce-output$i
    fi

    i=$((i+1))
done

echo "PAM clustering completed"