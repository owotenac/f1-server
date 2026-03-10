from dotenv import load_dotenv
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db

class FirestoreClient(object):
    _instance = None
   
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreClient, cls).__new__(cls)
            cls._instance.client = cls._instance.getFirestoreClient()

        return cls._instance

    def firestoreCredentials(self) -> credentials.Certificate:
        """
        Returns a firebase_admin.credentials.Certificate object, created from either a file or a dict,
        depending on the available credentials source.
        """
        load_dotenv() 
        # Try to get credentials from environment variable
        cred_json = os.environ.get('asc-db')
        secret_file_path = './f1-app_db.json'

        if cred_json:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
        elif os.path.exists(secret_file_path):
            # Running locally with JSON file (for development only)
            cred = credentials.Certificate(secret_file_path)
        else:
            raise ValueError("Firebase credentials not found")
        return cred    

    def getFirestoreClient(self) -> firestore.client:
        cred = self.firestoreCredentials()
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        self._firestore_client = firestore.client()
        return self._firestore_client
   
    def deleteAllInFirestore(self, collection_name: str):
        collection_ref = self.client.collection(collection_name)
        self.delete_collection(collection_ref, 10)

    def delete_collection(self, coll_ref, batch_size):
        if batch_size == 0:
            return

        docs = coll_ref.list_documents(page_size=batch_size)
        deleted = 0

        for doc in docs:
            doc.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return self.delete_collection(coll_ref, batch_size)