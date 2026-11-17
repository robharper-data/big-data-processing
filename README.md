# Big data processing: Hadoop MapReduce, Apache Pig and Spark Streaming

Three distributed data-processing projects run on a Hadoop cluster (AWS EMR): batch analytics and clustering with MapReduce, an ETL pipeline in Pig with a Python user-defined function, and real-time text analytics with Spark Streaming in Scala.

A joint project by Joseph Mchaileh and Robert Harper, completed in 2025 during our Master of Data Science at RMIT University.

## 1. Hadoop MapReduce (`01-hadoop-mapreduce`)

Python mappers and reducers run with Hadoop Streaming over taxi trip records.

- **Fare statistics by taxi and trip length.** Each trip is classed as short, medium or long by distance, and the trip count and maximum, minimum and average fare are calculated for each taxi and class. The mapper uses an in-mapper combiner to aggregate locally before the shuffle.
- **K-medoids (PAM) clustering of drop-off locations.** An iterative MapReduce job: the mapper assigns each drop-off point to its nearest medoid, and the reducer picks the point in each cluster with the smallest total distance to the others as the new medoid. A driver script reruns the job until the medoids stop changing or a maximum number of iterations is reached.
- **Trips per taxi company, sorted.** Three chained jobs: a reduce-side join of trips to taxis to attach each trip's company, a count of trips per company (again with an in-mapper combiner), and a sort by trip count that uses range partitioning to spread companies evenly across three reducers.

## 2. Apache Pig (`02-apache-pig`)

An ETL pipeline over three related tables: trips, taxis and companies.

- **Clean:** remove trips with missing fields, non-positive distances, distances over 20 km or fares under $5.
- **Enrich:** join trips to taxis and then to companies.
- **Aggregate:** trip count, total and average distance, and average fare for each company, sorted by trip count.
- **Python UDF:** `fare_band.py` classes each fare as LOW (up to $15), MID ($15 to $30) or HIGH (over $30). The results are counted per company and pivoted into one column per band, with zeros for empty bands.

`validation_checks.ipynb` reproduces the cleaning rules in pandas, as an independent check on how many records the Pig script should keep.

## 3. Spark Streaming in Scala (`03-spark-streaming`)

A Spark Streaming application that watches an HDFS folder and processes each new file as it arrives, in 3-second batches.

- **Word counts:** words are cleaned to letters only, with words under three characters removed, and counted for each batch.
- **Co-occurrence counts:** for each batch, every ordered pair of words in the same line is counted.
- **Running totals:** co-occurrence counts accumulate across batches with `updateStateByKey` and checkpointing. Output is written only when new files have arrived, not on empty intervals.

## Data

The taxi data (trips, taxis and companies) was a synthetic dataset supplied by the course and is not included. The table layouts are defined at the top of `a2.pig`. The streaming application takes any plain-text files.

The k-medoids job reads its starting point from `initialization.txt`: the maximum number of iterations on the first line, then one tab-separated `x y` medoid per line.

## Running it

All three parts were written for a Hadoop cluster with HDFS, Pig and Spark (AWS EMR).

- **MapReduce:** place `hadoop-streaming-3.1.4.jar` in the folder, load the input files to `/Input` on HDFS and run `Task1-run.sh`, `Task2-run.sh` or `Task3-run.sh`.
- **Pig:** load the input files to `/Input` on HDFS and run `run.sh`.
- **Spark Streaming:** build the jar with `mvn package`, then submit it with input and output folders on HDFS:

```
spark-submit --class streaming.a3 --master yarn --deploy-mode client a3.jar hdfs:///input hdfs:///output
```
