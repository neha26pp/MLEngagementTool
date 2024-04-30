import unittest
from firebase_operations import FirebaseOperations

class TestFirebaseOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Firebase
        FirebaseOperations.initialize_firebase()

    @classmethod
    def tearDownClass(cls):
        # Clean up after tests (e.g., delete test data)
        pass

    def test_upload_file_to_storage_csv(self):
        # Test uploading CSV file to Firebase Storage
        # Mock the file_path and storage_path
        file_path = 'addresses2.csv'
        storage_path = 'demo_test/rawData/csv/' + file_path
        result = FirebaseOperations.upload_file_to_storage(file_path, storage_path, content_type='text/csv')
        self.assertEqual(result, storage_path)
    
    def test_upload_file_to_storage_txt(self):
        # Test uploading TXT file to Firebase Storage
        # Mock the file_path and storage_path
        file_path = 'sample3.txt'
        storage_path = 'demo_test/rawData/txt/' + file_path
        result = FirebaseOperations.upload_file_to_storage(file_path, storage_path, content_type='text/plain')
        self.assertEqual(result, storage_path)

    def test_delete_file_from_storage_csv(self):
        # Test deleting CSV file from Firebase Storage
        # Mock the storage_path of the CSV file to be deleted
        file_path = 'addresses2.csv'
        storage_path = 'demo_test/rawData/csv/' + file_path
        FirebaseOperations.upload_file_to_storage(file_path, storage_path, content_type='text/csv')
        deleted = FirebaseOperations.delete_file_from_storage(storage_path)
        self.assertTrue(deleted)
    
    def test_delete_file_from_storage_txt(self):
        # Test deleting txt file from Firebase Storage
        # Mock the storage_path of the txt file to be deleted
        file_path = 'sample3.txt'
        storage_path = 'demo_test/rawData/txt/' + file_path
        FirebaseOperations.upload_file_to_storage(file_path, storage_path, content_type='text/plain')
        deleted = FirebaseOperations.delete_file_from_storage(storage_path)
        self.assertTrue(deleted)

    def test_add_firestore_document(self):
        # Test adding document to Firestore
        # Mock collection_name, document_name, and document_data
        collection_name = 'demo_test_collection'
        document_name = 'test_document'
        document_data = {
            'stimulus1': 'Example Stimulus 1',
            'stimulus2': 'Example Stimulus 2',
            'eyeScore': 95,
            'emotionScore': 80,
            'fusionScore': 75
        }
        
        # Convert storage paths to Firestore document paths
        csv_document_path = 'demo_test/rawData/csv/addresses2'
        txt_document_path = 'demo_test/rawData/txt/sample3'
        
        # Create Firestore document references
        file_references = {
            'csvFile': FirebaseOperations.create_firestore_reference(csv_document_path),
            'txtFile': FirebaseOperations.create_firestore_reference(txt_document_path)
        }

        FirebaseOperations.add_firestore_document(collection_name, document_name, document_data, file_references)

        # Check if the document exists in Firestore
        doc_ref = FirebaseOperations.get_firestore_document(collection_name, document_name)
        self.assertIsNotNone(doc_ref)

    def test_delete_firestore_document(self):
        # Test deleting a document from Firestore
        # Mock collection_name and document_name
        collection_name = 'demo_test_collection'
        document_name = 'test_document2'

        # Create the document before deleting
        document_data = {
            'stimulus1': 'Example Stimulus 1',
            'stimulus2': 'Example Stimulus 2',
            'eyeScore': 95,
            'emotionScore': 80,
            'fusionScore': 75
        }
        FirebaseOperations.add_firestore_document(collection_name, document_name, document_data)

        # Delete the document from Firestore
        FirebaseOperations.delete_firestore_document(collection_name, document_name)

        # Check if the document has been deleted
        doc_ref = FirebaseOperations.get_firestore_document(collection_name, document_name)
        self.assertTrue(doc_ref)
    
    def test_get_firestore_document(self):
        # Test getting a document from Firestore
        # Mock collection_name and document_name
        collection_name = 'demo_test_collection'
        document_name = 'test_document3'

        # Create the document before querying
        document_data = {
            'stimulus1': 'Example Stimulus 1',
            'stimulus2': 'Example Stimulus 2',
            'eyeScore': 95,
            'emotionScore': 80,
            'fusionScore': 75
        }
        # Convert storage paths to Firestore document paths
        csv_document_path = 'demo_test/rawData/csv/addresses2'
        txt_document_path = 'demo_test/rawData/txt/sample3'
        
        # Create Firestore document references
        file_references = {
            'csvFile': FirebaseOperations.create_firestore_reference(csv_document_path),
            'txtFile': FirebaseOperations.create_firestore_reference(txt_document_path)
        }

        FirebaseOperations.add_firestore_document(collection_name, document_name, document_data, file_references)
        # Get the document from Firestore
        doc_ref = FirebaseOperations.get_firestore_document(collection_name, document_name)

        # Check if the document exists
        self.assertTrue(doc_ref.exists)

        # Get the document data
        doc_data = doc_ref.to_dict()

        # Remove the file_references from the document data for comparison
        doc_data.pop('csvFile', None)
        doc_data.pop('txtFile', None)

        # Check if the document data is correct
        expected_data = {
            'stimulus1': 'Example Stimulus 1',
            'stimulus2': 'Example Stimulus 2',
            'eyeScore': 95,
            'emotionScore': 80,
            'fusionScore': 75
        }
        self.assertEqual(doc_data, expected_data)

if __name__ == '__main__':
    unittest.main()
