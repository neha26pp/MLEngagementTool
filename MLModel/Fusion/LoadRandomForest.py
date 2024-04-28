import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import joblib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from MLModel.Regression import EyeFeatureCalculator
from MLModel.Fusion import EmotionPreprocessor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Define a function to load labels from txt files
def load_labels_from_txt(directory):
    labels = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            # Convert each line to float and remove the '%' sign before conversion
            labels.extend([float(line.strip().replace('%', '')) for line in file if line.strip()])
    return np.array(labels)

# Load the test labels
label_directory = 'C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\Scripts\\MyQualtricsDownload\\QuizScores'
y_test = load_labels_from_txt(label_directory)

# Load the model
model_directory = 'C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\MLModel\\Fusion'
model_filename = os.path.join(model_directory, 'best_random_forest_model.pkl')
model = joblib.load(model_filename)

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
X_test = np.concatenate((eyeFeatures, emotionFeatures), axis=1)

# Run the model on the test data
y_pred = model.predict(X_test)

# print predicted scores with name of file label is from
label_directory = 'C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\Scripts\\MyQualtricsDownload\\QuizScores'

print("Predicted Scores:")
index = 0  # Start an index at 0
for file_name in os.listdir(label_directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(label_directory, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                if index < len(y_pred):  # Check to prevent index out of range
                    print(f'{file_name}: {y_pred[index]}')
                    index += 1  # Increment the index

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'Mean Absolute Percentage Error: {mape}')
print(f'R^2 score: {r2}')

# Plot actual vs predicted values
plt.figure(figsize=(10, 5))
plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual Values')
plt.scatter(range(len(y_test)), y_pred, color='red', label='Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Sample Index')
plt.ylabel('Values')
plt.legend()
plt.grid(True)
plt.show()

# Plot residuals
residuals = y_test - y_pred
plt.figure(figsize=(10, 5))
plt.scatter(y_pred, residuals, color='green')
plt.axhline(0, color='black', lw=2)
plt.title('Residual Plot')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.grid(True)
plt.show()

# Plot learning curves
# Simulated training and validation errors (to be replaced with actual learning data in real usage)
train_sizes = np.linspace(0.1, 1.0, 10)
train_scores = np.exp(-train_sizes * np.random.rand(10))  # Exponential decay of training error
validation_scores = np.exp(-train_sizes * np.random.rand(10)) + 0.1  # Validation error

plt.figure(figsize=(10, 5))
plt.plot(train_sizes, train_scores, label='Training Error')
plt.plot(train_sizes, validation_scores, label='Validation Error')
plt.title('Learning Curves')
plt.xlabel('Training Set Size')
plt.ylabel('Error')
plt.legend()
plt.grid(True)
plt.show()