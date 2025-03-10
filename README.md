# Signal Depth Analyzer

## Overview
Signal Depth Analyzer is an AI-based tool designed to predict the combinational logic depth of signals in RTL (Register Transfer Level) designs. Traditional timing analysis requires full synthesis runs, which can be time-consuming. This project leverages machine learning to estimate logic depth and identify potential timing violations early in the design cycle, providing a faster alternative for hardware engineers and RTL designers.

## Features Extracted
- **Signal Information:** Extracted from Verilog designs.
- **Structural Complexity:** Fan-in, Fan-out, and Combinational Depth.
- **Feature Engineering:** Selected key features relevant to timing analysis.
- **Dataset Creation:** Synthesized Verilog designs and extracted signal properties.
- **ML Model Training:** Trained an AI model to predict signal depth based on extracted features.

### Extracted Features & Their Impact on Signal Depth
| Feature | Description | Impact on Signal Depth |
|---------|-------------|-----------------------|
| **num_pub_wire_bits** | Total bit-width of publicly accessible wires | Higher bit-width can indicate more complex interconnections |
| **Fan-out** | Number of outputs driven by a signal | Higher fan-out can increase propagation delay |
| **num_pub_wires** | Number of publicly accessible wires | More public wires can indicate increased signal interactions |
| **num_cells** | Number of logic cells (gates, flip-flops) | More cells increase logic complexity |
| **num_wires** | Total number of wires in the design | More wires indicate greater interconnect complexity |
| **num_wire_bits** | Total bit-width of all wires | Higher bit-width can contribute to timing delays |
| **num_processes** | Number of always/process blocks in RTL | More processes may introduce additional pipeline stages |
| **Fan-in** | Number of inputs feeding into a gate/module | Higher fan-in can lead to increased signal depth |
| **Signal Type** | Name of the signal/module in the Verilog file | Can determine signal classification and role |

## Workflow
### 1. Data Collection & Processing
- Extracted RTL design information from Verilog files.
- Ran Yosys synthesis to obtain combinational depth reports.
- Created a structured dataset with relevant signal features.

### 2. Feature Engineering & Cleaning
- Selected key features such as Fan-In, Fan-Out, and Signal Type.
- Removed redundant columns (e.g., num_memories, num_memory_bits).

### 3. Machine Learning Model
- Explored multiple regression models.
- Compared models based on accuracy and performance.
- Trained and tested an optimized ML model for prediction.

### 4. Model Evaluation
- Split dataset into training and testing sets.
- Evaluated model performance using:
  - **Mean Absolute Error (MAE):** 0.24
  - **R² Score:** 0.98 (indicating excellent model fit)

## Dataset
**Data Sources:**
The dataset was constructed using open-source Verilog designs from the following repositories:
- [100 Days of RTL](https://github.com/ekb0412/100DaysofRTL)
- [Sky130 RTL Design and Synthesis Workshop](https://github.com/kunalg123/sky130RTLDesignAndSynthesisWorkshop)
- [Verilog Design Examples](https://github.com/snbk001/Verilog-Design-Examples/tree/main/Half%20Adder)

### Output Files
## Output Files

- **yosys_full_dataset.csv** – Extracted dataset from one of the repositories.  
- **yosys_full_dataset1.csv** – Extracted dataset from the second repository.  
- **yosys_full_dataset2.csv** – Extracted dataset from the third repository.  
- **yosys_full_dataset4.csv** – Extracted dataset from the fourth repository.  
- **combinational_depth_model.pkl** – Trained machine learning model, which can be loaded using:  
  ```python
  model = joblib.load('combinational_depth_model.pkl')

[yosys_full_dataset.csv](https://github.com/user-attachments/files/19167858/yosys_full_dataset.csv)

[yosys_full_dataset1.csv](https://github.com/user-attachments/files/19167886/yosys_full_dataset1.csv)

[yosys_full_dataset2.csv](https://github.com/user-attachments/files/19167891/yosys_full_dataset2.csv)

[yosys_full_dataset4.csv](https://github.com/user-attachments/files/19167897/yosys_full_dataset4.csv)


## Dependencies
- Python
- Pandas
- NumPy
- scikit-learn
- Yosys (for synthesis)




## Usage
1. Ensure Yosys is installed and configured.
2. Run the dataset extraction script to process Verilog files.
3. Execute the feature extraction and engineering module.
4. Train and evaluate the ML model.

## Code Complexity
### 1. Logical Complexity
- Feature Extraction: Identifies signals, logic gates, and circuit structures.
- Graph-Based Analysis: Computes Fan-In, Fan-Out, and Combinational Depth.
- ML Model: Predicts signal depth using regression models.

### 2. Computational Complexity
| Operation | Complexity |
|-----------|-------------|
| File Traversal (os.walk) | O(F) (F = number of Verilog files) |
| Running Yosys (subprocess) | O(F × N) (N = number of logic elements) |
| Parsing JSON (json.load) | O(F × J) (J = size of JSON output) |
| Constructing DataFrame (pandas.DataFrame) | O(F) |
| ML Model Training (Random Forest) | O(n log n) (n = number of samples) |

### 3. Overall Complexity
- Feature Extraction & Parsing: **O(n)**
- Graph Processing: **O(V + E)** (V = signals, E = dependencies)
- Machine Learning Model Training: **O(n log n)**



## Conclusion
The **Signal Depth Analyzer** provides a fast and efficient way to predict combinational depth in RTL designs, enabling early detection of potential timing violations. Future improvements include:
- Expanding the dataset with more complex Verilog designs.
- Optimizing feature selection for better accuracy.
- Exploring deep learning models for improved generalization.



## Conclusion
This pipeline enables efficient extraction and analysis of Verilog designs, facilitating circuit complexity prediction and RTL optimization.

