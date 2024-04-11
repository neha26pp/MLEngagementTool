import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from MLModel.Regression import EyeFeatureCalculator

print("Current working directory:", os.getcwd())

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
param_grid = {
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

dt = DecisionTreeRegressor(random_state=42)

grid_search = GridSearchCV(estimator=dt, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)

grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
best_score = grid_search.best_score_

# Print the best hyperparameters
print(f"Best Hyperparameters: {best_params}")
print(f"Best Score (neg MSE): {best_score}")

# Train the Decision Tree with the best parameters
best_dt = DecisionTreeRegressor(**best_params, random_state=42)
best_dt.fit(X_train, y_train)

y_pred = best_dt.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("MSE:", mse)
print("R^2:", r2)

plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], y_test, color='blue', label='Actual Values')
plt.scatter(X_test[:, 0], y_pred, color='red', label='Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Feature Value')
plt.ylabel('Target Value')
plt.legend()
plt.show()

save_directory = "MLModel"
model_filename = os.path.join(save_directory, 'best_decision_tree_model.pkl')
joblib.dump(best_dt, model_filename)
