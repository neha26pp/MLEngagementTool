import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import EyeFeatureCalculator

# create a 2d array
# call fucnttion calculate eye features from EyeFeatureCalculator class
features = EyeFeatureCalculator.run()


