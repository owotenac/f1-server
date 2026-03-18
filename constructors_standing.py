import asyncio
import fetch
import constructors_picture
from fastapi import HTTPException
import copy
def constructors_standing(year: int):

    try: 
        params = {
            'year': year
        }
        baseURL = f'https://api.jolpi.ca/ergast/f1/{year}/constructorstandings/'
        response = asyncio.run(fetch.api_call(baseURL, params=params))

        # Deep copy pour ne pas muter l'objet en cache
        simplifiedResponse = copy.deepcopy(
            response["MRData"]['StandingsTable']['StandingsLists'][0]
        )
                #then rename keys to fit with Props in client
        for constructor in simplifiedResponse['ConstructorStandings']:
            #get the team name mapping
            teamID = constructor.get("Constructor", {}).get("constructorId","")
            constructor["Constructor"]["logo_url"] = constructors_picture.contructorsInfo.get(teamID, {}).get("logo_url", "")
            constructor["Constructor"]["color"] = constructors_picture.contructorsInfo.get(teamID, {}).get("color", "")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team data: {str(e)}")

    return simplifiedResponse