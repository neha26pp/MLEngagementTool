import os
import numpy as np
import matplotlib.pyplot as plt
import joblib
import EyeFeatureCalculator
from sklearn.metrics import r2_score

# Define a function to load labels from txt files
def load_labels_from_txt(directory):
    labels = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                # Convert each line to float and remove the '%' sign before conversion
                labels.extend([float(line.strip().replace('%', '')) for line in file if line.strip()])
    return np.array(labels)

# Load the test labels
label_directory = 'C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\Scripts\\MyQualtricsDownload\\QuizScores'
y_test = load_labels_from_txt(label_directory)

# Load the model
model_directory = 'C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\MLModel\\Regression'
model_filename = os.path.join(model_directory, 'random_forest_model.pkl')
model = joblib.load(model_filename)

# Assuming that the features for the test set are available in the same format as the training set
X_test = EyeFeatureCalculator.run('C:\\Users\\Anthraxlemonaid\\VSCode\\MLEngagementTool\\EyeData')  # Replace with actual feature loading

# Run the model on the test data
y_pred = model.predict(X_test)

# Calculate the R^2 score
r2 = r2_score(y_test, y_pred)
print(f'R^2 score: {r2}')

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

# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_test)), y_test, color='blue', label='Actual Values')
plt.scatter(range(len(y_test)), y_pred, color='red', label='Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.xlabel('Sample index')
plt.ylabel('Engagement Percentage')
plt.legend()
plt.show()