
import fastf1
from flask import request, session
import pandas as pd
import asyncio
import fetch

resultColumns = {
    'DriverNumber' : 'driver_number', 
    'Position': 'position'
}

def get_session_result():
    #year
    year = request.args.get('year', type=int)
    if (year is None):
        message = "year parameter is required"
        return { "error": message }, 400
    #round
    meeting_key = request.args.get('meeting_key', type=int)
    if (meeting_key is None):
        message = "meeting_key parameter is required"
        return { "error": message }, 400
    #session
    session_key = request.args.get('session_key', type=int)
    if (session_key is None):
        message = "session_key parameter is required"
        return { "error": message }, 400

    if (year == 2026):
        session = fastf1.get_session(year, meeting_key, session_key)
        session.load(laps=True, telemetry=True, messages=False, weather=False)

        #rename columns
        resultDF = session.results
        resultDF = resultDF.rename(columns=resultColumns)
        #add the position
        resultDF['position'] = range(1, len(resultDF) + 1)

        for index, row in resultDF.iterrows():
            driver_name = row['Abbreviation']
            best_lap_info = session.laps.pick_drivers(driver_name).pick_fastest(True)
            # Assuming more_info is a dict with keys matching column names
            if best_lap_info is not None:
                resultDF.loc[index, 'best_lap_time'] = best_lap_info['LapTime']
                resultDF.loc[index, 'Compound'] = best_lap_info['Compound']

        return resultDF.to_json(orient='records', date_format='iso')
    else:
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
                
        return response  