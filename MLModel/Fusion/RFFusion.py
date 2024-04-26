import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import EmotionPreprocessor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib
import random
import optuna

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from MLModel.Regression import EyeFeatureCalculator
from MLModel.Regression import SlidingWindow

print("Current working directory:", os.getcwd())

save_directory = "MLModel/Fusion"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

eyeDataFolder = "EyeData"
emotionDataFolder = "EmotionData"

# Load and prepare features
emotionFeatures = EmotionPreprocessor.EmotionPreprocess(emotionDataFolder)
eyeFeatures = EyeFeatureCalculator.run(eyeDataFolder)

# Ensure both are numpy arrays and have compatible shapes
eyeFeatures = np.array(eyeFeatures)
emotionFeatures = np.array(emotionFeatures)

assert eyeFeatures.shape[0] == emotionFeatures.shape[0], "Mismatch in number of samples between eye and emotion features"

# Concatenate eye and emotion features along the features axis
combinedFeatures = np.concatenate((eyeFeatures, emotionFeatures), axis=1)

# Load and prepare labels
LabelFolder = "Scripts/MyQualtricsDownload/QuizScores"
labels = []
for file in os.listdir(LabelFolder):
    full_path = os.path.join(LabelFolder, file)
    with open(full_path, 'r') as f:
        labels.extend([float(line.strip().replace('%', '')) for line in f.readlines()])

X_train, X_test, y_train, y_test = train_test_split(combinedFeatures, labels, test_size=0.2, random_state=42)

def objective(trial):
    # Suggest values for the hyperparameters
    params = {
        'n_estimators': trial.suggest_categorical('n_estimators', [10, 100, 1000, 2000, 5000, 7500, 10000, 15000]),
        'max_depth': trial.suggest_categorical('max_depth', [None, 100, 1000, 5000, 7500, 10000, 15000]),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 500, log=True),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 500, log=True),
        'max_features': trial.suggest_categorical('max_features', ['log2', 'sqrt']),
        'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
    }
    
    model = RandomForestRegressor(random_state=42, **params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    return r2

# Create a study object and specify the direction of the optimization
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Results
print("Best trial:")
trial = study.best_trial

print("  Value: ", trial.value)
print("  Params: ")
for key, value in trial.params.items():
    print(f"    {key}: {value}")
    
# Save the best model
best_model = RandomForestRegressor(random_state=42, **trial.params)
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

model_filename = os.path.join(save_directory, 'random_forest_model.pkl')
joblib.dump(best_model, model_filename)
    
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual Values')
plt.scatter(range(len(y_test)), y_pred, color='red', label='Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Sample index')
plt.ylabel('Engagement Percentage')
plt.legend()
plt.show()

