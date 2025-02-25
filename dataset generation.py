pip install pandas pyarrow

import pandas as pd

splits = {'train': 'data/train-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/ahmedallam/RTL-Repo/" + splits["train"])

print(df)
import pandas as pd
import re

# Load dataset
splits = {'train': 'data/train-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/ahmedallam/RTL-Repo/" + splits["train"])

# Feature extraction function
def extract_verilog_features(code):
    features = {
        "num_AND": len(re.findall(r"\band\b", code, re.IGNORECASE)),
        "num_OR": len(re.findall(r"\bor\b", code, re.IGNORECASE)),
        "num_XOR": len(re.findall(r"\bxor\b", code, re.IGNORECASE)),
        "num_NOT": len(re.findall(r"\bnot\b", code, re.IGNORECASE)),
        "num_DFF": len(re.findall(r"\bdff\b", code, re.IGNORECASE)),
        "num_always": len(re.findall(r"\balways\b", code, re.IGNORECASE)),
        "num_wire": len(re.findall(r"\bwire\b", code, re.IGNORECASE)),
        "num_reg": len(re.findall(r"\breg\b", code, re.IGNORECASE)),
        "num_assign": len(re.findall(r"\bassign\b", code, re.IGNORECASE)),
        "num_delay": len(re.findall(r"#\d+", code))  # Captures #5, #10 delays
    }
    return features

# Apply feature extraction on all Verilog code
feature_df = df["all_code"].apply(extract_verilog_features).apply(pd.Series)

# Merge features with original dataset
df = pd.concat([df, feature_df], axis=1)

# Save processed dataset
df.to_csv("rtl_dataset_with_features.csv", index=False)

print("Dataset saved as 'rtl_dataset_with_features.csv'")
print(df.head())  # Check first few rows

df = pd.read_csv("rtl_dataset_with_features.csv")

# Get dataset shape
num_rows, num_cols = df.shape
print(f"Dataset Size: {num_rows} rows, {num_cols} columns")

# Get feature names
features = df.columns.tolist()
print("Features:", features)

import pandas as pd
import re
from collections import defaultdict

# Load dataset
df = pd.read_csv("rtl_dataset_with_features.csv")

# Function to extract Fan-in, Fan-out, and other key features
def analyze_verilog(verilog_code):
    signal_usage = defaultdict(lambda: {"inputs": 0, "outputs": 0})
    logic_depth = 0
    num_conditions = 0
    num_loops = 0
    num_instantiations = 0

    # Extract wire and reg signals
    signals = re.findall(r'\b(?:wire|reg)\s+([\w\[\], ]+);', verilog_code)
    for signal_group in signals:
        for signal in re.findall(r'\b\w+\b', signal_group):
            signal_usage[signal]  # Initialize

    # Extract assignments (for Fan-in & Fan-out)
    assignments = re.findall(r'(\w+)\s*=\s*(.+);', verilog_code)
    for output_signal, input_signals in assignments:
        signal_usage[output_signal]["outputs"] += 1
        for input_signal in re.findall(r'\b\w+\b', input_signals):
            if input_signal in signal_usage:
                signal_usage[input_signal]["inputs"] += 1

    # Estimate logic depth (by counting chained assignments)
    logic_depth = len(re.findall(r'=', verilog_code))

    # Count conditional statements
    num_conditions = len(re.findall(r'\b(if|else|case)\b', verilog_code))

    # Count loops
    num_loops = len(re.findall(r'\b(for|while|repeat)\b', verilog_code))

    # Count module instantiations (hierarchical complexity)
    num_instantiations = len(re.findall(r'\b\w+\s+\w+\s*\(.*?\);', verilog_code))

    # Compute average Fan-in and Fan-out
    total_fan_in = sum(s["inputs"] for s in signal_usage.values())
    total_fan_out = sum(s["outputs"] for s in signal_usage.values())
    num_signals = len(signal_usage)

    avg_fan_in = total_fan_in / num_signals if num_signals else 0
    avg_fan_out = total_fan_out / num_signals if num_signals else 0

    return avg_fan_in, avg_fan_out, logic_depth, num_conditions, num_loops, num_instantiations

# Apply analysis to all rows
df[['avg_fan_in', 'avg_fan_out', 'logic_depth', 'num_conditions', 'num_loops', 'num_instantiations']] = df['all_code'].apply(
    lambda code: pd.Series(analyze_verilog(code))
)

# Save new dataset
df.to_csv("analyzing_dataset.csv", index=False)
print("Dataset saved as analyzing_dataset.csv ✅")

import pandas as pd

# Load dataset
df = pd.read_csv("rtl_dataset_with_features.csv", low_memory=False)

# Save as Parquet (efficient for large datasets)
df.to_parquet("analyzing_dataset.parquet")

print("Dataset successfully saved as 'analyzing_dataset.parquet' 🚀")

df_numeric = df.select_dtypes(include=['int64', 'float64'])

import pandas as pd  

# Load the Parquet file
file_path = "numeric_analyzing_dataset.parquet"  # Update this path if needed
df = pd.read_parquet(file_path)

# Display basic info about the dataset
print(df.info())

# Display the first few rows
df.head()
