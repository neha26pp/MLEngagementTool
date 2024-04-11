import os
import csv
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def sliding_window_function(csv_data, window_size, step_size, function_to_apply):
    results = []
    for start in range(1, len(csv_data) - window_size + 1, step_size):  # Skip header row with start=1
        window = csv_data[start:start + window_size]
        result = function_to_apply(window)
        results.append(result)
    return results

def getAvgGazeLAOI_sliding_window(csv_window):
    SumLAOI = 0
    rowCount = 0
    for row in csv_window:
        LAOI = int(row[6])
        SumLAOI += LAOI
        rowCount += 1

    avgLAOI = SumLAOI / rowCount if rowCount > 0 else 0
    return avgLAOI

def getAvgBlinkLatency_sliding_window(csv_window):
    sumLatency, count = 0, 0
    for row in csv_window:
        try:
            value = float(row[25])
            if value > 0.7:  
                sumLatency += value
                count += 1
        except ValueError:
            continue
    avgLatency = sumLatency / count if count else 0
    return avgLatency 

def getMeanPupilSize_L_sliding_window(csv_window):
    sumPupilSize, rowCount = 0, 0
    for row in csv_window:
        try:
            sumPupilSize += (float(row[13]) * float(row[15]) * math.pi)
            rowCount += 1
        except ValueError:
            continue
    avgPupilSize = sumPupilSize / rowCount if rowCount else 0
    return avgPupilSize

def getMeanPupilSize_R_sliding_window(csv_window):
    sumPupilSize, rowCount = 0, 0
    for row in csv_window:
        try:
            sumPupilSize += (float(row[14]) * float(row[16]) * math.pi)
            rowCount += 1
        except ValueError:
            continue
    avgPupilSize = sumPupilSize / rowCount if rowCount else 0
    return avgPupilSize 

def getAvgFixationDuration_sliding_window(csv_window):
    fixationDurations = []
    fixationStartTime = None
    originHorzGazeCoord, originVertGazeCoord = None, None
    
    for row in csv_window:
        if not row:  # Skip empty rows
            continue

        currentTime = float(row[0])
        currentHorzGazeCoord = float(row[38])
        currentVertGazeCoord = float(row[39])
        
        if fixationStartTime is None:
            # Initialize the fixation
            fixationStartTime = currentTime
            originHorzGazeCoord = currentHorzGazeCoord
            originVertGazeCoord = currentVertGazeCoord
        else:
            # Calculate the Euclidean distance to check if it's within 1 degree of the original fixation point
            pointDistance = math.sqrt(((currentHorzGazeCoord - originHorzGazeCoord) ** 2) + ((currentVertGazeCoord - originVertGazeCoord) ** 2))
            theta = math.atan(pointDistance / (2 * 70)) * (180 / math.pi)  # Assuming 70 cm from screen
            within_one_degree = theta <= 1 
            
            if within_one_degree:
                # If still within 1 degree, we continue the fixation
                pass
            else:
                # Fixation ended, calculate duration and reset
                duration = currentTime - fixationStartTime
                # Filter out the durations based on your criteria (e.g., only including certain ranges)
                fixationDurations.append(duration)
                
                # Start a new fixation
                fixationStartTime = currentTime
                originHorzGazeCoord = currentHorzGazeCoord
                originVertGazeCoord = currentVertGazeCoord

    # Calculate the average duration of fixations
    avgDuration = sum(fixationDurations) / len(fixationDurations) if fixationDurations else 0
    return avgDuration


def getFixationRate_sliding_window(csv_window):
    fixationCount, totalTime = 0, 0
    if not csv_window:
        return 0
    startTime = float(csv_window[0][0])  # Start time of the window
    endTime = float(csv_window[-1][0])  # End time of the window
    totalTime = endTime - startTime

    for i, row in enumerate(csv_window):
        currentTime = float(row[0])
        currentHorzGazeCoord = float(row[38])
        currentVertGazeCoord = float(row[39])
        if i > 0:  # Compare with previous row to calculate fixation
            prevRow = csv_window[i-1]
            prevTime = float(prevRow[0])
            prevHorzGazeCoord = float(prevRow[38])
            prevVertGazeCoord = float(prevRow[39])
            # Calculate if within 1 degree of previous fixation point
            pointDistance = math.sqrt(((currentHorzGazeCoord - prevHorzGazeCoord) ** 2) + ((currentVertGazeCoord - prevVertGazeCoord) ** 2))
            theta = math.atan(pointDistance / (2 * 70)) * (180 / math.pi)
            within_one_degree = theta <= 1
            if within_one_degree:
                duration = currentTime - prevTime
                if 0.2 <= duration <= 0.5:
                    fixationCount += 1
    
    fixationRate = fixationCount / totalTime if totalTime > 0 else 0
    return fixationRate

