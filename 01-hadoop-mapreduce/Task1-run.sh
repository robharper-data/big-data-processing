#!/bin/bash

hadoop fs -rm -r -f /Output/Task1

hadoop jar ./hadoop-streaming-3.1.4.jar \
-D stream.num.map.output.key.fields=2 \
-D mapred.reduce.tasks=3 \
-file ./Task1_mapper.py \
-mapper ./Task1_mapper.py \
-file ./Task1_reducer.py \
-reducer ./Task1_reducer.py \
-input /Input/Trips.txt \
-output /Output/Task1







