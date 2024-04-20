import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..')))
from MLModel.Regression import EyeFeatureCalculator
from MLModel.Regression import SlidingWindow
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Print the current working directory
print("Current working directory:", os.getcwd())

# Load the saved model from file
#svr = joblib.load('MLModel/svr_model.pkl')

# create a 2d array
trainingFolder = "EyeData"
features = EyeFeatureCalculator.run(trainingFolder)
# features = SlidingWindow.run(trainingFolder)
features = np.array(features)

LabelFolder = "Scripts/MyQualtricsDownload/QuizScores"  # Adjust this path as necessary

labels = []
for file in os.listdir(LabelFolder):
    if file.endswith(".txt"):
        full_path = os.path.join(LabelFolder, file)
        # print("Reading file: ", full_path)
        with open(full_path, 'r') as f:
            # Read each line, remove the percent symbol, and convert to float
            file_values = [float(line.strip().replace('%', '')) for line in f.readlines()]
            labels.extend(file_values)  # Use extend to add all values in the list

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Define the hyperparameter ranges to explore
param_grid = {
    'kernel': ['linear', 'poly', 'rbf'],
    'C': [0.1, 1, 10, 100],
    'gamma': [0.1, 1, 10],
    'epsilon': [0.1, 0.01, 0.001]
}

best_score = -np.inf
best_params = None

# Iterate through different combinations of hyperparameters
for kernel in param_grid['kernel']:
    for C in param_grid['C']:
        for gamma in param_grid['gamma']:
            for epsilon in param_grid['epsilon']:
                # Initialize and train the SVR model
                svr = SVR(kernel=kernel, C=C, gamma=gamma, epsilon=epsilon)
                svr.fit(X_train, y_train)

                # Make predictions on the test set
                y_pred = svr.predict(X_test)

                # Calculate the model performance metrics
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                score = r2  # You can choose another metric if desired

                # Check if this combination of hyperparameters yields a better score
                if score > best_score:
                    best_score = score
                    best_params = {'kernel': kernel, 'C': C, 'gamma': gamma, 'epsilon': epsilon}

# Print the best hyperparameters and corresponding score
print("Best Hyperparameters:", best_params)
print("Best Score:", best_score)

# Visualization: Plot actual vs. predicted values for the test set
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], y_test, color='blue', label='Actual Values')  # Adjust if more than one feature
plt.scatter(X_test[:, 0], y_pred, color='red', label='Predicted Values')  # Adjust if more than one feature
plt.title('Actual vs. Predicted Values')
plt.xlabel('Feature Value')
plt.ylabel('Target Value')
plt.legend()
plt.show()

# Specify the directory where you want to save the model
save_directory = "MLModel"

# Save the trained model to a file in the specified directory
#model_filename = os.path.join(save_directory, 'svr_model.pkl')
#joblib.dump(svr, model_filename)

#testFolder = "MLModel/EyeTestDataSet"  # Adjust this path as necessary