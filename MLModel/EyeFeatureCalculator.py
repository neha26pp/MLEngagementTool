import csv
import math
import os

def getAvgGazeLAOI(csv_data):
    SumLAOI = 0
    rowCount = 0
    minLAOI = 0  # Initialize with a large value
    maxLAOI = 1  # Initialize with a small value

    # Start processing from the first data row, skipping the header assumed to be at index 0
    for row in csv_data[1:]:  # Skip the header by slicing the list to start from the second element
        try:
            # Convert Gaze_LAOI value to int and add to sum
            LAOI = int(row[6])
            SumLAOI += LAOI
            rowCount += 1
            # Update minLAOI and maxLAOI
            minLAOI = min(minLAOI, LAOI)
            maxLAOI = max(maxLAOI, LAOI)
        except ValueError as e:
            # Handle rows where conversion to integer fails
            print(f"Skipping row due to error: {e}")

    if rowCount > 0:
        AvgGazeLAOI = SumLAOI / rowCount
    else:
        AvgGazeLAOI = 0  # Avoid division by zero if there are no valid rows

    # Scale AvgGazeLAOI
    if maxLAOI != minLAOI:  # Avoid division by zero
        scaledAvgGazeLAOI = (AvgGazeLAOI - minLAOI) / (maxLAOI - minLAOI)
    else:
        scaledAvgGazeLAOI = 0  # or any other value that makes sense in your case

    return scaledAvgGazeLAOI
            
def getAvgBlinkLatency_L(csv_data):
    sumLatency = 0
    count = 0
    minLatency = 2  # Initialize with a large value
    maxLatency = 10  # Initialize with a small value

    # Skip the header row by starting from the first data row
    for row in csv_data[1:]:  # Assuming csv_data includes the header at index 0
        try:
            # Only process rows with a valid numeric value in the specified column
            value = float(row[25])  # Attempt to convert the value to float
            if value > 0.7:
                sumLatency += value
                count += 1
                # Update minLatency and maxLatency
                minLatency = min(minLatency, value)
                maxLatency = max(maxLatency, value)
        except ValueError as e:
            # Handle the case where conversion to float fails
            print(f"Skipping row due to error: {e}")

    if count > 0:
        avgLatency = sumLatency / count
    else:
        avgLatency = 0  # Avoid division by zero if no valid rows were found

    # Scale avgLatency
    if maxLatency != minLatency:  # Avoid division by zero
        scaledAvgLatency = (avgLatency - minLatency) / (maxLatency - minLatency)
    else:
        scaledAvgLatency = 0  # or any other value that makes sense in your case

    return scaledAvgLatency
                
def getMeanPupilSize_L(csv_data):
    min_size = 500  # Minimum pupil size
    max_size = 5000  # Maximum pupil size
    sumPupilSize = 0
    rowCount = 0
    
    for row in csv_data[1:]:
        sumPupilSize += (float(row[13]) * float(row[15]) * math.pi)
        rowCount += 1
    
    if rowCount == 0:  # Prevent division by zero
        return 0

    # Calculate the average pupil size
    avgPupilSize = sumPupilSize / rowCount

    # Normalize the average pupil size to a 0-1 scale
    normalizedSize = (avgPupilSize - min_size) / (max_size - min_size)
    normalizedSize = max(0, min(normalizedSize, 1))  # Ensure the value is within [0, 1]

    return normalizedSize
        
def getMeanPupilSize_R(csv_data):
    min_size = 500  # Minimum pupil size
    max_size = 5000  # Maximum pupil size
    sumPupilSize = 0
    rowCount = 0
    
    for row in csv_data[1:]:
        sumPupilSize += (float(row[14]) * float(row[16]) * math.pi)
        rowCount += 1
    
    if rowCount == 0:  # Prevent division by zero
        return 0

    # Calculate the average pupil size
    avgPupilSize = sumPupilSize / rowCount

    # Normalize the average pupil size to a 0-1 scale
    normalizedSize = (avgPupilSize - min_size) / (max_size - min_size)
    normalizedSize = max(0, min(normalizedSize, 1))  # Ensure the value is within [0, 1]

    return normalizedSize
        
