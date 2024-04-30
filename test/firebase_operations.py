import firebase_admin
from firebase_admin import credentials, storage, firestore

class FirebaseOperations:
    @staticmethod
    def initialize_firebase():
        cred = credentials.Certificate('cred.json')
        firebase_admin.initialize_app(cred, {'storageBucket': 'test2-c2612.appspot.com'})

    @staticmethod
    def upload_file_to_storage(file_path, storage_path, content_type=None):
        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        if content_type:
            blob.upload_from_filename(file_path, content_type=content_type)
        else:
            blob.upload_from_filename(file_path)
        return storage_path  # Return storage path as reference

    @staticmethod
    def add_firestore_document(collection_name, document_name, document_data, file_references=None):
        db = firestore.client()
        collection_ref = db.collection(collection_name)
        document_ref = collection_ref.document(document_name)
        if file_references:
            document_data.update(file_references)
        document_ref.set(document_data)

    @staticmethod
    def create_firestore_reference(storage_path):
        db = firestore.client()
        return db.document(storage_path)

    @staticmethod
    def get_firestore_document(collection_name, document_name):
        db = firestore.client()
        doc_ref = db.collection(collection_name).document(document_name)
        return doc_ref.get()

    @staticmethod
    def upload_file_and_add_firestore(file_path, storage_path, collection_name, document_name, document_data, content_type=None):
        # Upload file to Firebase Storage and get storage path as reference
        file_reference = FirebaseOperations.upload_file_to_storage(file_path, storage_path, content_type)

        # Get Firestore document reference for the uploaded file
        file_doc_reference = FirebaseOperations.create_firestore_reference(file_reference)

        # Add document to Firestore collection with reference to file path
        file_references = {'rawData': file_doc_reference}
        FirebaseOperations.add_firestore_document(collection_name, document_name, document_data, file_references)

        print(f'File {file_path} uploaded to {storage_path} in Firebase Storage.')
        print(f'Document added to {collection_name} in Firestore with file reference.')

    @staticmethod
    def delete_file_from_storage(storage_path):
        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        blob.delete()
        print(f'File {storage_path} deleted from Firebase Storage.')
        return True  # Return True to indicate successful deletion
    
    @staticmethod
    def delete_firestore_document(collection_name, document_name):
        try:
            db = firestore.client()
            collection_ref = db.collection(collection_name)
            document_ref = collection_ref.document(document_name)
            
            if document_ref.get().exists:
                document_ref.delete()
                print(f'Document {document_name} deleted from Firestore collection {collection_name}.')
                return True  # Return True to indicate successful deletion
            else:
                print(f'Document {document_name} does not exist in Firestore collection {collection_name}.')
                return False  # Return False to indicate document not found
        except Exception as e:
            print(f'Error deleting document {document_name} from Firestore collection {collection_name}: {e}')
            return False  # Return False to indicate deletion failure
    
    @staticmethod
    def get_firestore_document(collection_name, document_name):
        db = firestore.client()
        doc_ref = db.collection(collection_name).document(document_name)
        return doc_ref.get()
    

