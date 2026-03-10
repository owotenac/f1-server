import asyncio
import fetch
import constructors_picture
import drivers_picture
from fastapi import HTTPException

def drivers_standing(year : int):
    try: 
        params = {
            'year': year
        }
        baseURL = f'https://api.jolpi.ca/ergast/f1/{year}/driverstandings/'
        response = asyncio.run(fetch.api_call(baseURL, params=params))

        #we remove evrything which is not needed
        simplifiedResponse = response["MRData"]['StandingsTable']['StandingsLists'][0]
        #then rename keys to fit with Props in client
        for driver in simplifiedResponse['DriverStandings']:
            driver["Driver"]["name_acronym"] = driver["Driver"].pop("code")
            driver["Driver"]["last_name"] = driver["Driver"].pop("familyName")
            driver["Driver"]["first_name"] = driver["Driver"].pop("givenName")
            driver["Driver"]["driver_number"] = driver["Driver"].pop("permanentNumber")
            driver["Driver"]["headshot_url"] = driver["Driver"].pop("url")
            driver["Driver"]["team_name"] = driver["Constructors"][0].pop("name")
            driver["Driver"]["picture_url"] = drivers_picture.driversPictureInfo.get(driver["Driver"]["name_acronym"], {}).get("picture_url", "")
            driver.pop("Constructors")

            #then if we find the teamname in the constructor list, we add it
            team_name = driver["Driver"]["team_name"]
            #we need to map
            team_id = constructors_picture.constructionMapping.get(team_name)
            if (team_id in constructors_picture.contructorsInfo):
                driver["team"] = constructors_picture.contructorsInfo[team_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get drivers standings: {str(e)}")  

    return simplifiedResponse