import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import EyeFeatureCalculator
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# create a 2d array
trainingFolder = "EyeData"
features = EyeFeatureCalculator.run(trainingFolder)
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

# Initialize and train the SVR model on the training set
svr = SVR(kernel='poly', C=100, gamma=0.1, epsilon=0.1) # poly seems to be the best for default values
svr.fit(X_train, y_train)

# Make predictions on the test set
y_pred = svr.predict(X_test)

# Calculate and print the model performance metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Visualization: Plot actual vs. predicted values for the test set
plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], y_test, color='blue', label='Actual Values')  # Adjust if more than one feature
plt.scatter(X_test[:, 0], y_pred, color='red', label='Predicted Values')  # Adjust if more than one feature
plt.title('Actual vs. Predicted Values')
plt.xlabel('Feature Value')
plt.ylabel('Target Value')
plt.legend()
plt.show()

#testFolder = "MLModel/EyeTestDataSet"  # Adjust this path as necessary
