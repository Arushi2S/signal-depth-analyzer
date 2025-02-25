import pandas as pd
import re
from collections import defaultdict

# Load dataset
splits = {'train': 'data/train-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/ahmedallam/RTL-Repo/" + splits["train"])

def extract_verilog_features(code):
    return {
        "num_AND": len(re.findall(r"\band\b", code, re.IGNORECASE)),
        "num_OR": len(re.findall(r"\bor\b", code, re.IGNORECASE)),
        "num_XOR": len(re.findall(r"\bxor\b", code, re.IGNORECASE)),
        "num_NOT": len(re.findall(r"\bnot\b", code, re.IGNORECASE)),
        "num_DFF": len(re.findall(r"\bdff\b", code, re.IGNORECASE)),
        "num_always": len(re.findall(r"\balways\b", code, re.IGNORECASE)),
        "num_wire": len(re.findall(r"\bwire\b", code, re.IGNORECASE)),
        "num_reg": len(re.findall(r"\breg\b", code, re.IGNORECASE)),
        "num_assign": len(re.findall(r"\bassign\b", code, re.IGNORECASE)),
        "num_delay": len(re.findall(r"#\d+", code)),
    }

def analyze_verilog(verilog_code):
    signal_usage = defaultdict(lambda: {"inputs": 0, "outputs": 0})
    logic_depth = len(re.findall(r'=', verilog_code))
    num_conditions = len(re.findall(r'\b(if|else|case)\b', verilog_code))
    num_loops = len(re.findall(r'\b(for|while|repeat)\b', verilog_code))
    num_instantiations = len(re.findall(r'\b\w+\s+\w+\s*\(.*?\);', verilog_code))

    signals = re.findall(r'\b(?:wire|reg)\s+([\w\[\], ]+);', verilog_code)
    for signal_group in signals:
        for signal in re.findall(r'\b\w+\b', signal_group):
            signal_usage[signal]
    
    assignments = re.findall(r'(\w+)\s*=\s*(.+);', verilog_code)
    for output_signal, input_signals in assignments:
        signal_usage[output_signal]["outputs"] += 1
        for input_signal in re.findall(r'\b\w+\b', input_signals):
            if input_signal in signal_usage:
                signal_usage[input_signal]["inputs"] += 1
    
    total_fan_in = sum(s["inputs"] for s in signal_usage.values())
    total_fan_out = sum(s["outputs"] for s in signal_usage.values())
    num_signals = len(signal_usage)
    
    avg_fan_in = total_fan_in / num_signals if num_signals else 0
    avg_fan_out = total_fan_out / num_signals if num_signals else 0
    
    return avg_fan_in, avg_fan_out, logic_depth, num_conditions, num_loops, num_instantiations

# Feature extraction and analysis
df_features = df["all_code"].apply(extract_verilog_features).apply(pd.Series)
df_analysis = df["all_code"].apply(lambda code: pd.Series(analyze_verilog(code), 
    index=['avg_fan_in', 'avg_fan_out', 'logic_depth', 'num_conditions', 'num_loops', 'num_instantiations']))

df = pd.concat([df, df_features, df_analysis], axis=1)

df.to_csv("analyzing_dataset.csv", index=False)
df.to_parquet("analyzing_dataset.parquet")

print("Dataset successfully saved as CSV and Parquet ✅")
print(df.head())