def getAvgFixationDuration(csv_data):
    min_duration = 0.05  # Minimum fixation duration in seconds
    max_duration = 0.15  # Maximum fixation duration in seconds
    fixationDurations = []
    fixationStartTime = None
    originHorzGazeCoord = None
    originVertGazeCoord = None
    
    for row in csv_data[1:]:
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
            # Calculate if within 1 degree of initial fixation point
            pointDistance = math.sqrt(((currentHorzGazeCoord - originHorzGazeCoord) ** 2) + ((currentVertGazeCoord - originVertGazeCoord) ** 2))
            theta = math.atan(pointDistance / (2 * 70)) * (180 / math.pi)  # Assuming 70 cm from screen
            within_one_degree = theta <= 1
            
            if within_one_degree:
                duration = currentTime - fixationStartTime
                
                # Only append durations that fall within the specified range
                if min_duration <= duration <= max_duration:
                    fixationDurations.append(duration)
                
                fixationStartTime = currentTime
                originHorzGazeCoord = currentHorzGazeCoord
                originVertGazeCoord = currentVertGazeCoord
            else:
                fixationStartTime = None

    # Calculate the average duration of fixations
    if fixationDurations:
        avgDuration = sum(fixationDurations) / len(fixationDurations)
    else:
        avgDuration = 0

    # Normalize the average duration to a 0-1 scale
    if avgDuration > 0:
        normalizedDuration = (avgDuration - min_duration) / (max_duration - min_duration)
        normalizedDuration = max(0, min(normalizedDuration, 1))  # Ensure the value is within [0, 1]
    else:
        normalizedDuration = 0

    return normalizedDuration
            
def getFixationRate(csv_data):
    minRate = 0  # Minimum fixation rate
    maxRate = 3   # Maximum fixation rate
    totalTime = float(csv_data[-1][0])
    fixationCount = 0
    fixationStartTime = None
    originHorzGazeCoord = None
    originVertGazeCoord = None
    distanceFromScreen = 70  # Preset distance from screen in centimeters

    for row in csv_data[1:]:
        currentTime = float(row[0])
        currentHorzGazeCoord = float(row[38])
        currentVertGazeCoord = float(row[39])
        
        if fixationStartTime is None:
            # Initialize the fixation
            fixationStartTime = currentTime
            originHorzGazeCoord = currentHorzGazeCoord
            originVertGazeCoord = currentVertGazeCoord
        else:
            # Calculate the distance and check if within 1 degree
            pointDistance = math.sqrt(((currentHorzGazeCoord - originHorzGazeCoord) ** 2) + ((currentVertGazeCoord - originVertGazeCoord) ** 2)) # Distance formula
            theta = math.atan(pointDistance / (2 * distanceFromScreen)) * (180 / math.pi) # Convert to degrees
            within_one_degree = theta <= 1 # Check if within 1 degree
            
            if within_one_degree:
                duration = currentTime - fixationStartTime
                
                if duration > 0.5:
                    # End the fixation because it's too long, but don't record it
                    fixationStartTime = None
            else:
                # End the fixation because the gaze moved too far
                if fixationStartTime:
                    duration = currentTime - fixationStartTime
                    if 0.2 <= duration <= 0.5:
                        fixationCount += 1  # Counting the fixation
                fixationStartTime = currentTime
                originHorzGazeCoord = currentHorzGazeCoord
                originVertGazeCoord = currentVertGazeCoord

    # Handle the last fixation if it was ongoing
    if fixationStartTime and 0.2 <= (currentTime - fixationStartTime) <= 0.5:
        fixationCount += 1  # Count the last fixation if it meets the criteria
        
    if totalTime > 0:
        fixationRate = fixationCount / totalTime
        scaledRate = (fixationRate - minRate) / (maxRate - minRate)
    else:
        scaledRate = 0

    return scaledRate
        
