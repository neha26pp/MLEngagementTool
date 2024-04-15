import unittest
import pandas as pd
from Scripts.DataPreprocessor import DataNormalization


class TestDataNormalization(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'skip1': [1, 2, 3],
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        })
        self.df2 = pd.DataFrame({
            'skip1': [1, 2, 3],
            'A': [4, 5, 6],
            'B': [7, 8, 9],
            'C': [10, 11, 12]
        })
        self.normalized_solution = pd.DataFrame({
            'skip1': [1, 2, 3],
            'A': [0.0, 0.5, 1.0],
            'B': [0.0, 0.5, 1.0],
            'C': [0.0, 0.5, 1.0]
        })
        self.variance_solution = pd.DataFrame({
            'DataFrame_0': [0.25, 0.25, 0.25],
            'DataFrame_1': [0.25, 0.25, 0.25],
        }, index=['A', 'B', 'C'])
        self.data_list = [[1, 1, 4, 7], [2, 2, 5, 8], [3, 3, 6, 9]]

    def test_minMaxScaler_with_dataframe(self):
        # it should return a DataFrame normalized
        normalized_df = DataNormalization.minMaxScaler(df=self.df, header_skip=0, col_skip=1)
        self.assertIsInstance(normalized_df, pd.DataFrame)
        pd.testing.assert_frame_equal(normalized_df, self.normalized_solution)

    def test_minMaxScaler_with_data_list(self):
        # it should return a DataFrame
        normalized_df = DataNormalization.minMaxScaler(data_list=self.data_list, header_skip=0, col_skip=1)
        self.assertIsInstance(normalized_df, pd.DataFrame)
        self.normalized_solution.columns = range(len(self.normalized_solution.columns))
        pd.testing.assert_frame_equal(normalized_df, self.normalized_solution)

    def test_minMaxScaler_with_empty_data(self):
        # it should raise a value error
        with self.assertRaises(ValueError):
            DataNormalization.minMaxScaler()

    def test_normalizeMultipleDataframes(self):
        # it should return a list of Dataframes normalized
        normalized_dataframes = DataNormalization.normalizeMultipleDataframes(
            [self.df, self.df2], header_skip=0, col_skip=1)

        # Assert output length
        self.assertEqual(len(normalized_dataframes), 2)

        # Assert output type
        for df in normalized_dataframes:
            self.assertIsInstance(df, pd.DataFrame)

        # Assert each normalized dataframe to the solution
        for df in normalized_dataframes:
            pd.testing.assert_frame_equal(df, self.normalized_solution)

    def test_calculateNormalizedVariances(self):
        # it should return a list of Dataframes with normalized variances
        variances = DataNormalization.calculateNormalizedVariances([self.df, self.df2], header_skip=0, col_skip=1)
        self.assertIsInstance(variances, pd.DataFrame)
        pd.testing.assert_frame_equal(variances, self.variance_solution)


if __name__ == '__main__':
    unittest.main()
