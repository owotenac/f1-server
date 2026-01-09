import aiohttp
import requests
from urllib.request import urlparse

async def api_call(url: str, params: dict = None):
    headers = {
        "Accept": "application/json",
    }
    print(f"Fetching URL: {url} with params: {params}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            return data
        



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