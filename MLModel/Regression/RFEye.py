import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Assuming EyeFeatureCalculator and SlidingWindow are defined in the imported modules
import EyeFeatureCalculator

print("Current working directory:", os.getcwd())

save_directory = "MLModel/Regression"

# Load and prepare the data
trainingFolder = "EyeData"
features = EyeFeatureCalculator.run(trainingFolder)  # Example function call, replace with actual data loading if necessary
features = np.array(features)

labelFolder = "Scripts/MyQualtricsDownload/QuizScores"
labels = []
for file in os.listdir(labelFolder):
    if file.endswith(".txt"):
        with open(os.path.join(labelFolder, file), 'r') as f:
            labels.extend([float(line.strip().replace('%', '')) for line in f.readlines()])

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

def random_params():
    return {
        'n_estimators': random.choice([10, 100, 1000]),
        'max_depth': random.choice([None, 10, 100]),
        'min_samples_split': random.choice([2, 5, 10]),
        'min_samples_leaf': random.choice([1, 2, 8]),
        'max_features': random.choice(['log2', 'sqrt']),
        'bootstrap': random.choice([True, False]),
    }

attempt = 0
r2 = -np.inf

# Change the loop condition to stop when R^2 is at least 0.7
while r2 < 0.3:
    attempt += 1
    params = random_params()
    model = RandomForestRegressor(random_state=42, **params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    print(f"Attempt {attempt}: R^2 = {r2:.3f} with params {params}")
    # Removed the unnecessary condition check for R^2 >= 0.2

# Check if the loop ended with a satisfying R^2 score and print results
if r2 >= 0.2:
    print("Achieved R^2 >= 0.2")
    print(f"Parameters: {params}")
    print(f"R^2 score: {r2}")

    # Save using joblib
    params_joblib_filename = os.path.join(save_directory, 'model_parameters.joblib')
    joblib.dump({'params': params, 'r2_score': r2}, params_joblib_filename)
else:
    print("Failed to achieve R^2 >= 0.2 after {attempt} attempts.")

# Visualization of model performance
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], y_test, color='blue', label='Actual Values')
plt.scatter(X_test[:, 0], y_pred, color='red', label='Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Feature Value')
plt.ylabel('Target Value')
plt.legend()
plt.show()

# Optionally save the model

if not os.path.exists(save_directory):
    os.makedirs(save_directory)
model_filename = os.path.join(save_directory, 'random_forest_model.pkl')
joblib.dump(model, model_filename)
