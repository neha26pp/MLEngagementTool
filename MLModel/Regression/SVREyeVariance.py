import os
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, median_absolute_error
from scipy.stats import uniform, reciprocal
from joblib import dump, load
from Scripts.DataLoad import DataLoad
from Scripts.DataPreprocessor import DataNormalization


# Step 1: Load Data and Get normalized variance
dataframes = DataLoad.readCSVFromSubDir("../../EyeData", isDataFrame=True)
normalized_variances = DataNormalization.calculateNormalizedVariances(dataframes)
print(normalized_variances)

# Step 2: Prepare training data
X = np.array(normalized_variances).T
y = DataLoad.readLabels("/../../Scripts/MyQualtricsDownload/QuizScores")
print(len(X), len(y))

# Step 3: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Split datasets")

# Step 4: Define the hyperparameter ranges to explore
param_dist = {
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
    'C': reciprocal(0.1, 100),
    'gamma': uniform(0.01, 10),
    # 'epsilon': [0.1, 0.01, 0.001]
}

# Step 5: Create SVR model and RandomizedSearchCV obj
svr = SVR()
random_search = RandomizedSearchCV(svr, param_distributions=param_dist, n_iter=50, cv=5,
                                   scoring='neg_mean_squared_error', n_jobs=1, random_state=42)
print("Train the model")
random_search.fit(X_train, y_train)
print("Best Parameters: ", random_search.best_params_)

# Step 6: Output and Save the best model
best_svr = random_search.best_estimator_
dump(best_svr, 'best_svr_eye_variance.joblib')

# Step 7: Load and Evaluate the model
loaded_model = load('best_svr_eye_variance.joblib')
y_pred = loaded_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mee = median_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Best svr")
print("Mean Squared Error: {:2f}".format(mse))
print("Median Absolute Error: {:2f}".format(mee))
print("R2 score: {:2f}".format(r2))

# Step 8: Load the model for prediction
# Load the model from file
# loaded_model = load('model.joblib')
# y_new = loaded_model.predict(X_new)

'''Output:
Best Parameters:  {'C': 0.35498788321965025, 'gamma': 3.052422429595377, 'kernel': 'poly'}
Mean Squared Error: 30.244103
Median Absolute Error: 5.063471
R2 score: 0.000053
'''
