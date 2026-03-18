import asyncio
import fetch
import constructors_standing

contructorsInfo = {
  'mercedes': {
    'name': 'Mercedes',
    'constructorId': 'mercedes',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/mercedes/2026mercedeslogo.png',
    "color": "00D7B6",
  },
  'ferrari': {
    'name': 'Ferrari',
    'constructorId': 'ferrari',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/ferrari/2026ferrarilogo.png',
    "color": "ED1131",
  },
  'mclaren': {
    'name': 'McLaren',
    'constructorId': 'mclaren',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/mclaren/2026mclarenlogo.png',
    "color": "F47600"
  },
  'red_bull': {
    'name': 'Red Bull',
    'constructorId': 'red_bull',
    "color": "4781D7",
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/redbullracing/2026redbullracinglogo.png'
  },
  'haas': {
    'name': 'Haas F1 Team',
    'constructorId': 'haas',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/haas/2026haaslogo.png',
    "color": "9C9FA2",
  },
  'rb': {
    'name': 'RB F1 Team',
    'constructorId': 'rb',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/racingbulls/2026racingbullslogo.png',
    "color": "6C98FF",
  },
  'audi': {
    'name': 'Audi',
    'constructorId': 'audi',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/audi/2026audilogo.png',
    "color": "F50537",
  },
  'alpine': {
    'name': 'Alpine F1 Team',
    'constructorId': 'alpine',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/alpine/2026alpinelogo.png',
    "color": "00A1E8",
  },
  'williams': {
    'name': 'Williams',
    'constructorId': 'williams',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/williams/2026williamslogo.png',
    "color": "1868DB",
  },
  'cadillac': {
    'name': 'Cadillac F1 Team',
    'constructorId': 'cadillac',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/cadillac/2026cadillaclogo.png',
    "color": "909090",
  },
  'aston_martin': {
    'name': 'Aston Martin',
    'constructorId': 'aston_martin',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/astonmartin/2026astonmartinlogo.png',
    "color": "229971",
  }
}
def extractConstructorsInfo(year: int):

    response_openf1 = constructors_standing.constructors_standing(year)


    constructors = {}
    for r in response_openf1['ConstructorStandings']:
        print(r)
        teamID = r['Constructor']['constructorId']
        c = {}
        c['name'] = r['Constructor']['name']
        #c['color'] = r['color']
        c['constructorId'] = teamID
        c['logo_url'] = testURL(teamID)

        constructors[teamID] = c

    print (constructors)


def testURL(team: str) -> str:
    baseURL = f'https://media.formula1.com/image/upload/c_lfill,w_64/q_auto/v1740000000/common/f1/2026/{team}/2026{team}logo.png'
    response = fetch.is_valid_image_url(baseURL)
    if response['valid'] and response['status_code'] == 200:
        return baseURL
    return ""

#year 2025 => 9839
#extractConstructorsInfo(2026)
