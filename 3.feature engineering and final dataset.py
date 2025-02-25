import pandas as pd
import numpy as np

# Load the dataset
file_path = "final.csv"
df = pd.read_csv(file_path)

# Feature Engineering
# 1. Gate Activity: Normalize logic gate usage
if {'num_AND', 'num_OR', 'num_XOR', 'num_NOT'}.issubset(df.columns):
    df['gate_activity'] = (df['num_AND'] + df['num_OR'] + df['num_XOR'] + df['num_NOT']) / (df.iloc[:, 1:5].sum(axis=1) + 1)

# 2. Register to Wire Ratio: Measures the complexity of register usage
if {'num_reg', 'num_wire'}.issubset(df.columns):
    df['reg_wire_ratio'] = df['num_reg'] / (df['num_wire'] + 1)  # Avoid division by zero

# 3. Circuit Complexity Score
if {'num_AND', 'num_OR', 'num_XOR', 'num_NOT', 'num_DFF'}.issubset(df.columns):
    df['complexity'] = (df['num_AND'] + 2 * df['num_OR'] + 3 * df['num_XOR'] +
                        0.5 * df['num_NOT'] + 5 * df['num_DFF'])

# 4. Log Transform Signal Depth to reduce large variations
if 'Signal_Depth' in df.columns:
    df['Signal_Depth'] = np.log1p(df['Signal_Depth'])  # log1p to handle zero values

# Save the updated dataset
output_file = "final1.csv"
df.to_csv(output_file, index=False)

print("✅ Feature engineering completed and dataset saved as final1.csv")

# Load dataset
df = pd.read_csv('final1.csv')

# Remove rows where too many columns have zero values
threshold = int(0.6 * len(df.columns))  # If 60% or more columns are zero, drop row
df_filtered = df[(df != 0).sum(axis=1) > threshold]

# Select important columns for signal analysis
important_columns = ['num_AND', 'num_OR', 'num_XOR', 'num_NOT', 'num_DFF', 'num_wire', 'num_reg', 'num_assign', 'Fan_In', 'Fan_Out', 'Signal_Depth', 'Circuit_Complexity_Score']
df_filtered = df_filtered[important_columns]

# Save cleaned dataset
df_filtered.to_csv('final_cleaned.csv', index=False)

print("✅ Final cleaned dataset saved successfully as final_cleaned.csv")

# Load the dataset
df = pd.read_csv("final1.csv")

# Select only the important columns
important_columns = [
    "__index_level_0__", "Fan_In", "Fan_Out", "Signal_Depth", "gate_activity", "reg_wire_ratio", "complexity"
]
df_refined = df[important_columns]

# Save the refined dataset
df_refined.to_csv("final_refined.csv", index=False)

print("✅ Refined dataset saved as 'final_refined.csv'!")
print(df_refined.head())  # Display the first few rows
