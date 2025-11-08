# Directory paths
BENCHMARKS_DIR="./benchmarks"
RESULTS_DIR="./results"

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

# Find the first 10 smallest files in ./benchmarks/ sorted by size, then loop over them (sort -nr for largest)
for file in $(find "$BENCHMARKS_DIR" -type f -exec du -b {} + | sort -n | head -n 10 | cut -f2); do
    # Get the first 5 characters of the file name
    base_name=$(basename "$file")
    result_name="${base_name:0:5}.res"

    # Run minisat and save the result
    ./minisat/core/minisat "$file" "$RESULTS_DIR/$result_name"
done
