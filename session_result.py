from fastapi import HTTPException
import asyncio
import fetch


def get_session_result(session_key: int):

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team data: {str(e)}")
            
    return response  