
from requests import session

import race_picture
import fetch
import asyncio
from firestore_client import FirestoreClient
from fastapi import HTTPException
from datetime import datetime, timezone

def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s).astimezone(timezone.utc)

def storeRaces(year: int):
    try:
        params = {
            'year': year
        }
        response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/meetings', params=params))

        for race in response:
            #hack 2026 2 GP are still in openF1 but will not take place
            if (race['meeting_key'] == 1282 or race['meeting_key'] == 1283):
                continue
            pictureURL = race_picture.racePictureURLs.get(race['location'], "")
            race['pictureURL'] = pictureURL
            #get sessions for each
            raceSessions = storeSessions(race["meeting_key"])
            race['race_sessions'] = raceSessions
            #update date
            race['date_start']= parse_dt(race["date_start"])
            race['date_end']= parse_dt(race["date_end"])
            #store races
            FirestoreClient().client.collection('races').document(str(race["meeting_key"])).set(race)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get races: {str(e)}")
    
    return response

def storeSessions(meeting_key: int):
    try:
        params = {
            'meeting_key': meeting_key
        }
        response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/sessions', params=params))

        raceSessions = {}
        for session in response:
            FirestoreClient().client.collection('sessions').document(f'{meeting_key}-{session["session_key"]}').set(session)
            raceSessions[session['session_name']] = session['session_key']

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")
    
    return raceSessions

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

