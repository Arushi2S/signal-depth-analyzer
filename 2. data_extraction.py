#firstly we have to clone the repos mentioned in readme file using command like (!git clone https://github.com/ekb0412/100DaysofRTL.git)
#1
import os
import json
import csv
import subprocess

# Yosys path (adjust if needed)
YOSYS_PATH = r"C:\msys64\mingw64\bin\yosys.exe"

# Base directory containing all Verilog projects
BASE_DIR = r"C:\Users\Ashish Soti\Desktop\libraries\verilog_projects"

# Get all Verilog files recursively
verilog_files = []
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".v"):  # Only pick Verilog files
            verilog_files.append(os.path.join(root, file))

# Function to extract all required features from Yosys JSON output
def extract_features(json_output, filename):
    features = []
    modules = json_output.get("modules", {})
    
    for module_name, module_data in modules.items():
        # Prepare feature dictionary with filename and module name
        feature_data = {"File": filename, "Signal Type": module_name.strip("\\")}
        
        # Include specific fields directly
        feature_data["Combinational Depth"] = module_data.get("num_cells", 0)  # Assuming num_cells ≈ depth
        feature_data["Fan-in"] = module_data.get("num_pub_wires", 0)
        feature_data["Fan-out"] = module_data.get("num_wire_bits", 0)
        
        # Add other relevant fields from the module data
        feature_data["num_memories"] = module_data.get("num_memories", 0)
        feature_data["num_pub_wire_bits"] = module_data.get("num_pub_wire_bits", 0)
        feature_data["num_memory_bits"] = module_data.get("num_memory_bits", 0)
        feature_data["num_pub_wires"] = module_data.get("num_pub_wires", 0)
        feature_data["num_cells"] = module_data.get("num_cells", 0)
        feature_data["num_wires"] = module_data.get("num_wires", 0)
        feature_data["num_wire_bits"] = module_data.get("num_wire_bits", 0)
        feature_data["num_processes"] = module_data.get("num_processes", 0)
        
        features.append(feature_data)
    
    return features

# Process each Verilog file
all_features = []
for verilog_file in verilog_files:
    try:
        # Convert Windows path to Unix-style for MSYS2
        verilog_file_fixed = verilog_file.replace("\\", "/")
        
        # Run Yosys command
        command = f'"{YOSYS_PATH}" -p "read_verilog \\"{verilog_file_fixed}\\"; stat -json"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Extract JSON output from Yosys
        output = result.stdout
        json_start = output.find("{")  # Find where JSON starts
        json_end = output.rfind("}")   # Find where JSON ends
        
        if json_start != -1 and json_end != -1:
            json_data = json.loads(output[json_start:json_end+1])
            extracted = extract_features(json_data, verilog_file)
            all_features.extend(extracted)
        else:
            print(f"⚠️ Failed to parse Yosys output for {verilog_file}")
    
    except Exception as e:
        print(f"❌ Error processing {verilog_file}: {e}")

# Save extracted data to CSV
csv_filename = "yosys_full_dataset.csv"
# Collect all unique fieldnames (keys from the first feature dictionary)
if all_features:
    fieldnames = list(set().union(*(f.keys() for f in all_features)))

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_features)

print(f"✅ Processed {len(verilog_files)} files and saved dataset to {csv_filename}")

#2nd

import os
import json
import csv
import subprocess

# Yosys path (adjust if needed)
YOSYS_PATH = r"C:\msys64\mingw64\bin\yosys.exe"

# Base directory containing Verilog design examples
BASE_DIR = r"C:\Users\Ashish Soti\Desktop\libraries\verilog_design_examples"

# Get all Verilog files recursively
verilog_files = []
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".v"):  # Only pick Verilog files
            verilog_files.append(os.path.join(root, file))

