#!/usr/bin/env python3
# task2_init.py
import sys

# Initialize medoids from initialization.txt and create medoids.txt
def main(in_path, out_path):
    with open(in_path, "r") as f:
        lines = f.read().splitlines()

    # Handle empty file case
    if not lines:
        raise ValueError("initialization.txt is empty")

    # Extract max iterations
    first = lines[0].strip()

    # Convert to integer
    try:
        v = int(first)
    except ValueError:
        raise ValueError("v must be an integer")
        
    # Write remaining lines to medoids.txt
    rest = lines[1:]
    with open(out_path, "w") as g: 
        if rest:
            g.write("\n".join(rest) + "\n")

    # Print v to standard output - needed by bash script
    print(v)

# Run the initialization program
if __name__ == "__main__":
    in_path =  "initialization.txt"
    out_path = "medoids.txt"
    main(in_path, out_path)
