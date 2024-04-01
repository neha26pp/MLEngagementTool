from sklearn.linear_model import RANSACRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os
import sys

# Update the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Assuming EyeFeatureCalculator is correctly set up
from MLModel.Regression import EyeFeatureCalculator

print("Current working directory:", os.getcwd())

# Load and prepare data
trainingFolder = "EyeData"
features = EyeFeatureCalculator.run(trainingFolder)
features = np.array(features)

LabelFolder = "Scripts/MyQualtricsDownload/QuizScores"

labels = []
for file in os.listdir(LabelFolder):
    if file.endswith(".txt"):
        full_path = os.path.join(LabelFolder, file)
        with open(full_path, 'r') as f:
            file_values = [float(line.strip().replace('%', '')) for line in f.readlines()]
            labels.extend(file_values)

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Hyperparameter tuning
min_samples_options = [0.5, 0.6, 0.7, 0.8]
max_trials_options = [50, 100, 150, 200]
loss_options = ['absolute_error', 'squared_error']  # Corrected loss options

best_score = float('inf')
best_params = {}

for min_samples in min_samples_options:
    for max_trials in max_trials_options:
        for loss in loss_options:
            ransac = RANSACRegressor(min_samples=min_samples, max_trials=max_trials, loss=loss, random_state=42)
            ransac.fit(X_train, y_train)
            y_pred = ransac.predict(X_test)
            score = mean_squared_error(y_test, y_pred)
            
            if score < best_score:
                best_score = score
                best_params = {'min_samples': min_samples, 'max_trials': max_trials, 'loss': loss}

print("Best Hyperparameters:", best_params)
print("Best MSE:", best_score)

# Final training with the best parameters
ransac_regressor = RANSACRegressor(min_samples=best_params['min_samples'], max_trials=best_params['max_trials'], loss=best_params['loss'], random_state=42)
ransac_regressor.fit(X_train, y_train)
y_pred = ransac_regressor.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("MSE:", mse)
print("R^2:", r2)

# Visualization
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], y_test, color='blue', label='Actual Values')
plt.scatter(X_test[:, 0], y_pred, color='red', label='Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Feature Value')
plt.ylabel('Target Value')
plt.legend()
plt.show()

# Save the model
save_directory = "MLModel"
model_filename = os.path.join(save_directory, 'best_ransac_model.pkl')
joblib.dump(ransac_regressor, model_filename)
