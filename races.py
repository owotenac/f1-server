from firestore_client import FirestoreClient
from fastapi import HTTPException
import config


def getRaces(year: int):
    races = []
    try:
        params = {
            'year': year
        }
        docs = FirestoreClient().client.collection('races').get()
        return [doc.to_dict() for doc in docs]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get races: {str(e)}")

    return races

