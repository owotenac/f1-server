import asyncio
from urllib.request import urlopen
import fastf1
import pandas as pd
from flask import request
import requests
import fetch

racesColumns = {
    'Location' : 'location', 
    'OfficialEventName': 'meeting_official_name', 
    'EventName': 'meeting_name',
    'Country' : 'country_name',
    'EventDate' : 'date_start',
    'RoundNumber' : 'meeting_key'
}

def getRaces():
    #year
    year = request.args.get('year', type=int)
    if (year is None):
        message = "year parameter is required"
        return { "error": message }, 400
    
    if (year == 2026):
        events = fastf1.get_event_schedule(year,include_testing=False)    
        events = events.rename(columns=racesColumns)
        events = events.assign(year=year)

        return events.to_json(orient='records', date_format='iso')
    else:
        params = {
            'year': year
        }
        response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/meetings', params=params))
        return response


if __name__ == "__main__":
    getRaces()