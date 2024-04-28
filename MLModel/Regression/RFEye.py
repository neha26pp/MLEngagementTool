import os
from matplotlib import pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import random
import optuna

# Assuming EyeFeatureCalculator and SlidingWindow are defined in the imported modules
import EyeFeatureCalculator
import SlidingWindow

print("Current working directory:", os.getcwd())

save_directory = "MLModel/Regression"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Load and prepare the data
trainingFolder = "EyeData"
features = EyeFeatureCalculator.run(trainingFolder)
features = np.array(features)

labelFolder = "C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\Scripts\\MyQualtricsDownload\\QuizScores"
labels = []
for file in os.listdir(labelFolder):
    with open(os.path.join(labelFolder, file), 'r') as f:
        labels.extend([float(line.strip().replace('%', '')) for line in f.readlines()])

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

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

model_filename = os.path.join(save_directory, 'best_random_forest_model.pkl')
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
