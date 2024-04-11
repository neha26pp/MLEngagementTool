import unittest
import MLModel.Regression.EyeFeatureCalculator as EyeFeatureCalculator
from MLModel.Regression.EyeFeatureCalculator import getAvgGazeLAOI, getMeanPupilSize_L, calculateFeatures, getAvgBlinkLatency_L, getMeanPupilSize_R, getAvgFixationDuration, getFixationRate, getAvgSaccadeSize, getAvgSaccadeSpeed
import os
import csv

class TestEyeFeatureCalculator(unittest.TestCase):
    def setUp(self):
        # Create mock CSV data that covers the columns needed by all functions
        # set mock csv  equal to the data in the csv file
        csv_file_path = "MLModel/EyeTestDataSet/test1.csv"
        self.mock_csv_data = []
        
        with open(csv_file_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip the header row
            for row in csvreader:
                self.mock_csv_data.append(row)

    def test_getAvgGazeLAOI(self):
        # Test getAvgGazeLAOI with mock data
        result = getAvgGazeLAOI(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)
        
    def test_getAvgBlinkLatency_L(self):
        # Test getAvgBlinkLatency_L with mock data
        result = getAvgBlinkLatency_L(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)
        
    def test_getMeanPupilSize_L(self):
        # Test getMeanPupilSize_L with mock data
        result = getMeanPupilSize_L(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)

    def test_getMeanPupilSize_R(self):
        # Test getMeanPupilSize_R with mock data
        result = getMeanPupilSize_R(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)
        
    def test_AvgFixationDuration(self):
        # Test AvgFixationDuration with mock data
        result = getAvgFixationDuration(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)
        
    def test_AvgFixationRate(self):
        # Test AvgFixationrate with mock data
        result = getFixationRate(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)
        
    def test_AvgSaccadeSize(self):
        # Test AvgSaccadeSize with mock data
        result = getAvgSaccadeSize(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)
        
    def test_AvgSaccadeSpeed(self):
        # Test AvgSaccadeSpeed with mock data
        result = getAvgSaccadeSpeed(self.mock_csv_data)
        # assert result is between 0 and 1 inclusive
        self.assertTrue(0 <= result <= 1)
        
    def test_calculateFeatures(self):
        # Test calculateFeatures with comprehensive mock data covering all required columns
        features = calculateFeatures(self.mock_csv_data)
        self.assertEqual(len(features), 8)  # Assuming you're calculating 8 features
        # Add more specific assertions to validate each feature's value

    def test_run(self):
        eye_data_folder = "MLModel/EyeTestDataSet"  # Update this path to the actual location
        expected_csv_count = sum(1 for _ in os.listdir(eye_data_folder) if _.endswith('.csv'))

        # Call the run function
        features_2d = EyeFeatureCalculator.run(eye_data_folder)

        # Assert that the number of CSV files matches the length of the features_2d array
        self.assertEqual(len(features_2d), expected_csv_count, "Number of processed CSV files does not match the expected count.")

if __name__ == '__main__':
    unittest.main()