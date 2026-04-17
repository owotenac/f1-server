from fastapi import HTTPException
from firestore_client import FirestoreClient
from datetime import datetime, timezone
from google.cloud import firestore
import fetch
import asyncio


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


def getLastResults():
    try:
        races_ref = FirestoreClient().client.collection('races')
        now = datetime.now(timezone.utc)

        # Dernier GP terminé
        last_snap = (
            races_ref
            .where("date_end", "<", now)
            .order_by("date_end", direction=firestore.Query.DESCENDING)
            .limit(1)
            .get()
        )

        last_gp = last_snap[0].to_dict() if last_snap else None
        if last_gp is None:
            raise HTTPException(status_code=404, detail=f"Last GP not found")

        #get the last session of the race
        last_session_id = last_gp['race_sessions']['Race']
        session_ref = FirestoreClient().client.collection('sessions').document(f"{last_gp['meeting_key']}-{last_session_id}").get()
        session = session_ref.to_dict()

        #session results
        session_result = get_session_result(last_gp['meeting_key'], last_session_id)

        return { 'Race' : last_gp, 'Session': session, 'Results' : session_result}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session result: {str(e)}")

def getNextGP():
    try:
        races_ref = FirestoreClient().client.collection('races')
        now = datetime.now(timezone.utc)

        # Prochain GP pas encore commencé
        next_snap =  (
            races_ref
            .where("date_start", ">", now)
            .order_by("date_start", direction=firestore.Query.ASCENDING)
            .limit(1)
            .get()
        )

        next_gp = next_snap[0].to_dict() if next_snap else None

        return {"next_gp": next_gp}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session result: {str(e)}")