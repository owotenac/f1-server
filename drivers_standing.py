import asyncio
import fetch
import constructors_picture
import drivers_picture
from fastapi import HTTPException
import copy

def drivers_standing(year : int):
    try: 
        params = {
            'year': year
        }
        baseURL = f'https://api.jolpi.ca/ergast/f1/{year}/driverstandings/'
        response = asyncio.run(fetch.api_call(baseURL, params=params))

        # Deep copy pour ne pas muter l'objet en cache
        simplifiedResponse = copy.deepcopy(
            response["MRData"]['StandingsTable']['StandingsLists'][0]
        )

        #then rename keys to fit with Props in client
        for driver in simplifiedResponse['DriverStandings']:
            driver["Driver"]["picture_url"] = drivers_picture.driversPictureInfo.get(driver["Driver"]["code"], {}).get("headshot_url", "")
            #then if we find the teamname in the constructor list, we add it
            team_id = driver["Constructors"][0]["constructorId"]
            #then we had the team information
            team = constructors_picture.contructorsInfo.get(team_id, {})
            driver["Constructors"] = team
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get drivers standings: {str(e)}")  

    return simplifiedResponse