import asyncio
import fetch
from fastapi import HTTPException

from firestore_client import FirestoreClient

def getSessions(meeting_key: int):
    client = FirestoreClient().client  # une seule instance
    
    try:
        # Requête 1 : les sessions
        session_docs = client.collection('sessions').where('meeting_key', '==', meeting_key).get()
        sessions = [doc.to_dict() for doc in session_docs]
        if not sessions:
            return []

        result_ids = {f'{meeting_key}-{s["session_key"]}' for s in sessions}
        
        result_refs = [
            client.collection('session_results').document(doc_id)
            for doc_id in result_ids
        ]
        #batch
        result_docs = client.get_all(result_refs)  
        existing_results = {doc.id for doc in result_docs if doc.exists}

        for s in sessions:
            doc_id = f'{meeting_key}-{s["session_key"]}'
            s['session_results_available'] = doc_id in existing_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sessions: {str(e)}")

    return sessions

