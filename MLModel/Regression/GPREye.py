import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from MLModel.Regression import EyeFeatureCalculator
from MLModel.Regression import SlidingWindow

# Assuming EyeFeatureCalculator and the dataset preparation steps are defined elsewhere
# Load your dataset
trainingFolder = "EyeData"
#features = EyeFeatureCalculator.run(trainingFolder)
features = SlidingWindow.run(trainingFolder)
features = np.array(features)

LabelFolder = "Scripts/MyQualtricsDownload/QuizScores"
labels = []
for file in os.listdir(LabelFolder):
    if file.endswith(".txt"):
        full_path = os.path.join(LabelFolder, file)
        with open(full_path, 'r') as f:
            file_values = [float(line.strip().replace('%', '')) for line in f.readlines()]
            labels.extend(file_values)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Hyperparameter tuning
constant_values = [1.0, 2.0, 3.0]
length_scale_values = [1.0, 10.0, 100.0]
alpha_values = [1e-2, 1e-3, 1e-4]

best_score = float("-inf")
best_params = {'constant_value': None, 'length_scale': None, 'alpha': None}

for constant_value in constant_values:
    for length_scale in length_scale_values:
        for alpha in alpha_values:
            kernel = C(constant_value, (1e-3, 1e3)) * RBF(length_scale, (1e-2, 1e2))
            gpr = GaussianProcessRegressor(kernel=kernel, alpha=alpha, n_restarts_optimizer=10, normalize_y=True)
            gpr.fit(X_train, y_train)
            score = gpr.log_marginal_likelihood_value_
            if score > best_score:
                best_score = score
                best_params['constant_value'] = constant_value
                best_params['length_scale'] = length_scale
                best_params['alpha'] = alpha

print(f"Best Parameters: Constant Value: {best_params['constant_value']}, Length Scale: {best_params['length_scale']}, Alpha: {best_params['alpha']}")


# Initialize and train the GPR with the best kernel
best_kernel = C(best_params['constant_value'], (1e-3, 1e3)) * RBF(best_params['length_scale'], (1e-2, 1e2))
gpr = GaussianProcessRegressor(kernel=best_kernel, alpha=best_params['alpha'], n_restarts_optimizer=10, normalize_y=True)
gpr.fit(X_train, y_train)

# Make predictions on the test set
y_pred, std_dev = gpr.predict(X_test, return_std=True)

# Calculate the model performance metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MSE:", mse)
print("R^2:", r2)

# Visualization: Plot actual vs. predicted values for the test set
plt.figure(figsize=(10, 6))
plt.errorbar(X_test[:, 0], y_pred, yerr=std_dev, fmt='o', color='red', label='Predictions with Uncertainty')
plt.scatter(X_test[:, 0], y_test, color='blue', label='Actual Values')
plt.title('Actual vs. Predicted Values with Uncertainty')
plt.xlabel('Feature Value')
plt.ylabel('Target Value')
plt.legend()
plt.show()

# Saving the model, adjust the directory as needed
save_directory = "MLModel"
model_filename = os.path.join(save_directory, 'gpr_model.pkl')
joblib.dump(gpr, model_filename)