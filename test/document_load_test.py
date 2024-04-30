import unittest
from firebase_operations import FirebaseOperations

class TestFirebaseLoad(unittest.TestCase):
    def test_add_documents_to_collection(self):
        FirebaseOperations.initialize_firebase()
        collection_name = 'demo_load_test_collection'
        num_documents = 10000  # Change this to the desired number of documents
        
        # Add documents to the collection
        for i in range(num_documents):
            document_name = f'document_{i}'
            document_data = {
                'stimulus1': '.',
                'stimulus2': '.',
                'stimulus1Score': 0,
                'stimulus2Score': 0,
                'SVREye_stimulus1': 0,
                'SVREmotion_stimulus1': 0,
                'SVRFusion_stimulus1': 0,
                'LSTM_stimulus1': 0,
                'SVREye_stimulus2': 0,
                'SVREmotion_stimulus2': 0,
                'SVRFusion_stimulus2': 0,
                'LSTM_stimulus2': 0,
                # Add more fields as needed
            }
            
            # Add document to Firestore collection
            FirebaseOperations.add_firestore_document(collection_name, document_name, document_data)
            
            # Verify if the document exists in the collection
            self.assertTrue(FirebaseOperations.get_firestore_document(collection_name, document_name).exists)

if __name__ == '__main__':
    unittest.main()