def getAvgSaccadeSize(csv_data):
    minSaccadeSize = 50  # Minimum saccade size
    maxSaccadeSize = 1000 # Maximum saccade size
    sumSaccadeSize = 0
    count = 0

    # Skip the header row by starting from index 1
    for row in csv_data[1:]:
        try:
            # Assuming 'horz_gaze_coord' is at index 37 and 'vert_gaze_coord' is at index 38 in data rows
            horzGazeCoord = float(row[37])  # Adjusted index assuming 0-based indexing for data rows
            vertGazeCoord = float(row[38])
            # Calculate saccade size or use appropriate logic here
            # For demonstration, using a placeholder calculation:
            saccadeSize = (horzGazeCoord ** 2 + vertGazeCoord ** 2) ** 0.5
            sumSaccadeSize += saccadeSize
            count += 1
        except ValueError as e:
            print(f"Skipping row {row} due to error: {e}")

    if count > 0:
        avgSaccadeSize = sumSaccadeSize / count
        scaledAvgSaccadeSize = (avgSaccadeSize - minSaccadeSize) / (maxSaccadeSize - minSaccadeSize)
    else:
        avgSaccadeSize = 0  # Avoid division by zero if there are no valid rows

    return scaledAvgSaccadeSize
        
def getAvgSaccadeSpeed(csv_data):
    minSpeed = 5000  # Minimum saccade speed
    maxSpeed = 40000 # Maximum saccade speed
    totalSaccadeSize = 0
    totalTimeDiff = 0
    prevTime = float(csv_data[1][0])  # Initialize with time from the first row

    for row in csv_data[1:]:  # Start from the second row
        try:
            # Assuming 'horz_gaze_coord' is at index 37 and 'vert_gaze_coord' is at index 38 in data rows
            horzGazeCoord = float(row[37])  # Adjusted index assuming 0-based indexing for data rows
            vertGazeCoord = float(row[38])
            # Calculate saccade size or use appropriate logic here
            # For demonstration, using a placeholder calculation:
            saccadeSize = (horzGazeCoord ** 2 + vertGazeCoord ** 2) ** 0.5
            totalSaccadeSize += saccadeSize
            currentTime = float(row[0])  # Assuming time is at index 0
            timeDiff = currentTime - prevTime
            totalTimeDiff += timeDiff
            prevTime = currentTime  # Store the current time for the next iteration
        except ValueError as e:
            print(f"Skipping row {row} due to error: {e}")
    if totalTimeDiff > 0:
        avgSaccadeSpeed = totalSaccadeSize / totalTimeDiff  # Use totalTimeDiff instead of timeDiff
        scaledAvgSaccadeSpeed = (avgSaccadeSpeed - minSpeed) / (maxSpeed - minSpeed)
    else:
        avgSaccadeSpeed = 0  # Avoid division by zero if there are no valid rows
        
    return scaledAvgSaccadeSpeed

def calculateFeatures(csv_data):
    # Calculate the features
    AvgGazeLAOI = getAvgGazeLAOI(csv_data)
    AvgBlinkLatency_L = getAvgBlinkLatency_L(csv_data)
    MeanPupilSize_L = getMeanPupilSize_L(csv_data)
    MeanPupilSize_R = getMeanPupilSize_R(csv_data)
    FixationDuration = getAvgFixationDuration(csv_data)
    fixationRate = getFixationRate(csv_data)
    AvgSaccadeSize = getAvgSaccadeSize(csv_data)
    AvgSaccadeSpeed = getAvgSaccadeSpeed(csv_data)
    
    # Add every variable to an array
    features = [AvgGazeLAOI, AvgBlinkLatency_L, MeanPupilSize_L, MeanPupilSize_R, FixationDuration, fixationRate, AvgSaccadeSize, AvgSaccadeSpeed]
    return features

def run(eye_data_folder):
    features_2d = []
    
    # Use os.walk to navigate the directory structure
    for subdir, _, files in os.walk(eye_data_folder):
        # Sort files if needed to ensure they are processed in a specific order
        for file in sorted(files):  # Ensuring a consistent order
            # Check if file is a CSV by its extension
            if file.endswith('.csv'):
                csv_file_path = os.path.join(subdir, file)
                with open(csv_file_path, "r") as f:
                    csv_reader = list(csv.reader(f))[1:]  # Skip header
                    features = calculateFeatures(csv_reader)
                    features_2d.append(features)
    return features_2d