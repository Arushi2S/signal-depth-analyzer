import pandas as pd
import joblib  # For loading the model

# Load the pre-trained model
model = joblib.load('combinational_depth_model.pkl')

# Define sample input (excluding irrelevant columns)
sample_input = {
    'num_pub_wires': [10],
    'num_pub_wire_bits': [13],
    'num_cells': [13],
    'Fan-out': [339],
    'num_wires': [32],
    'num_processes': [1],
    'num_wire_bits': [339],
    'Fan-in': [10]
} 

# Convert input to DataFrame
df_input = pd.DataFrame(sample_input)

# Function to preprocess input data
def preprocess_input(input_data):
    # Get feature names from the trained model
    model_columns = model.feature_names_in_
    
    # Identify missing columns
    missing_columns = [col for col in model_columns if col not in input_data.columns]
    missing_data = pd.DataFrame(0, columns=missing_columns, index=input_data.index)
    
    # Concatenate missing columns and reorder
    input_data = pd.concat([input_data, missing_data], axis=1)
    input_data = input_data[model_columns]
    
    return input_data

# Preprocess the input
processed_input = preprocess_input(df_input)

# Predict combinational depth
predicted_depth = model.predict(processed_input)

# Output the result
print("Predicted Combinational Depth:", predicted_depth[0])

#Predicted Combinational Depth: 13.06, The model is predicting a combinational depth close to the actual value (13)
