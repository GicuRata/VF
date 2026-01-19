import csv
import os
import subprocess
import glob
import time

# configuration
CSV_FILE = 'benchmark-competition-results/detailed_main.csv'
BENCHMARKS_DIR = 'benchmarks'
RESULTS_DIR = 'results'
MINISAT_BIN = './minisat/core/minisat'
TOP_N = 40

def get_average_time(row):
    """calculates the average time from the solver columns"""
    times = []
    for key, value in row.items():
        if key in ['hash', 'vresult']:
            continue
        try:
            time_val = float(value)
            times.append(time_val)
        except ValueError:
            # treat non-numeric as timeout
            times.append(10000.0)
    
    if not times:
        return 10000.0
    
    return sum(times) / len(times)

def main():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    benchmark_stats = []

    print(f"Reading {CSV_FILE}...")
    try:
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                avg_time = get_average_time(row)
                benchmark_stats.append({
                    'hash': row['hash'],
                    'avg_time': avg_time
                })
    except FileNotFoundError:
        print(f"Error: CSV file {CSV_FILE} not found.")
        return

    # sort by average time ascending
    benchmark_stats.sort(key=lambda x: x['avg_time'])

    # select top n
    top_benchmarks = benchmark_stats[:TOP_N]

    print(f"Found {len(top_benchmarks)} benchmarks. Running top {TOP_N}...")
    
    # 5 minutes timeout
    TIMEOUT_SECONDS = 300

    run_count = 0
    for bench in top_benchmarks:
        h = bench['hash']
        # find the file in benchmarks dir
        pattern = os.path.join(BENCHMARKS_DIR, f"{h}*")
        files = glob.glob(pattern)
        
        if not files:
            print(f"Warning: No file found for hash {h}")
            continue
        
        benchmark_file = files[0]
        base_name = os.path.basename(benchmark_file)
        
        result_name = base_name[:5] + ".res"
        result_path = os.path.join(RESULTS_DIR, result_name)
        
        print(f"[{run_count+1}/{TOP_N}] Running {base_name} (Avg Time: {bench['avg_time']:.2f}s)")
        
        cmd = [MINISAT_BIN, benchmark_file, result_path]
        
        start_time = time.time()
        try:
            # minisat returns 10 for sat and 20 for unsat, which are valid outcomes
            result = subprocess.run(cmd, check=False, timeout=TIMEOUT_SECONDS)
            execution_time = time.time() - start_time
            print(f"  > Execution Time: {execution_time:.2f}s")
            
            if result.returncode in [0, 10, 20]:
                # append execution time to the result file
                try:
                    with open(result_path, 'a') as rf:
                        rf.write(f"\nExecution Time: {execution_time:.2f}s\n")
                except Exception as file_e:
                    print(f"  > Error writing time to output file: {file_e}")
            else:
                print(f"  > Error running minisat on {base_name}: Return code {result.returncode}")
        except subprocess.TimeoutExpired:
            print(f"  > Timeout reached after {TIMEOUT_SECONDS}s")
            # note timeout in the file if it was created
            try:
                with open(result_path, 'a') as rf:
                     rf.write(f"\nTimeout after {TIMEOUT_SECONDS}s\n")
            except:
                pass
        except Exception as e:
            print(f"  > Error running minisat on {base_name}: {e}")
        
        run_count += 1

    print("Done.")

if __name__ == "__main__":
    main()
