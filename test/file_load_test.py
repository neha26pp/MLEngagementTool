import unittest
from firebase_operations import FirebaseOperations

class TestFirebaseStorageLoad(unittest.TestCase):
    def test_upload_files_to_storage(self):
        FirebaseOperations.initialize_firebase()
        num_files = 1000  # Change this to the desired number of files
        csv_file_path = 'addresses2.csv'
        txt_file_path = 'sample3.txt'
        
        for i in range(num_files):
            csv_storage_path = f'demo_load_test/csv/sample_{i}.csv'  # Specify different storage paths for each upload
            txt_storage_path = f'demo_load_test/txt/sample_{i}.txt'

            # Upload files to Firebase Storage
            result = FirebaseOperations.upload_file_to_storage(csv_file_path, csv_storage_path)
            self.assertEqual(result, csv_storage_path)
            result = FirebaseOperations.upload_file_to_storage(txt_file_path, txt_storage_path)
            self.assertEqual(result, txt_storage_path)

if __name__ == '__main__':
    unittest.main()