def getAvgSaccadeSize_sliding_window(csv_window):
    sumSaccadeSize, count = 0, 0
    for row in csv_window:
        try:
            horzGazeCoord = float(row[37])
            vertGazeCoord = float(row[38])
            saccadeSize = math.sqrt(horzGazeCoord ** 2 + vertGazeCoord ** 2)
            sumSaccadeSize += saccadeSize
            count += 1
        except ValueError:
            continue
    avgSaccadeSize = sumSaccadeSize / count if count else 0
    return avgSaccadeSize

def getAvgSaccadeSpeed_sliding_window(csv_window):
    totalSaccadeSize, totalTimeDiff = 0, 0
    for i, row in enumerate(csv_window):
        if i > 0:  # Need a previous point to calculate speed
            currentTime = float(row[0])
            prevRow = csv_window[i-1]
            prevTime = float(prevRow[0])
            timeDiff = currentTime - prevTime
            if timeDiff > 0:  # Avoid division by zero
                horzGazeCoord = float(row[37])
                vertGazeCoord = float(row[38])
                prevHorzGazeCoord = float(prevRow[37])
                prevVertGazeCoord = float(prevRow[38])
                saccadeSize = math.sqrt((horzGazeCoord - prevHorzGazeCoord) ** 2 + (vertGazeCoord - prevVertGazeCoord) ** 2)
                totalSaccadeSize += saccadeSize
                totalTimeDiff += timeDiff
    avgSaccadeSpeed = totalSaccadeSize / totalTimeDiff if totalTimeDiff > 0 else 0
    return avgSaccadeSpeed

def calculate_features_sliding_window(csv_data):
    window_size = 200  # Define your window size
    step_size = 50  # Define your step size for the sliding window
    features = []
    
    # Calculate the features using the sliding window approach
    AvgGazeLAOI = sliding_window_function(csv_data, window_size, step_size, getAvgGazeLAOI_sliding_window)
    AvgBlinkLatency = sliding_window_function(csv_data, window_size, step_size, getAvgBlinkLatency_sliding_window)
    MeanPupilSize_L = sliding_window_function(csv_data, window_size, step_size, getMeanPupilSize_L_sliding_window)
    MeanPupilSize_R = sliding_window_function(csv_data, window_size, step_size, getMeanPupilSize_R_sliding_window)
    AvgFixationDuration = sliding_window_function(csv_data, window_size, step_size, getAvgFixationDuration_sliding_window)
    FixationRate = sliding_window_function(csv_data, window_size, step_size, getFixationRate_sliding_window)
    AvgSaccadeSize = sliding_window_function(csv_data, window_size, step_size, getAvgSaccadeSize_sliding_window)
    AvgSaccadeSpeed = sliding_window_function(csv_data, window_size, step_size, getAvgSaccadeSpeed_sliding_window)
    
    # Combine the features into a single list
    features = list(zip(AvgGazeLAOI, AvgBlinkLatency, MeanPupilSize_L, MeanPupilSize_R, AvgFixationDuration, FixationRate, AvgSaccadeSize, AvgSaccadeSpeed))
    return features

def run(eye_data_folder):
    all_features = []
    
    # Walk through the files in the eye_data_folder
    for subdir, _, files in os.walk(eye_data_folder):
        for file in sorted(files):
            if file.endswith('.csv'):
                csv_file_path = os.path.join(subdir, file)
                with open(csv_file_path, "r") as f:
                    csv_reader = list(csv.reader(f))[1:]  # Skip the header
                    file_features = calculate_features_sliding_window(csv_reader)
                    
                    # Instead of extending all_features with file_features directly,
                    # calculate the average of file_features and append that to all_features
                    if file_features:  # Ensure file_features is not empty
                        avg_file_features = np.mean(np.array(file_features, dtype=np.float64), axis=0)
                        all_features.append(avg_file_features)
    
    if all_features:
        # Convert list of averaged features per file to a numpy array for easier manipulation
        feature_array = np.array(all_features)

        # Now, feature_array has one set of features per file, ready to be scaled
        scaler = MinMaxScaler()
        all_features_scaled = scaler.fit_transform(feature_array)

        # Return the 2D numpy array of the scaled features
        return all_features_scaled
    else:
        print("No features collected.")
        return np.array([])  # Return an empty array for consistency
