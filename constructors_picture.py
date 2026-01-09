import asyncio
import fetch

constructionMapping = {
    'Red Bull': 'redbullracing',
    'McLaren': 'mclaren',
    'Sauber': 'kicksauber',
    'RB F1 Team': 'racingbulls',
    'Alpine F1 Team': 'alpine',
    'Mercedes': 'mercedes',
    'Aston Martin': 'astonmartin',
    'Ferrari': 'ferrari',
    'Williams': 'williams',
    'Haas F1 Team': 'haasf1team'
}


contructorsInfo = {
  'redbullracing': {
    'team_name': 'Red Bull Racing',
    'team_color': '4781D7',
    'team_id': 'redbullracing',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/redbullracing/2025redbullracinglogo.png'
  },
  'mclaren': {
    'team_name': 'McLaren',
    'team_color': 'F47600',
    'team_id': 'mclaren',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/mclaren/2025mclarenlogo.png'
  },
  'kicksauber': {
    'team_name': 'Kick Sauber',
    'team_color': '01C00E',
    'team_id': 'kicksauber',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/kicksauber/2025kicksauberlogo.png'
  },
  'racingbulls': {
    'team_name': 'Racing Bulls',
    'team_color': '6C98FF',
    'team_id': 'racingbulls',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/racingbulls/2025racingbullslogo.png'
  },
  'alpine': {
    'team_name': 'Alpine',
    'team_color': '00A1E8',
    'team_id': 'alpine',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/alpine/2025alpinelogo.png'
  },
  'mercedes': {
    'team_name': 'Mercedes',
    'team_color': '00D7B6',
    'team_id': 'mercedes',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/mercedes/2025mercedeslogo.png'
  },
  'astonmartin': {
    'team_name': 'Aston Martin',
    'team_color': '229971',
    'team_id': 'astonmartin',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/astonmartin/2025astonmartinlogo.png'
  },
  'ferrari': {
    'team_name': 'Ferrari',
    'team_color': 'ED1131',
    'team_id': 'ferrari',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/ferrari/2025ferrarilogo.png'
  },
  'williams': {
    'team_name': 'Williams',
    'team_color': '1868DB',
    'team_id': 'williams',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/williams/2025williamslogo.png'
  },
  'haasf1team': {
    'team_name': 'Haas F1 Team',
    'team_color': '9C9FA2',
    'team_id': 'haasf1team',
    'logo_url': 'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/haasf1team/2025haasf1teamlogo.png'
  }
}

def extractConstructorsInfo(year: int):

    params = {
        'session_key': 9839
    }
    response_openf1 = asyncio.run(fetch.api_call('https://api.openf1.org/v1/drivers', params=params))

    constructors = {}
    for r in response_openf1:
        teamID = r['team_name'].lower().replace(" ","")
        if teamID not in constructors:
            c = {}
            c['team_name'] = r['team_name']
            c['team_color'] = r['team_colour']
            c['team_id'] = teamID
            c['logo_url'] = testURL(c['team_id'])

            constructors[teamID] = c

    print (constructors)


def testURL(team: str) -> str:
    baseURL = f'https://media.formula1.com/image/upload/c_lfill,w_40/q_auto/v1740000000/common/f1/2025/{team}/2025{team}logo.png'
    response = fetch.is_valid_image_url(baseURL)
    if response['valid'] and response['status_code'] == 200:
        return baseURL
    return ""

if __name__ == "__main__":

    #year 2025 => 9839
    extractConstructorsInfo(2025)
