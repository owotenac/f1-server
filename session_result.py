from fastapi import HTTPException
import asyncio
import fetch
from firestore_client import FirestoreClient


def get_session_result(meeting_key: int, session_key: int):

    try: 
        session_results = FirestoreClient().client.collection('session_results').document(f'{meeting_key}-{session_key}').get()

        if (session_results.exists == False):
            raise HTTPException(status_code=404, detail=f"Session result not found")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session result: {str(e)}")
            
    return session_results.to_dict()