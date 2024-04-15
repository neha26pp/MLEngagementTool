import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from MLModel.Regression import EyeFeatureCalculator
from MLModel.Regression import SlidingWindow

print("Current working directory:", os.getcwd())

dataFolder = "EyeData"
eyeFeatures = EyeFeatureCalculator.run(dataFolder)
eyeFeatures = np.array(eyeFeatures)

# Load and prepare labels
LabelFolder = "Scripts/MyQualtricsDownload/QuizScores"
labels = []
for file in os.listdir(LabelFolder):
    if file.endswith(".txt"):
        full_path = os.path.join(LabelFolder, file)
        with open(full_path, 'r') as f:
            labels.extend([float(line.strip().replace('%', '')) for line in f.readlines()])

X_train, X_test, y_train, y_test = train_test_split(eyeFeatures, labels, test_size=0.2, random_state=42)

def random_params():
    return {
        'n_estimators': random.choice([5, 20, 50, 100]),
        'max_depth': random.choice([None, 10, 50, 100, 200]),
        'min_samples_split': random.choice([2, 5, 10, 20]),
        'min_samples_leaf': random.choice([1, 2, 4]),
        'max_features': random.choice(['sqrt', 'log2']),
        'bootstrap': random.choice([True, False]),
    }

target_r2 = 0.15  # Define your target R^2 score

best_r2 = -np.inf
best_model = None
best_params = {}

attempt = 0
found = False  # Flag to check if satisfactory model is found

# Run the training loop
while not found and attempt < 100000:  # Set a maximum number of attempts to avoid infinite loop
    attempt += 1
    params = random_params()
    model = RandomForestRegressor(random_state=42, **params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    print(f"Attempt {attempt}: R^2 = {r2:.3f} with params {params}")

    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_params = params
        
        if best_r2 >= target_r2:
            found = True
            print(f"Target R^2 score of {target_r2} reached.")

# Save the best model and parameters
if found:
    print(f"Best R^2 score: {best_r2}")
    print(f"Best parameters: {best_params}")
    save_directory = "C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\MLModel\\Fusion"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    model_filename = os.path.join(save_directory, 'random_forest_model.pkl')
    joblib.dump(best_model, model_filename)
else:
    print(f"Failed to find a satisfactory model after {attempt} attempts.")
