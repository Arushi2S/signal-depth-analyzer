import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  # Using Regressor since "Combinational Depth" is continuous
from sklearn.metrics import mean_absolute_error, r2_score

# Step 1: Load the datasets with a specified encoding
df1 = pd.read_csv("C:/Users/Ashish Soti/Desktop/mazedar/yosys_full_dataset.csv", encoding='ISO-8859-1')
df2 = pd.read_csv("C:/Users/Ashish Soti/Desktop/mazedar/yosys_full_dataset1.csv", encoding='ISO-8859-1')
df3 = pd.read_csv("C:/Users/Ashish Soti/Desktop/mazedar/yosys_full_dataset2.csv", encoding='ISO-8859-1')
df4 = pd.read_csv("C:/Users/Ashish Soti/Desktop/signal depth/yosys_full_dataset4.csv", encoding='ISO-8859-1')

# Step 2: Combine the datasets into one
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Step 3: Preprocess the data
# Drop unintended columns 'num_memories', 'num_memory_bits', and 'File'
df = df.drop(['num_memories', 'num_memory_bits', 'File'], axis=1)

# Separate features (X) and target (y)
X = df.drop('Combinational Depth', axis=1)  # Features
y = df['Combinational Depth']  # Target variable

# Handle categorical columns like 'Signal Type' (example using one-hot encoding)
X = pd.get_dummies(X, columns=['Signal Type'], drop_first=True)

# Step 4: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train a Random Forest Regressor (for continuous target)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Step 6: Predict on the test set
y_pred = model.predict(X_test)

# Step 7: Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Output results
print(f"Model Mean Absolute Error: {mae:.2f}")
print(f"Model R-squared: {r2:.2f}")

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# Assuming 'df' is your dataset, and 'X' and 'y' are your features and target
model = RandomForestRegressor()
model.fit(X, y)  # Train the model

# Save the model to a file
with open('combinational_depth_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
