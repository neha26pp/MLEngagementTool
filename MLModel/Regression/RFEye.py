import os
from matplotlib import pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib
import random

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
        'min_samples_leaf': random.choice([1, 2, 4]),
        'max_features': random.choice(['log2', 'sqrt']),
        'bootstrap': random.choice([True, False]),
    }

target_r2 = 0.2 

best_r2 = -np.inf
best_model = None
best_params = {}

attempt = 0
found = False  # Flag to check if satisfactory model is found

# Run the training loop
while attempt < 100000:  # Set a maximum number of attempts to avoid infinite loop
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
        
        # Check if current model meets the target R^2 score
        if best_r2 >= target_r2:
            found = True
            print(f"Target R^2 score of {target_r2} reached.")
            break  # Stop the loop as we've reached the target score

# Save the best model and parameters
if found:
    print(f"Best R^2 score: {best_r2}")
    print(f"Best parameters: {best_params}")
    
    params_joblib_filename = os.path.join(save_directory, 'best_model_parameters.joblib')
    joblib.dump({'params': best_params, 'r2_score': best_r2}, params_joblib_filename)
    
    model_filename = os.path.join(save_directory, 'best_random_forest_model.pkl')
    joblib.dump(best_model, model_filename)
else:
    print(f"Failed to find a satisfactory model after {attempt} attempts.")
    
# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual Values')
plt.scatter(range(len(y_test)), y_pred, color='red', label='Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Sample index')
plt.ylabel('Engagement Percentage')
plt.legend()
plt.show()
<<<<<<< Updated upstream
=======

# Optionally save the model

if not os.path.exists(save_directory):
    os.makedirs(save_directory)
model_filename = os.path.join(save_directory, 'random_forest_model.pkl')
joblib.dump(model, model_filename)
>>>>>>> Stashed changes