# Function to extract all required features from Yosys JSON output
def extract_features(json_output, filename):
    features = []
    modules = json_output.get("modules", {})
    
    for module_name, module_data in modules.items():
        # Prepare feature dictionary with filename and module name
        feature_data = {"File": filename, "Signal Type": module_name.strip("\\")}
        
        # Include specific fields directly
        feature_data["Combinational Depth"] = module_data.get("num_cells", 0)  # Assuming num_cells ≈ depth
        feature_data["Fan-in"] = module_data.get("num_pub_wires", 0)
        feature_data["Fan-out"] = module_data.get("num_wire_bits", 0)
        
        # Add other relevant fields from the module data
        feature_data["num_memories"] = module_data.get("num_memories", 0)
        feature_data["num_pub_wire_bits"] = module_data.get("num_pub_wire_bits", 0)
        feature_data["num_memory_bits"] = module_data.get("num_memory_bits", 0)
        feature_data["num_pub_wires"] = module_data.get("num_pub_wires", 0)
        feature_data["num_cells"] = module_data.get("num_cells", 0)
        feature_data["num_wires"] = module_data.get("num_wires", 0)
        feature_data["num_wire_bits"] = module_data.get("num_wire_bits", 0)
        feature_data["num_processes"] = module_data.get("num_processes", 0)
        
        features.append(feature_data)
    
    return features

# Process each Verilog file
all_features = []
for verilog_file in verilog_files:
    try:
        # Convert Windows path to Unix-style for MSYS2
        verilog_file_fixed = verilog_file.replace("\\", "/")
        
        # Run Yosys command
        command = f'"{YOSYS_PATH}" -p "read_verilog \\"{verilog_file_fixed}\\"; stat -json"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Extract JSON output from Yosys
        output = result.stdout
        json_start = output.find("{")  # Find where JSON starts
        json_end = output.rfind("}")   # Find where JSON ends
        
        if json_start != -1 and json_end != -1:
            json_data = json.loads(output[json_start:json_end+1])
            extracted = extract_features(json_data, verilog_file)
            all_features.extend(extracted)
        else:
            print(f"⚠️ Failed to parse Yosys output for {verilog_file}")
    
    except Exception as e:
        print(f"❌ Error processing {verilog_file}: {e}")

# Save extracted data to CSV
csv_filename = "yosys_full_dataset1.csv"
# Collect all unique fieldnames (keys from the first feature dictionary)
if all_features:
    fieldnames = list(set().union(*(f.keys() for f in all_features)))

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_features)

print(f"✅ Processed {len(verilog_files)} files and saved dataset to {csv_filename}")

#3

import os
import json
import csv
import subprocess

# Yosys path (adjust if needed)
YOSYS_PATH = r"C:\msys64\mingw64\bin\yosys.exe"

# Base directory containing Verilog files in the new location
BASE_DIR = r"C:\Users\Ashish Soti\Desktop\synthese\sky130RTLDesignAndSynthesisWorkshop\verilog_files"

# Get all Verilog files recursively
verilog_files = []
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".v"):  # Only pick Verilog files
            verilog_files.append(os.path.join(root, file))

# Function to extract all required features from Yosys JSON output
def extract_features(json_output, filename):
    features = []
    modules = json_output.get("modules", {})
    
    for module_name, module_data in modules.items():
        # Prepare feature dictionary with filename and module name
        feature_data = {"File": filename, "Signal Type": module_name.strip("\\")}
        
        # Include specific fields directly
        combinational_depth = module_data.get("num_cells", 0)  # Assuming num_cells ≈ depth
        if combinational_depth == 0:
            continue  # Skip if combinational depth is 0
        feature_data["Combinational Depth"] = combinational_depth
        feature_data["Fan-in"] = module_data.get("num_pub_wires", 0)
        feature_data["Fan-out"] = module_data.get("num_wire_bits", 0)
        
        # Add other relevant fields from the module data
        feature_data["num_memories"] = module_data.get("num_memories", 0)
        feature_data["num_pub_wire_bits"] = module_data.get("num_pub_wire_bits", 0)
        feature_data["num_memory_bits"] = module_data.get("num_memory_bits", 0)
        feature_data["num_pub_wires"] = module_data.get("num_pub_wires", 0)
        feature_data["num_cells"] = module_data.get("num_cells", 0)
        feature_data["num_wires"] = module_data.get("num_wires", 0)
        feature_data["num_wire_bits"] = module_data.get("num_wire_bits", 0)
        feature_data["num_processes"] = module_data.get("num_processes", 0)
        
        features.append(feature_data)
    
    return features

