import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from MLModel.Regression import EyeFeatureCalculator
from MLModel.Regression import SlidingWindow
import EmotionPreprocessor

# Print the current working directory
print("Current working directory:", os.getcwd())

dataFolder = "EyeData"
#eyeFeatures = EyeFeatureCalculator.run(trainingFolder)
eyeFeatures = SlidingWindow.run(dataFolder)
eyeFeatures = np.array(eyeFeatures)

emotionFeatures = EmotionPreprocessor.EmotionPreprocess(dataFolder)
emotonFeatures = np.array(emotionFeatures)

combinedFeatures = np.concatenate((eyeFeatures, emotionFeatures), axis=1)
LabelFolder = "Scripts/MyQualtricsDownload/QuizScores"

labels = []
for file in os.listdir(LabelFolder):
    if file.endswith(".txt"):
        full_path = os.path.join(LabelFolder, file)
        with open(full_path, 'r') as f:
            file_values = [float(line.strip().replace('%', '')) for line in f.readlines()]
            labels.extend(file_values)

X_train, X_test, y_train, y_test = train_test_split(combinedFeatures, labels, test_size=0.2, random_state=42)

# Define hyperparameter space
param_grid = {
    'n_estimators': [5, 20, 50, 100],
    'max_depth': [None, 10, 50, 100, 200],
    'min_samples_split': [2, 5, 10, 20],
}

# Initialize the Random Forest Regressor
rf = RandomForestRegressor(random_state=42)

# Initialize GridSearchCV
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)
# Define the directory where you want to save your results and model
save_directory = "MLModel"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Your GridSearchCV fitting and results saving logic
grid_search.fit(X_train, y_train)

results = pd.DataFrame(grid_search.cv_results_)
results_filename = os.path.join(save_directory, 'grid_search_results.csv')
results.to_csv(results_filename, index=False)

# Continue with your logic for finding the best parameters, retraining, and saving the model
best_params = grid_search.best_params_
best_score = grid_search.best_score_
print(f"Best Score (neg MSE): {best_score}")

best_rf = RandomForestRegressor(**best_params, random_state=42)
best_rf.fit(X_train, y_train)

# Saving the model
model_filename = os.path.join(save_directory, 'best_random_forest_fusion_model.pkl')
joblib.dump(best_rf, model_filename)

# Make predictions with the best model
y_pred = best_rf.predict(X_test)

# Calculate and print performance metrics
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

# Save the model, if needed
save_directory = "MLModel"
model_filename = os.path.join(save_directory, 'best_random_forest_model.pkl')
joblib.dump(best_rf, model_filename)