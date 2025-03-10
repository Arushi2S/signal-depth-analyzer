# firstly clone repo and check if you are able to access signals before running yosys analysis
import os

def find_verilog_files(root_dirs):
    verilog_files = []
    for root_dir in root_dirs:
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".v"):
                    verilog_files.append(os.path.join(root, file))
    return verilog_files

# Example usage:
verilog_dirs = [
    r"C:\Users\Ashish Soti\Desktop\libraries\verilog_projects",
    r"C:\Users\Ashish Soti\Desktop\libraries\verilog_design_examples"
]
verilog_files = find_verilog_files(verilog_dirs)
print(f"Found {len(verilog_files)} Verilog files.")

import re

def extract_signals_from_file(verilog_file):
    signals = []
    with open(verilog_file, "r") as file:
        for line in file:
            line = line.strip()
            match = re.match(r"^(input|output|wire|reg)\s+([\w\s,]+);", line)
            if match:
                signal_type, signal_names = match.groups()
                for sig in signal_names.split(","):
                    signals.append({"Signal Name": sig.strip(), "Signal Type": signal_type, "File": verilog_file})
    return signals

# Extract signals from all Verilog files
all_signals = []
for vfile in verilog_files:
    all_signals.extend(extract_signals_from_file(vfile))

print(f"Extracted {len(all_signals)} signals from 89 files.")

#then we can proceed to data extraction 
