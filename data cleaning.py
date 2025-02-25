import pandas as pd
import networkx as nx

# Define file paths
input_file = r"C:\Users\Ashish Soti\Desktop\libraries\analyzing_dataset.parquet"
output_file = r"C:\Users\Ashish Soti\Desktop\libraries\newly_analyzed_data.parquet"

# Load the dataset
df = pd.read_parquet(input_file)

# Display basic info
print("Dataset Preview:")
print(df.head())
print("\nColumn Data Types:")
print(df.dtypes)

# Ensure expected columns exist
if 'source' not in df.columns or 'destination' not in df.columns:
    raise ValueError("Dataset must contain 'source' and 'destination' columns!")

# Create a directed graph
G = nx.DiGraph()

# Add edges (connections between signals)
for _, row in df.iterrows():
    G.add_edge(row['source'], row['destination'])

# Compute Fan-In and Fan-Out for each node
df['Fan_In'] = df['destination'].map(lambda node: G.in_degree(node))
df['Fan_Out'] = df['source'].map(lambda node: G.out_degree(node))

# Compute Signal Depth (longest path in DAG)
depths = {node: nx.single_source_longest_path_length(G, node) for node in G.nodes()}
df['Signal_Depth'] = df['destination'].map(lambda node: max(depths[node], default=0))

# Save the updated dataset
df.to_parquet(output_file)

print(f"Updated dataset saved as: {output_file}")

import pandas as pd

# Define file paths
input_file = r"C:\Users\Ashish Soti\Desktop\libraries\analyzing_dataset.parquet"
output_file = r"C:\Users\Ashish Soti\Desktop\libraries\newly_analyzed_data.parquet"

# Load dataset
df = pd.read_parquet(input_file)

# Display column names and preview
print("Dataset Columns:", df.columns)
print(df.head())

# Compute Fan-In (approximate as sum of logic inputs per row)
df['Fan_In'] = df[['num_AND', 'num_OR', 'num_XOR', 'num_NOT']].sum(axis=1)

# Compute Fan-Out (approximate as sum of storage elements per row)
df['Fan_Out'] = df[['num_DFF', 'num_always', 'num_assign']].sum(axis=1)

# Signal Depth (Use 'level' as depth indicator if available)
df['Signal_Depth'] = df['level']

# Save updated dataset
df.to_parquet(output_file)

print(f"Updated dataset saved as: {output_file}")

# Define file paths
input_file = r"C:\Users\Ashish Soti\Desktop\libraries\newly_analyzed_data.parquet"
output_file = r"C:\Users\Ashish Soti\Desktop\libraries\filtered_analyzed_data.parquet"

# Load dataset
df = pd.read_parquet(input_file)

# Keep only integer columns
df_int = df.select_dtypes(include=['int64', 'int32'])

# Save the filtered dataset
df_int.to_parquet(output_file)

# Print column names after filtering
print("Filtered dataset columns:", df_int.columns)
print(df_int.head())

print(f"Filtered dataset saved as: {output_file}")
import pandas as pd

# Define file paths
input_file = r"C:\Users\Ashish Soti\Desktop\libraries\newly_analyzed_data.parquet"
output_file = r"C:\Users\Ashish Soti\Desktop\libraries\filtered_analyzed_data.parquet"

# Load dataset
df = pd.read_parquet(input_file)

# Keep only integer columns
df_int = df.select_dtypes(include=['int64', 'int32'])

# Save the filtered dataset
df_int.to_parquet(output_file)

# Print the new shape and columns
print("Shape of strictly filtered dataset:", df_int.shape)
print("Columns in filtered dataset:", df_int.columns)
import pandas as pd

# Define file paths
input_file = r"C:\Users\Ashish Soti\Desktop\libraries\newly_analyzed_data.parquet"
output_file = r"C:\Users\Ashish Soti\Desktop\libraries\filtered_analyzed_data.parquet"

# Load dataset
df = pd.read_parquet(input_file)

# Convert 'Signal_Depth' to numeric (int or float)
if 'Signal_Depth' in df.columns:
    df['Signal_Depth'] = pd.to_numeric(df['Signal_Depth'], errors='coerce')

# Keep only numerical (int + float) columns
df_numeric = df.select_dtypes(include=['int64', 'int32', 'float64'])

# Save the updated dataset
df_numeric.to_parquet(output_file)

# Print the new shape and columns
print("Shape of final dataset:", df_numeric.shape)
print("Columns in final dataset:", df_numeric.columns)
import pandas as pd

# Define file paths
input_parquet = r"C:\Users\Ashish Soti\Desktop\libraries\filtered_analyzed_data.parquet"
output_csv = r"C:\Users\Ashish Soti\Desktop\libraries\final.csv"

# Load the dataset
df_final = pd.read_parquet(input_parquet)

# Ensure required columns exist
required_columns = ['num_AND', 'num_OR', 'num_XOR', 'num_NOT', 'num_DFF', 'num_wire']
missing_columns = [col for col in required_columns if col not in df_final.columns]

if missing_columns:
    raise ValueError(f"Missing required columns in dataset: {missing_columns}")

# Compute Signal Depth based on RTL logic complexity
df_final['Signal_Depth'] = (
    (df_final['num_AND'] * 1) +  # AND gates contribute 1 depth level
    (df_final['num_OR'] * 1) +   # OR gates contribute 1 depth level
    (df_final['num_XOR'] * 2) +  # XOR gates are complex, so contribute 2 levels
    (df_final['num_NOT'] * 1) +  # NOT gates contribute 1 depth level
    (df_final['num_DFF'] * 3) +  # DFFs add pipeline stages, contributing more depth
    (df_final['num_wire'] // 2)  # Wire count adds signal propagation delay
)

# Ensure no zero values in Signal_Depth
df_final.loc[df_final['Signal_Depth'] == 0, 'Signal_Depth'] = 1  # Set minimum depth to 1

# Save the final dataset as CSV
df_final.to_csv(output_csv, index=False)

# Display summary
print("✅ Final dataset saved successfully!")
print(df_final[['Signal_Depth']].describe())  # Show statistics of Signal_Depth
print(df_final.head())  # Display first few rows
