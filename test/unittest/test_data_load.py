import unittest
import pandas as pd
from Scripts.DataLoad import DataLoad
import os


class TestDataLoad(unittest.TestCase):
    def setUp(self):
        self.test_eye_folder_path = "../../MLModel/EyeTestDataSet"
        self.labels_folder_path = "/../../Scripts/MyQualtricsDownload/QuizScores"

    def test_readCSV(self):
        # it should read dataframe with correct size from a csv file
        file_path = os.path.join(self.test_eye_folder_path, "test1.csv")
        # Test reading as list
        data_list = DataLoad.readCSV(file_path)
        self.assertIsInstance(data_list, list)
        self.assertEqual(len(data_list), 13312)
        # Test reading as DataFrame
        data_df = DataLoad.readCSV(file_path, isDataFrame=True)
        self.assertIsInstance(data_df, pd.DataFrame)
        self.assertEqual(data_df.shape, (13312, 57))

    def test_readCSVFromSubDir(self):
        # It should read multiple CSV files from subdirectories
        features = DataLoad.readCSVFromSubDir(self.test_eye_folder_path)
        self.assertIsInstance(features, list)
        self.assertTrue(all(isinstance(feature, list) for feature in features))

    def test_readLabels(self):
        # It should read labels from txt files and return a list of floats
        labels = DataLoad.readLabels(self.labels_folder_path)
        # Assert the variable labels is a list of float
        self.assertIsInstance(labels, list)
        self.assertTrue(all(isinstance(label, float) for label in labels))


if __name__ == '__main__':
    unittest.main()
