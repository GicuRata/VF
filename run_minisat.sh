#!/bin/bash

# Directory paths
BENCHMARKS_DIR="./benchmarks"
RESULTS_DIR="./results"

# --- CONFIGURATION ---
# Define the range of files to process, sorted by size.
START_INDEX=10
END_INDEX=20

mkdir -p "$RESULTS_DIR"

echo "Processing files from index $START_INDEX to $END_INDEX..."

# Find all files, get their size, sort them, and select the desired range
for file in $(find "$BENCHMARKS_DIR" -type f -exec du -b {} + | sort -nr | sed -n "${START_INDEX},${END_INDEX}p" | cut -f2-); do
    base_name=$(basename "$file")
    result_name="${base_name:0:5}.res"
    echo "Running minisat on $file..."
    ./minisat/core/minisat "$file" "$RESULTS_DIR/$result_name"
done

echo "Done."