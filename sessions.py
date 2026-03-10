import asyncio
import fetch
from fastapi import HTTPException

from firestore_client import FirestoreClient

def getSessions(year: int, meeting_key: int):
    sessions = []
    try:
        docs = FirestoreClient().client.collection('sessions').where('meeting_key', '==', meeting_key).get()

        for doc in docs:
            sessions.append(doc.to_dict())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sessions: {str(e)}")

    return sessions  

