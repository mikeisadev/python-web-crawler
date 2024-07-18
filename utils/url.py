import validators
import re

protocols: list = ('https://', 'http://', 'ftp://')

regex: dict = {
    'protocol': r'([a-z]+[://]+)',
    'port'    : r'([:][0-9]+)'
}

def isUrlHttps(url: str) -> bool:
    '''
    Check if the given URL is with the HTTPS protocol or not
    '''
    return True if 'https://' in url else False

def extractProtocol(url: str) -> str|None:
    '''
    Extract the protocol from the URL.
    '''
    found = re.search(regex['protocol'], url)

    if found and found.group(0) in protocols:
        return found.group(0)
    else:
        return None

def urlToStructure(url: str) -> dict:
    '''
    Convert url string to a data structure with all the data: protocol, url, query, port and fragment
    '''
    if not validators.url(url):
        raise Exception('Invalid URL! Please enter a valid URL to be converted into a data structure')
    
    urlList: dict = {
        'protocol': None,
        'url': [],
        'query': {},
        'port': None,
        'fragment': None
    }

    # Get protocol
    urlList['protocol'] = extractProtocol(url)

    # Build URL
    if isUrlHttps(url):
        urlList['url'].append('https://')
        url = url.replace('https://', '')
    else:
        urlList['url'].append('http://')
        url = url.replace('http://', '')

    for _str in url.split('/'):
        urlList['url'].append(_str) if len(_str) > 0 else None

    # Check for port number
    port = re.search(regex['port'], urlList['url'][1])

    if port:
        urlList['port'] = int( port.group(0)[1:] )
    else:
        urlList['port'] = 443 if isUrlHttps(url) else 80

    # Fragment.
    if '#' in urlList['url'][-1]:
        frag = urlList['url'][-1].split('#')
        urlList['fragment'] = frag.pop(-1)

        urlList['url'][-1] = frag[0]

    # Check for query string
    if '?' in (urlList['url'][-1]):
        queryPairs = urlList['url'][-1].split('?')

        urlList['url'][-1] = queryPairs.pop(0)

        queryPairs = queryPairs[0]

        for args in queryPairs.split('&'):
            argsList = args.split('=')

            urlList['query'][argsList[0]] = argsList[1]

    return urlList

def isIndexUrl(url: str) -> bool:
    '''
    An utility function to check if the given URL returns to the index page
    '''
    urlList = ( urlToStructure(url) )['url']

    return True if len(urlList) == 2 else False

def urlHasProtocol(url: str) -> bool:
    prot = re.search(regex['protocol'], url)
    
    return True if prot and prot.group(0) in protocols else False

def urlHasPort(url: str) -> bool:
    return True if re.search(regex['port'], url) else False

def urlHasQueryStrings(url: str) -> bool:
    return True if urlToStructure(url)['query'] else False

def urlHasFragment(url: str) -> bool:
    return True if urlToStructure(url)['fragment'] else False

# print( urlHasFragment('https://michelemincone.com/chi-sono#section-1') )

# print( urlToStructure('https://michelemincone.com/chi-sono?h=sedd&s=24#section-1') )

print(urlToStructure("https://michelemincone.com/wp-content/plugins/google-analytics-for-wordpress/assets/js/frontend-gtag.min.js?ver=8.28.0"))

__all__ = ['isUrlHttps', 'extractProtocol', 'urlToStructure', 'isIndexUrl', 'urlHasProtocol', 'urlHasPort', 'urlHasQueryStrings', 'urlHasFragment']