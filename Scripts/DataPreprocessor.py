import os

import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import pandas as pd
import seaborn as sns
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler

from Scripts.DataLoad import DataLoad


class DataNormalization:
    @classmethod
    def minMaxScaler(cls, df: pd.DataFrame = None, data_list: list = None, header_skip: int = 2, col_skip: int = 2):
        scaler = MinMaxScaler()

        if df is None and data_list is not None:
            df = pd.DataFrame(data_list)

        if df is None and data_list is None:
            raise ValueError("DataNormalization: Expect data frame or data list")

        # Drop the first two rows (headers)
        df = df.iloc[header_skip:, :].apply(pd.to_numeric, errors='coerce')

        if df.empty:
            raise ValueError("DataNormalization: DataFrame is empty after dropping NaN values")

        normalized_df = df.copy()
        normalized_df.iloc[:, col_skip:] = pd.DataFrame(scaler.fit_transform(df.iloc[:, col_skip:]))
        return normalized_df

    @classmethod
    def normalizeMultipleDataframes(cls, dataframes: list[pd.DataFrame], header_skip: int = 2, col_skip: int = 2) -> list[pd.DataFrame]:
        # all_data = pd.concat(dataframes, ignore_index=True)
        normalized_dataframes = []
        for df in dataframes:
            normalized_df = cls.minMaxScaler(df=df, header_skip=header_skip, col_skip=col_skip)
            normalized_dataframes.append(normalized_df)
        return normalized_dataframes

    @classmethod
    def calculateNormalizedVariances(cls, data_frames_list: list[pd.DataFrame], header_skip: int = 2,
                                     col_skip: int = 2) -> pd.DataFrame:
        normalized_variances = []

        for df in data_frames_list:
            normalized_df = DataNormalization.minMaxScaler(df=df, header_skip=header_skip, col_skip=col_skip)
            variances = normalized_df.iloc[:, col_skip:].var()
            normalized_variances.append(variances)

        merged_variances = pd.concat(normalized_variances, axis=1)
        merged_variances.columns = ['DataFrame_' + str(i) for i in range(len(data_frames_list))]

        return merged_variances


class DataVisualization:
    @classmethod
    def visualizeEyeFeatures(cls, data: list, head_skip: int = 0) -> None:  # not finished
        df = pd.DataFrame(data)

        # Get time seq from the 1st column
        time_sequence = df.iloc[head_skip:, 0]

        # Plotting features in subplots
        num_features_per_subplot = 8
        num_subplots = len(df.columns) // num_features_per_subplot
        fig, axes = plt.subplots(num_subplots, 1, figsize=(10, 30))

        # Plotting each feature
        for i, ax in enumerate(axes):
            start_idx = i * num_features_per_subplot + 1
            end_idx = min((i + 1) * num_features_per_subplot + 1, len(df.columns))
            for col in df.columns[start_idx:end_idx]:
                feature_values = df[col][head_skip:]  # Slice the feature values based on head_skip
                ax.plot(time_sequence, feature_values, label=f'Feature {col}')
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('Feature values')
            ax.set_title(f'Subplot {i + 1}')
            ax.legend()
            ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))

        plt.tight_layout()
        plt.show()
        # plt.savefig("dist_of_engagement_scores.jpg")

    @classmethod
    def visualizeScores(cls, folder_path: str) -> None:
        scores = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    try:
                        value = float(file.read().strip().replace("%", ""))
                        scores.append(value)
                    except ValueError:
                        print(f"Skipping file {file_name}: Cannot convert content to float")

        scores = np.array(scores)
        plt.hist(scores, bins=20, density=True, alpha=0.7, label="Histogram")

        # Draw the kernel density estimation curve
        sns.kdeplot(scores, fill=True, color='purple', label='Kernel Density Estimation')

        # Set title and labels
        plt.title('Distribution of Engagement Scores')
        plt.xlabel('Scores')
        plt.ylabel('Probability Density')
        plt.grid(True)
        plt.legend()
        plt.show()
        # plt.savefig("dist_of_engagement_scores")


if __name__ == "__main__":
    # Try readCSV
    # dataset = DataLoad.readCSV("../EyeData/Anna Steinbeck/stimulus1.csv")

    # Try minMaxScaler
    # dataset = DataLoad.readCSV("../EyeData/Bradley Zelek/stimulus1.csv")
    # dataset = DataNormalization.minMaxScaler(data_list=dataset)
    # print(dataset)

    # Try normalizeMultipleDataframes
    # dataframes = DataLoad.readCSVFromSubDir("../EyeData", isDataFrame=True)
    # normalized_dataframes = DataNormalization.normalizeMultipleDataframes(dataframes)
    # print(normalized_dataframes)

    # Try calculateNormalizedVariances
    dataframes = DataLoad.readCSVFromSubDir("../EyeData", isDataFrame=True)
    normalized_variances = DataNormalization.calculateNormalizedVariances(dataframes)
    print(normalized_variances)

    # Try visualizeEyeFeatures - not finished
    # DataVisualization.visualizeEyeFeatures(dataset, head_skip=2)
    # dataset = DataLoad.readCSVFromSubDir("../EyeData/")
    # print(np.array(dataset).shape)

    # Try visualizeScores
    # DataVisualization.visualizeScores("MyQualtricsDownload/QuizScores")

    pass
