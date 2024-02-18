import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import EyeFeatureCalculator
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

# create a 2d array
trainingFolder = "EyeData"
features = EyeFeatureCalculator.run(trainingFolder)

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

svr = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
svr.fit(features, labels)

testFolder = "MLModel/EyeTestDataSet"  # Adjust this path as necessary

testFeatures = EyeFeatureCalculator.run(testFolder)

# Convert testFeatures to a numpy array for consistent handling by sklearn
testFeatures = np.array(testFeatures)

testPredictions = svr.predict(testFeatures)
print("Predictions: ", testPredictions)
