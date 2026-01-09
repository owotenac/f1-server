import asyncio
from flask import request
import race_picture
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

    params = {
        'year': year
    }
    response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/meetings', params=params))

    for race in response:
        pictureURL = race_picture.racePictureURLs[race['location']]
        race['pictureURL'] = pictureURL

    return response

