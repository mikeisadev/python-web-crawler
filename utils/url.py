import validators
import re

protocols: list = ('https://', 'http://', 'ftp://')

regex: dict = {
    'protocol': r'([a-z]*(:\/\/))',
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

        urlList['port'] = 443
    else:
        urlList['url'].append('http://')
        url = url.replace('http://', '')

        urlList['port'] = 80

    for _str in url.split('/'):
        urlList['url'].append(_str) if len(_str) > 0 else None

    # Check for port number inside the URL string.
    port = re.search(regex['port'], urlList['url'][1])

    if port:
        urlList['port'] = int( port.group(0)[1:] )

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

def urlDelProt(url: str) -> str:
    return re.sub(regex['protocol'], '', url)

def delLastSlash(url: str) -> str:
    return url[0:-1] if url[-1] == '/' else url

def getPageSlug(url: str) -> str:
    urlList = urlToStructure(url)['url']
    slug = urlList[-1]
    noProt = delLastSlash( urlDelProt(url) )

    return '/' if slug == noProt else slug

def getPageName(url: str, format: str = 'html') -> str:
    urlList = urlToStructure(url)['url']
    slug = urlList[-1]
    noProt = delLastSlash( urlDelProt(url) )

    return f'index.{format}' if slug == noProt else f'{slug}.{format}'

def getHostnameFromUrl(url: str) -> str:
    '''
    From the URL get the hostname + the protocol used before the URL hostname.
    '''
    urlList = urlToStructure(url)['url']

    return (urlList[0] + urlList[1])

# print(getHostnameFromUrl('https://michelemincone.com'))

#print (getPageName('https://michelemincone.com/chi-sono#section-1'))
            
# print( urlHasFragment('https://michelemincone.com/chi-sono#section-1') )

# print( urlToStructure('https://michelemincone.com/chi-sono?h=sedd&s=24#section-1') )

__all__ = ['isUrlHttps', 'extractProtocol', 'urlToStructure', 'isIndexUrl', 'urlHasProtocol', 'urlHasPort', 'urlHasQueryStrings', 'urlHasFragment', 'urlDelProt', 'getPageSlug']