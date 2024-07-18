from utils.cralwer import createCrawledDir
import validators
import json

def checkUrlStrict(url) -> str:
    '''
    Check if an URL is valid.
    '''
    if not validators.url(url):
        print('Invalid URL!')
        return checkUrlStrict( input('Type an URL to crawl: ') )

    return url

def saveWebPage(html: bytes, name: str = 'index.html', enc = 'utf-8') -> bool:
    '''
    Save a web page.
    '''
    path = createCrawledDir()

    f = open(f'{path}\{name}', "w")
    f.write(html.decode())
    f.close()

    return True

def saveCrawlData(crawlData: dict, format: str = 'json') -> bool:
    '''
    Save the crawl data from dictionary to preferred format (as json)
    '''
    path = createCrawledDir()

    formats = ('json', 'xml', 'csv')

    if format not in formats:
        raise Exception(f'Invalid format! These are valid formats {' '.join(formats)}')

    f = open( f'{path}\crawldata.{format}', "w")

    match format:
        case 'json':
            f.write( json.dumps( crawlData, indent=8 ) )

    f.close()

    return True

def saveHeaders(arg, reqHeaders, resHeaders) -> dict:
    '''
    Return the requested headers in a key-value (dictionary) structure.
    '''
    headers: dict = {}

    match(arg):
        case 'all':
            headers['request'] = reqHeaders
            headers['response'] = resHeaders
        case 'request-headers':
            headers['request'] = reqHeaders
        case 'response-headers':
            headers['response'] = resHeaders

    return headers

__all__ = ['checkUrlStrict', 'saveHeaders']