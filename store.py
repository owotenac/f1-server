
from requests import session

import race_picture
import fetch
import asyncio
from firestore_client import FirestoreClient
from fastapi import HTTPException

def storeRaces(year: int):
    try:
        params = {
            'year': year
        }
        response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/meetings', params=params))

        for race in response:
            pictureURL = race_picture.racePictureURLs.get(race['location'], "")
            race['pictureURL'] = pictureURL
            #store races
            FirestoreClient().client.collection('races').document(str(race["meeting_key"])).set(race)
            #get sessions for each
            storeSessions(race["meeting_key"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get races: {str(e)}")
    
    return response

def storeSessions(meeting_key: int):
    try:
        params = {
            'meeting_key': meeting_key
        }
        response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/sessions', params=params))

        for session in response:
            FirestoreClient().client.collection('sessions').document(f'{meeting_key}-{session["session_key"]}').set(session)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")
    
    return response

def storeSessionsResults(meeting_key: int, session_key: int):
    try:
        params = {
            'session_key': session_key
        }
        response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/session_result', params=params))
        #then we retrieve the driver info
        drivers = asyncio.run(fetch.api_call('https://api.openf1.org/v1/drivers', params=params))
        #create a map of driver id to driver info
        driver_map = {driver['driver_number']: driver for driver in drivers}
        #enrich the response with driver info     
        for result in response:
            driver_id = result['driver_number']
            if driver_id in driver_map:
                result['driver_info'] = driver_map[driver_id]

        session_result = {}
        session_result['results'] = response #because it's an array
        
        FirestoreClient().client.collection('session_results').document(f'{meeting_key}-{session_key}').set(session_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get store session: {str(e)}")
    
    return session_result 

