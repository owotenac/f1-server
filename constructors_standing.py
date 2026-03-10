import asyncio
import fetch
import constructors_picture
from fastapi import HTTPException

def constructors_standing(year: int):

    try: 
        params = {
            'year': year
        }
        baseURL = f'https://api.jolpi.ca/ergast/f1/{year}/constructorstandings/'
        response = asyncio.run(fetch.api_call(baseURL, params=params))

        #we remove evrything which is not needed
        simplifiedResponse = response["MRData"]['StandingsTable']['StandingsLists'][0]
        #then rename keys to fit with Props in client
        for constructor in simplifiedResponse['ConstructorStandings']:
            print(constructor['Constructor'])
            #constructor["Constructor"]["team_name"] = constructor["Constructor"].pop("name")
            #constructor["Constructor"]["team_id"] = constructor["Constructor"].pop("constructorId")

            #get the team name mapping
            #teamName = constructors_picture.constructionMapping.get(constructor["Constructor"]["team_name"], "")
            #constructor["Constructor"]["logo_url"] = constructors_picture.contructorsInfo.get(teamName, {}).get("logo_url", "")
            #constructor["Constructor"]["team_color"] = constructors_picture.contructorsInfo.get(teamName, {}).get("team_color", "")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team data: {str(e)}")

    return simplifiedResponse