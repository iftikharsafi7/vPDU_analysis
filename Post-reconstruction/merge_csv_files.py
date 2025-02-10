import pandas as pd
import glob

# Get all CSV files matching the pattern
files = glob.glob('run*_vPDU-38_q.csv')

# Extract the run number from the filename for sorting
def extract_run_number(file_path):
    run_str = file_path.split('_')[0]  # Get "runXXX"
    return int(run_str[3:])  # Extract numeric part (XXX) and convert to integer

# Sort files by run number
sorted_files = sorted(files, key=extract_run_number)

# Initialize an empty list to store DataFrames
dataframes = []

# Read each file, add a 'Run' column, and append to the list
for file in sorted_files:
    run_number = extract_run_number(file)
    df = pd.read_csv(file)
    df.insert(0, 'Run', run_number)  # Insert 'Run' column at the beginning
    dataframes.append(df)

# Merge all DataFrames in order
merged_df = pd.concat(dataframes, ignore_index=True)

# Save the merged result (optional)
merged_df.to_csv('merged_output.csv', index=False)

print(f"Merged {len(sorted_files)} files into merged_output.csv with Run numbers added.")
