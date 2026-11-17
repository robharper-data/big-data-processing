#!/bin/bash    

IN=/Input
OUT1=/job1_out
OUT2=/job2_out
OUT3=/Output/Task3

# clean outputs for repeatable runs
hadoop fs -rm -r -f "$OUT1" "$OUT2" "$OUT3"

##### 1st Job - JOIN #####
hadoop jar ./hadoop-streaming-3.1.4.jar \
-D stream.num.map.output.key.fields=2 \
-D mapred.text.key.partitioner.options=-k1,1 \
-D mapred.reduce.tasks=3 \
-file ./Task3_Join_Mapper.py \
-mapper ./Task3_Join_Mapper.py \
-file ./Task3_Join_Reducer.py \
-reducer ./Task3_Join_Reducer.py \
-input "$IN" \
-output "$OUT1" \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

##### 2nd Job - COUNT #####
hadoop jar ./hadoop-streaming-3.1.4.jar \
-D mapred.reduce.tasks=3 \
-file ./Task3_Count_Mapper.py \
-mapper ./Task3_Count_Mapper.py \
-file ./Task3_Count_Reducer.py \
-reducer ./Task3_Count_Reducer.py \
-input "$OUT1" \
-output "$OUT2" \

hadoop fs -rm -r -f "$OUT1"

##### 3rd Job - SORT #####
hadoop jar ./hadoop-streaming-3.1.4.jar \
-D stream.num.map.output.key.fields=3 \
-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D mapred.text.key.comparator.options=-k3,3n \
-D mapred.text.key.partitioner.options=-k2,2 \
-D mapred.reduce.tasks=3 \
-file ./Task3_Sort_Mapper.py \
-mapper ./Task3_Sort_Mapper.py \
-file ./Task3_Sort_Reducer.py \
-reducer ./Task3_Sort_Reducer.py \
-input "$OUT2" \
-output "$OUT3" \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

hadoop fs -rm -r -f "$OUT2"

