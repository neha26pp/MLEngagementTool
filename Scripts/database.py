import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase Admin using your project's credentials
if not firebase_admin._apps:
    cred = credentials.Certificate('C:/Users/NEHA/Downloads/MLEngagementTool/firebase.json')
    firebase_admin.initialize_app(cred)

# Firestore database initialization
db = firestore.client()

def add_to_sessions(name, stimulus1, stimulus2):
    # Reference to the sessions collection
    sessions_ref = db.collection('sessions')
    doc_ref = sessions_ref.document(name)

    # Check if the document already exists
    doc = doc_ref.get()
    if doc.exists:
        print(f"A document with the name '{name}' already exists.")
    else:
        # Create a new document with structure matching your screenshot
        document_data = {
            'stimulus1': stimulus1,
            'stimulus2': stimulus2,
            'stimulus1Score': 0,  # Assuming default score is 0
            'stimulus2Score': 0,  # Assuming default score is 0
            'SVREye_stimulus1': 0,
            'SVREmotion_stimulus1': 0,
            'SVRFusion_stimulus1': 0,
            'LSTM_stimulus1': 0,
            'SVREye_stimulus2': 0,
            'SVREmotion_stimulus2': 0,
            'SVRFusion_stimulus2': 0,
            'LSTM_stimulus2': 0,
        }
        doc_ref.set(document_data)
        print(f"Document with the name '{name}' has been successfully created.")


