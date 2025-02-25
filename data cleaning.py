import pandas as pd
import networkx as nx

# Define file paths
input_file = r"C:\Users\Ashish Soti\Desktop\libraries\analyzing_dataset.parquet"
output_file = r"C:\Users\Ashish Soti\Desktop\libraries\newly_analyzed_data.parquet"
filtered_output_file = r"C:\Users\Ashish Soti\Desktop\libraries\filtered_analyzed_data.parquet"
final_csv = r"C:\Users\Ashish Soti\Desktop\libraries\final.csv"

# Load dataset
df = pd.read_parquet(input_file)
print("Dataset Preview:")
print(df.head())
print("\nColumn Data Types:")
print(df.dtypes)

# Ensure expected columns exist
if 'source' not in df.columns or 'destination' not in df.columns:
    raise ValueError("Dataset must contain 'source' and 'destination' columns!")

# Create directed graph
G = nx.DiGraph()
G.add_edges_from(df[['source', 'destination']].itertuples(index=False, name=None))

# Compute Fan-In and Fan-Out
df['Fan_In'] = df['destination'].map(G.in_degree)
df['Fan_Out'] = df['source'].map(G.out_degree)

# Compute Signal Depth
depths = {node: nx.single_source_longest_path_length(G, node) for node in G.nodes()}
df['Signal_Depth'] = df['destination'].map(depths.get).fillna(0).astype(int)

# Save updated dataset
df.to_parquet(output_file)
print(f"Updated dataset saved as: {output_file}")

# Keep only integer columns
df_int = df.select_dtypes(include=['int64', 'int32'])
df_int.to_parquet(filtered_output_file)
print("Filtered dataset saved as:", filtered_output_file)

# Convert 'Signal_Depth' to numeric and keep numerical columns
df_numeric = df.select_dtypes(include=['int64', 'int32', 'float64'])
df_numeric.to_parquet(filtered_output_file)
print("Shape of final dataset:", df_numeric.shape)
print("Columns in final dataset:", df_numeric.columns)

# Load final dataset for CSV conversion
df_final = pd.read_parquet(filtered_output_file)
required_columns = ['num_AND', 'num_OR', 'num_XOR', 'num_NOT', 'num_DFF', 'num_wire']
missing_columns = [col for col in required_columns if col not in df_final.columns]
if missing_columns:
    raise ValueError(f"Missing required columns in dataset: {missing_columns}")

# Compute Signal Depth
weights = {'num_AND': 1, 'num_OR': 1, 'num_XOR': 2, 'num_NOT': 1, 'num_DFF': 3, 'num_wire': 0.5}
df_final['Signal_Depth'] = sum(df_final[col] * weight for col, weight in weights.items())
df_final['Signal_Depth'] = df_final['Signal_Depth'].clip(lower=1).astype(int)

# Save as CSV
df_final.to_csv(final_csv, index=False)
print("✅ Final dataset saved successfully!")
print(df_final[['Signal_Depth']].describe())
print(df_final.head())
