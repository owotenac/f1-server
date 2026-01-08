import asyncio
from urllib.request import urlparse
import requests
import fetch

height = 400


racePictureURLs = {
'Sakhir' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Sakhir_Circuit.png',
'Melbourne' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackMelbournedetailed.png',
'Shanghai' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackShanghaidetailed.png',
'Suzuka' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackSuzukadetailed.png',
'Jeddah' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackJeddahdetailed.png',
'Miami' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.png',
'Imola' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackImoladetailed.png',
'Monaco' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monaco_Circuit.png',
'Barcelona' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackCatalunyadetailed.png',
'Montréal' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackMontréaldetailed.png',
'Spielberg' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackSpielbergdetailed.png',
'Silverstone' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackSilverstonedetailed.png',
'Spa-Francorchamps' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit.png',
'Budapest' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackHungaroringdetailed.png',
'Zandvoort' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackZandvoortdetailed.png',
'Monza' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackMonzadetailed.png',
'Baku' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Baku_Circuit.png',
'Marina Bay' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Singapore_Circuit.png',
'Austin' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackAustindetailed.png',
'Mexico City' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit.png',
'São Paulo' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackInterlagosdetailed.png',
'Las Vegas' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Las_Vegas_Circuit.png',
'Lusail' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2025/track/2025trackLusaildetailed.png',
'Yas Marina' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2026/track/2026trackyasmarinacircuitdetailed.png',
'Miami Gardens' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Miami_Circuit.png',
'Monte Carlo' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Monaco_Circuit.png',
'Madrid' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2026/track/2026trackMadriddetailed.png',
'Yas Island' : 'https://media.formula1.com/image/upload/c_fit,h_400/q_auto/v1740000000/common/f1/2026/track/2026trackyasmarinacircuitdetailed.png',
}


def extractRacePictureURL(year: int):
    params = {
        'year': year
    }
    response = asyncio.run(fetch.api_call('https://api.openf1.org/v1/meetings', params=params))

    for r in response:
        pictureURL = getRacesPicture(r)
        print(f"\'{r['location']}\' : \'{pictureURL}\',")


def getRacesPicture(race : dict) -> str:

    year = race['year']

    #first we test with the location
    raceName = race['location'].replace(" ","_").replace("-","_")
    r = testURL1(raceName)
    if r != "":
        return r
    #then we test with the location for the new url
    r = testURL2(year,raceName)
    if r != "":
        return r
    
    #then we test with the circuit short name    
    raceName = race['circuit_short_name'].replace(" ","_").replace("-","_")
    r = testURL1(raceName)
    if r != "":
        return r
    r = testURL2(year,raceName)
    if r != "":
        return r
    
    #then we test with the country name
    raceName = race['country_name'].replace(" ","_").replace("-","_")
    r = testURL1(raceName)
    if r != "":
        return r
    r = testURL2(year,raceName)
    if r != "":
        return r
    
    return ""

def testURL1(raceName: str) -> str:
    baseURL = f'https://media.formula1.com/image/upload/c_fit,h_{height}/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/{raceName}_Circuit.png'
    response = is_valid_image_url(baseURL)
    if response['valid'] and response['status_code'] == 200:
        return baseURL
    return ""

def testURL2(year: int, raceName: str) -> str:
    baseURL = f'https://media.formula1.com/image/upload/c_fit,h_{height}/q_auto/v1740000000/common/f1/{year}/track/{year}track{raceName}detailed.png'
    response = is_valid_image_url(baseURL)
    if response['valid'] and response['status_code'] == 200:
        return baseURL
    return ""

def is_valid_image_url(url, timeout=5):
    """
    Test if a URL is valid and points to an image without downloading it.
    
    Args:
        url: The URL to test
        timeout: Request timeout in seconds (default: 5)
    
    Returns:
        dict: Contains 'valid' (bool), 'status_code' (int), 'content_type' (str), 'message' (str)
    """
    try:
        # Validate URL format
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return {
                'valid': False,
                'status_code': None,
                'content_type': None,
                'message': 'Invalid URL format'
            }
        
        # Make HEAD request (doesn't download the body)
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        
        # Check status code
        if response.status_code != 200:
            return {
                'valid': False,
                'status_code': response.status_code,
                'content_type': response.headers.get('Content-Type'),
                'message': f'HTTP {response.status_code}'
            }
        
        # Check content type
        content_type = response.headers.get('Content-Type', '').lower()
        is_image = content_type.startswith('image/')
        
        return {
            'valid': is_image,
            'status_code': response.status_code,
            'content_type': content_type,
            'message': 'Valid image URL' if is_image else f'Not an image (Content-Type: {content_type})'
        }
        
    except requests.exceptions.Timeout:
        return {
            'valid': False,
            'status_code': None,
            'content_type': None,
            'message': 'Request timeout'
        }
    except requests.exceptions.ConnectionError:
        return {
            'valid': False,
            'status_code': None,
            'content_type': None,
            'message': 'Connection error'
        }
    except Exception as e:
        return {
            'valid': False,
            'status_code': None,
            'content_type': None,
            'message': f'Error: {str(e)}'
        }


# Example usage
if __name__ == "__main__":
    extractRacePictureURL(2026)