# Process each Verilog file
all_features = []
for verilog_file in verilog_files:
    try:
        # Convert Windows path to Unix-style for MSYS2
        verilog_file_fixed = verilog_file.replace("\\", "/")
        
        # Run Yosys command
        command = f'"{YOSYS_PATH}" -p "read_verilog \\"{verilog_file_fixed}\\"; stat -json"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Extract JSON output from Yosys
        output = result.stdout
        json_start = output.find("{")  # Find where JSON starts
        json_end = output.rfind("}")   # Find where JSON ends
        
        if json_start != -1 and json_end != -1:
            json_data = json.loads(output[json_start:json_end+1])
            extracted = extract_features(json_data, verilog_file)
            all_features.extend(extracted)
        else:
            print(f"⚠️ Failed to parse Yosys output for {verilog_file}")
    
    except Exception as e:
        print(f"❌ Error processing {verilog_file}: {e}")

# Remove entries with combinational depth 0
filtered_features = [feature for feature in all_features if feature["Combinational Depth"] > 0]

# Save extracted data to CSV
csv_filename = "yosys_full_dataset2.csv"
# Collect all unique fieldnames (keys from the first feature dictionary)
if filtered_features:
    fieldnames = list(set().union(*(f.keys() for f in filtered_features)))

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered_features)

print(f"✅ Processed {len(verilog_files)} files, removed entries with combinational depth 0, and saved dataset to {csv_filename}")

#4
import os 
import json
import csv
import subprocess

# Yosys path (adjust if needed)
YOSYS_PATH = r"C:\msys64\mingw64\bin\yosys.exe"

# Base directory containing Verilog files in the new location
BASE_DIR = r"C:\Users\Ashish Soti\Desktop\signal depth\100DaysofRTL"  # Updated base directory

# Get all Verilog files recursively
verilog_files = []
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".v"):  # Only pick Verilog files
            verilog_files.append(os.path.join(root, file))

# Function to extract all required features from Yosys JSON output
def extract_features(json_output, filename):
    features = []
    modules = json_output.get("modules", {})
    
    for module_name, module_data in modules.items():
        # Prepare feature dictionary with filename and module name
        feature_data = {"File": filename, "Signal Type": module_name.strip("\\")}
        
        # Include specific fields directly
        combinational_depth = module_data.get("num_cells", 0)  # Assuming num_cells ≈ depth
        if combinational_depth == 0:
            continue  # Skip if combinational depth is 0
        feature_data["Combinational Depth"] = combinational_depth
        feature_data["Fan-in"] = module_data.get("num_pub_wires", 0)
        feature_data["Fan-out"] = module_data.get("num_wire_bits", 0)
        
        # Add other relevant fields from the module data
        feature_data["num_memories"] = module_data.get("num_memories", 0)
        feature_data["num_pub_wire_bits"] = module_data.get("num_pub_wire_bits", 0)
        feature_data["num_memory_bits"] = module_data.get("num_memory_bits", 0)
        feature_data["num_pub_wires"] = module_data.get("num_pub_wires", 0)
        feature_data["num_cells"] = module_data.get("num_cells", 0)
        feature_data["num_wires"] = module_data.get("num_wires", 0)
        feature_data["num_wire_bits"] = module_data.get("num_wire_bits", 0)
        feature_data["num_processes"] = module_data.get("num_processes", 0)
        
        features.append(feature_data)
    
    return features

# Process each Verilog file
all_features = []
for verilog_file in verilog_files:
    try:
        # Convert Windows path to Unix-style for MSYS2
        verilog_file_fixed = verilog_file.replace("\\", "/")
        
        # Run Yosys command
        command = f'"{YOSYS_PATH}" -p "read_verilog \\"{verilog_file_fixed}\\"; stat -json"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Extract JSON output from Yosys
        output = result.stdout
        json_start = output.find("{")  # Find where JSON starts
        json_end = output.rfind("}")   # Find where JSON ends
        
        if json_start != -1 and json_end != -1:
            json_data = json.loads(output[json_start:json_end+1])
            extracted = extract_features(json_data, verilog_file)
            all_features.extend(extracted)
        else:
            print(f"⚠️ Failed to parse Yosys output for {verilog_file}")
    
    except Exception as e:
        print(f"❌ Error processing {verilog_file}: {e}")

# Remove entries with combinational depth 0
filtered_features = [feature for feature in all_features if feature["Combinational Depth"] > 0]

# Save extracted data to CSV
csv_filename = "yosys_full_dataset4.csv" 

# Collect all unique fieldnames (keys from the first feature dictionary)
if filtered_features:
    fieldnames = list(set().union(*(f.keys() for f in filtered_features)))

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered_features)

print(f"✅ Processed {len(verilog_files)} files, removed entries with combinational depth 0, and saved dataset to {csv_filename}")
