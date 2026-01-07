import fastf1
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
        
    if (year == 2026):
        #we have 5 events
        sessions_list = []
        for i in range(1,6):
            s = {}
            ss = fastf1.get_session(year, meeting_key, i)
            s['meeting_key'] = meeting_key
            s['session_key'] = i
            s['circuit_key'] = meeting_key
            s['circuit_short_name'] = ss.event['EventName']
            s['location'] = ss.event['Location']
            s['country_name'] = ss.event['Country']
            s['meeting_name'] = ss.event['EventName']
            s['meeting_official_name'] = ss.event['OfficialEventName']
            s['date_start'] = ss.date
            s['local_start_time'] = ss.date
            s['session_type'] = ss.event['EventFormat']
            s['session_name'] = ss.name
            s['year'] = year
            sessions_list.append(s)

        return sessions_list
    else:
        params = {
            'year': year,
            'meeting_key': meeting_key
        }
        response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/sessions', params=params))
        return response        
