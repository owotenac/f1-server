
import drivers_standing
import fetch

driversPictureInfo = {
  'NOR': {
    'driverId': 'norris',
    'dateOfBirth': '1999-11-13',
    'nationality': 'British',
    'name_acronym': 'NOR',
    'last_name': 'Norris',
    'first_name': 'Lando',
    'driver_number': '4',
    'headshot_url': 'http://en.wikipedia.org/wiki/Lando_Norris',
    'team_name': 'McLaren',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/mclaren/lannor01/2025mclarenlannor01right.png'
  },
  'VER': {
    'driverId': 'max_verstappen',
    'dateOfBirth': '1997-09-30',
    'nationality': 'Dutch',
    'name_acronym': 'VER',
    'last_name': 'Verstappen',
    'first_name': 'Max',
    'driver_number': '3',
    'headshot_url': 'http://en.wikipedia.org/wiki/Max_Verstappen',
    'team_name': 'Red Bull',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/redbullracing/maxver01/2025redbullracingmaxver01right.png'
  },
  'PIA': {
    'driverId': 'piastri',
    'dateOfBirth': '2001-04-06',
    'nationality': 'Australian',
    'name_acronym': 'PIA',
    'last_name': 'Piastri',
    'first_name': 'Oscar',
    'driver_number': '81',
    'headshot_url': 'http://en.wikipedia.org/wiki/Oscar_Piastri',
    'team_name': 'McLaren',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/mclaren/oscpia01/2025mclarenoscpia01right.png'
  },
  'RUS': {
    'driverId': 'russell',
    'dateOfBirth': '1998-02-15',
    'nationality': 'British',
    'name_acronym': 'RUS',
    'last_name': 'Russell',
    'first_name': 'George',
    'driver_number': '63',
    'headshot_url': 'http://en.wikipedia.org/wiki/George_Russell_(racing_driver)',
    'team_name': 'Mercedes',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/mercedes/georus01/2025mercedesgeorus01right.png'
  },
  'LEC': {
    'driverId': 'leclerc',
    'dateOfBirth': '1997-10-16',
    'nationality': 'Monegasque',
    'name_acronym': 'LEC',
    'last_name': 'Leclerc',
    'first_name': 'Charles',
    'driver_number': '16',
    'headshot_url': 'http://en.wikipedia.org/wiki/Charles_Leclerc',
    'team_name': 'Ferrari',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/ferrari/chalec01/2025ferrarichalec01right.png'
  },
  'HAM': {
    'driverId': 'hamilton',
    'dateOfBirth': '1985-01-07',
    'nationality': 'British',
    'name_acronym': 'HAM',
    'last_name': 'Hamilton',
    'first_name': 'Lewis',
    'driver_number': '44',
    'headshot_url': 'http://en.wikipedia.org/wiki/Lewis_Hamilton',
    'team_name': 'Ferrari',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/ferrari/lewham01/2025ferrarilewham01right.png'
  },
  'ANT': {
    'driverId': 'antonelli',
    'dateOfBirth': '2006-08-25',
    'nationality': 'Italian',
    'name_acronym': 'ANT',
    'last_name': 'Antonelli',
    'first_name': 'Andrea Kimi',
    'driver_number': '12',
    'headshot_url': 'https://en.wikipedia.org/wiki/Andrea_Kimi_Antonelli',
    'team_name': 'Mercedes',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/mercedes/andant01/2025mercedesandant01right.png'
  },
  'ALB': {
    'driverId': 'albon',
    'dateOfBirth': '1996-03-23',
    'nationality': 'Thai',
    'name_acronym': 'ALB',
    'last_name': 'Albon',
    'first_name': 'Alexander',
    'driver_number': '23',
    'headshot_url': 'http://en.wikipedia.org/wiki/Alexander_Albon',
    'team_name': 'Williams',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/williams/alealb01/2025williamsalealb01right.png'
  },
  'SAI': {
    'driverId': 'sainz',
    'dateOfBirth': '1994-09-01',
    'nationality': 'Spanish',
    'name_acronym': 'SAI',
    'last_name': 'Sainz',
    'first_name': 'Carlos',
    'driver_number': '55',
    'headshot_url': 'http://en.wikipedia.org/wiki/Carlos_Sainz_Jr.',
    'team_name': 'Williams',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/williams/carsai01/2025williamscarsai01right.png'
  },
  'ALO': {
    'driverId': 'alonso',
    'dateOfBirth': '1981-07-29',
    'nationality': 'Spanish',
    'name_acronym': 'ALO',
    'last_name': 'Alonso',
    'first_name': 'Fernando',
    'driver_number': '14',
    'headshot_url': 'http://en.wikipedia.org/wiki/Fernando_Alonso',
    'team_name': 'Aston Martin',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/astonmartin/feralo01/2025astonmartinferalo01right.png'
  },
  'HUL': {
    'driverId': 'hulkenberg',
    'dateOfBirth': '1987-08-19',
    'nationality': 'German',
    'name_acronym': 'HUL',
    'last_name': 'Hülkenberg',
    'first_name': 'Nico',
    'driver_number': '27',
    'headshot_url': 'http://en.wikipedia.org/wiki/Nico_H%C3%BClkenberg',
    'team_name': 'Sauber',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/kicksauber/nichül01/2025kicksaubernichül01right.png'
  },
  'HAD': {
    'driverId': 'hadjar',
    'dateOfBirth': '2004-09-28',
    'nationality': 'French',
    'name_acronym': 'HAD',
    'last_name': 'Hadjar',
    'first_name': 'Isack',
    'driver_number': '6',
    'headshot_url': 'https://en.wikipedia.org/wiki/Isack_Hadjar',
    'team_name': 'RB F1 Team',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/racingbulls/isahad01/2025racingbullsisahad01right.png'
  },
  'BEA': {
    'driverId': 'bearman',
    'dateOfBirth': '2005-05-08',
    'nationality': 'British',
    'name_acronym': 'BEA',
    'last_name': 'Bearman',
    'first_name': 'Oliver',
    'driver_number': '87',
    'headshot_url': 'http://en.wikipedia.org/wiki/Oliver_Bearman',
    'team_name': 'Haas F1 Team',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/haasf1team/olibea01/2025haasf1teamolibea01right.png'
  },
  'LAW': {
    'driverId': 'lawson',
    'dateOfBirth': '2002-02-11',
    'nationality': 'New Zealander',
    'name_acronym': 'LAW',
    'last_name': 'Lawson',
    'first_name': 'Liam',
    'driver_number': '30',
    'headshot_url': 'http://en.wikipedia.org/wiki/Liam_Lawson',
    'team_name': 'Red Bull',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/redbullracing/lialaw01/2025redbullracinglialaw01right.png'
  },
  'OCO': {
    'driverId': 'ocon',
    'dateOfBirth': '1996-09-17',
    'nationality': 'French',
    'name_acronym': 'OCO',
    'last_name': 'Ocon',
    'first_name': 'Esteban',
    'driver_number': '31',
    'headshot_url': 'http://en.wikipedia.org/wiki/Esteban_Ocon',
    'team_name': 'Haas F1 Team',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/haasf1team/estoco01/2025haasf1teamestoco01right.png'
  },
  'STR': {
    'driverId': 'stroll',
    'dateOfBirth': '1998-10-29',
    'nationality': 'Canadian',
    'name_acronym': 'STR',
    'last_name': 'Stroll',
    'first_name': 'Lance',
    'driver_number': '18',
    'headshot_url': 'http://en.wikipedia.org/wiki/Lance_Stroll',
    'team_name': 'Aston Martin',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/astonmartin/lanstr01/2025astonmartinlanstr01right.png'
  },
  'TSU': {
    'driverId': 'tsunoda',
    'dateOfBirth': '2000-05-11',
    'nationality': 'Japanese',
    'name_acronym': 'TSU',
    'last_name': 'Tsunoda',
    'first_name': 'Yuki',
    'driver_number': '22',
    'headshot_url': 'http://en.wikipedia.org/wiki/Yuki_Tsunoda',
    'team_name': 'RB F1 Team',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/racingbulls/yuktsu01/2025racingbullsyuktsu01right.png'
  },
  'GAS': {
    'driverId': 'gasly',
    'dateOfBirth': '1996-02-07',
    'nationality': 'French',
    'name_acronym': 'GAS',
    'last_name': 'Gasly',
    'first_name': 'Pierre',
    'driver_number': '10',
    'headshot_url': 'http://en.wikipedia.org/wiki/Pierre_Gasly',
    'team_name': 'Alpine F1 Team',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/alpine/piegas01/2025alpinepiegas01right.png'
  },
  'BOR': {
    'driverId': 'bortoleto',
    'dateOfBirth': '2004-10-14',
    'nationality': 'Brazilian',
    'name_acronym': 'BOR',
    'last_name': 'Bortoleto',
    'first_name': 'Gabriel',
    'driver_number': '5',
    'headshot_url': 'https://en.wikipedia.org/wiki/Gabriel_Bortoleto',
    'team_name': 'Sauber',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/kicksauber/gabbor01/2025kicksaubergabbor01right.png'
  },
  'COL': {
    'driverId': 'colapinto',
    'dateOfBirth': '2003-05-27',
    'nationality': 'Argentine',
    'name_acronym': 'COL',
    'last_name': 'Colapinto',
    'first_name': 'Franco',
    'driver_number': '43',
    'headshot_url': 'http://en.wikipedia.org/wiki/Franco_Colapinto',
    'team_name': 'Alpine F1 Team',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/alpine/fracol01/2025alpinefracol01right.png'
  },
  'DOO': {
    'driverId': 'doohan',
    'dateOfBirth': '2003-01-20',
    'nationality': 'Australian',
    'name_acronym': 'DOO',
    'last_name': 'Doohan',
    'first_name': 'Jack',
    'driver_number': '7',
    'headshot_url': 'http://en.wikipedia.org/wiki/Jack_Doohan',
    'team_name': 'Alpine F1 Team',
    'picture_url': 'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/2025/alpine/jacdoo01/2025alpinejacdoo01right.png'
  }
}

def extractDriversInfo(year: int):
    driversData = drivers_standing.f_drivers_standing(year)
    driversInfo = {}
    for driver in driversData['DriverStandings']:
        driverId = driver['Driver']['name_acronym']
        teamId = driver['team']['team_id']
        driversInfo[driverId] = driver['Driver']
        driversInfo[driverId]['picture_url'] = testURL(year, driver['Driver']['first_name'], driver['Driver']['last_name'], teamId)

    print (driversInfo)
    return driversInfo


def testURL(year: int, first_name: str, last_name: str, team: str) -> str:
    first_name = first_name[:3].lower()
    last_name = last_name[:3].lower()
    name = f'{first_name}{last_name}01'
    baseURL = f'https://media.formula1.com/image/upload/c_lfill,w_100/q_auto/v1740000000/common/f1/{year}/{team}/{name}/{year}{team}{name}right.png'
    print(baseURL)
    response = fetch.is_valid_image_url(baseURL)
    if response['valid'] and response['status_code'] == 200:
        return baseURL
    return ""

if __name__ == "__main__":
    #year 2025 => 9839
    extractDriversInfo(2025)
