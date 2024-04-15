from __future__ import annotations
import csv
import os
import pandas as pd


class DataLoad:
    @classmethod
    def readCSV(cls, filePath: str, isDataFrame: bool = False) -> list | pd.DataFrame:
        # Check if file is a CSV by its extension
        if filePath.endswith('.csv'):
            with open(filePath, "r") as f:
                csv_reader = list(csv.reader(f))
                # Filter out columns that are all empty
                filtered_reader = []
                for row in csv_reader:
                    filtered_row = [cell for cell in row if cell.strip() != '']
                    if filtered_row:  # If the row is not empty after filtering, add it to the result
                        filtered_reader.append(filtered_row)
                if isDataFrame is False:
                    return filtered_reader
                else:
                    return pd.DataFrame(filtered_reader)

    @classmethod
    def readCSVFromSubDir(cls, eye_data_folder: str, isDataFrame: bool = False) -> list:
        features = []

        # Use os.walk to navigate the directory structure
        for subdir, _, files in os.walk(eye_data_folder):
            # Sort files if needed to ensure they are processed in a specific order
            for file in sorted(files):  # Ensuring a consistent order
                # Check if file is a CSV by its extension
                if file.endswith('.csv'):
                    features.append(DataLoad.readCSV(os.path.join(subdir, file), isDataFrame=isDataFrame))
        return features  # shape: # of student data, time-len, # of data features

    @classmethod
    def readLabels(cls, label_folder) -> list:
        labels = []
        for file in os.listdir(os.getcwd() + label_folder):
            if file.endswith(".txt"):
                full_path = os.path.join(os.getcwd() + label_folder, file)

                # print("Reading file: ", full_path)
                with open(full_path, 'r') as f:
                    # Read each line, remove the percent symbol, and convert to float
                    file_values = [float(line.strip().replace('%', '')) for line in f.readlines()]
                    labels.extend(file_values)  # Use extend to add all values in the list
        return labels

if __name__ == "__main__":
    # features = DataLoad.readCSVFromSubDir("../EyeData")
    # for matrix in features:
    #     print(len(matrix))

    # print(DataLoad.readCSV("../EyeData/Anna Steinbeck/stimulus1.csv"))

    # print(DataLoad.readLabels("/MyQualtricsDownload/QuizScores"))

    pass
