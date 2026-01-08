from flask import request
import asyncio
import fetch

def getSessions():
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

    params = {
        'year': year,
        'meeting_key': meeting_key
    }
    response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/sessions', params=params))
    return response        
