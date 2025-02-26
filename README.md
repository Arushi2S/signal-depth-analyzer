[final.csv](https://github.com/user-attachments/files/18977579/final.csv)# signal-depth-analyzer
obtained dataset
# Verilog Code Analysis and Complexity Prediction

## Overview
This project extracts features from Verilog code to analyze signal complexity, combinational depth, and timing violations. The dataset undergoes multiple stages of processing, including feature extraction, graph-based analysis, and machine learning-based prediction.

## Features Extracted
1. **Logic Gate Usage:** Count of AND, OR, XOR, NOT gates, and D flip-flops (DFFs).
2. **Signal Information:** Number of wires, registers, and assignments.
3. **Structural Complexity:** Fan-in, Fan-out, signal depth.
4. **Behavioral Constructs:** Count of always blocks, loops, and conditionals.
5. **Circuit Complexity Score:** Weighted combination of logic gate counts.
6. **Feature Engineering:** Gate activity, register-to-wire ratio, log-transformed signal depth.

## Workflow
1. **Dataset Loading**
   - Loads a Verilog dataset from `hf://datasets/ahmedallam/RTL-Repo/`.
   - Extracts Verilog features using regular expressions.
   - Computes fan-in, fan-out, and logic depth.
   - Saves processed data to CSV and Parquet formats.

2. **Graph-Based Signal Analysis**
   - Loads dataset into NetworkX.
   - Constructs a directed graph from `source` and `destination` signals.
   - Computes fan-in, fan-out, and longest signal path.
   - Saves updated dataset with additional graph features.

3. **Feature Engineering & Cleaning**
   - Normalizes logic gate activity.
   - Computes register-to-wire ratio.
   - Computes circuit complexity score.
   - Log-transforms signal depth.
   - Filters out rows with excessive zero values.
   - Saves cleaned dataset as `final_cleaned.csv`.

4. **Machine Learning Model**
   - Uses `RandomForestRegressor` to predict circuit complexity.
   - Features: Fan-in, Fan-out, Signal Depth, Gate Activity, Register-to-Wire Ratio.
   - Trains on 80% of the dataset, tests on 20%.
   - Evaluates performance using MAE, MSE, and R² score.

## Dependencies
- Python
- Pandas
- NumPy
- NetworkX
- Scikit-learn
- Regular Expressions (re)

## Usage
1. Ensure the dataset path is correctly set.
2. Run the feature extraction script.
3. Execute the graph-based analysis module.
4. Perform feature engineering and save the dataset.
5. Train and evaluate the ML model.

## Output Files
- `analyzing_dataset.parquet` / `analyzing_dataset.csv` – Extracted Verilog features.
- `final_cleaned.csv` – Processed dataset with engineered features.
- `final_refined.csv` – Dataset for ML model.
- `final1.csv` – Feature-enhanced dataset.


## Model Performance Metrics
- **MAE (Mean Absolute Error)** – Measures average prediction error.
- **MSE (Mean Squared Error)** – Penalizes large errors.
- **R² Score** – Measures how well the model explains variance.

## Code Complexity

### **1. Logical Complexity**
The code processes Verilog files to extract design-related features and predict combinational complexity. Key logical operations include:
- **Feature Extraction**: Uses regular expressions to identify signals, logic gates, and circuit structures.
- **Graph Construction**: Creates a directed graph where nodes represent signals and edges represent dependencies.
- **Metric Computation**: Determines fan-in, fan-out, and combinational depth for each signal.
- **Machine Learning Model**: Trains a regression model to predict circuit complexity based on extracted features.

### **2. Computational Complexity**
The computational complexity of major operations is analyzed below:

| Operation | Complexity |
|-----------|------------|
| Regex-based feature extraction | O(n) (where n is the file size) |
| Graph construction (adding edges) | O(V + E) (where V is signals and E is dependencies) |
| Longest path calculation in DAG | O(V + E) |
| Random Forest training | O(n log n) (where n is the number of samples) |
| Data preprocessing (scaling, splitting) | O(n) |

### **3. Overall Complexity**
- **Feature extraction & parsing**: O(n)
- **Graph processing**: O(V + E)
- **Machine learning model training**: O(n log n)

### **4. Complexity Category**
- **Moderate to High Complexity** due to a mix of **text processing, graph analysis, and machine learning**.
- The most computationally expensive operations are **graph-based depth calculations** and **RandomForestRegressor training**.
- Optimization strategies may include caching, parallel processing, or reducing redundant operations.

---
This complexity analysis provides insights into performance bottlenecks and areas for improvement in the codebase.

## Conclusion
This pipeline enables efficient extraction and analysis of Verilog designs, facilitating circuit complexity prediction and RTL optimization.

