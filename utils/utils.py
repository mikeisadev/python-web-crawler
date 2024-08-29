import validators
import json
import codecs

def checkUrlStrict(url) -> str:
    '''
    Check if an URL is valid.
    '''
    if len(url) == 0:
        print('Please insert an URL!')
        return checkUrlStrict( input('Type an URL to crawl: ') )
    
    if not validators.url(url):
        print('Invalid URL!')
        return checkUrlStrict( input('Type an URL to crawl: ') )

    return url

def checkIfInputIsType(i, type, retryText)-> any:
    try:
        match type:
            case 'int': int(i)
            case 'str': str(i)
    except:
        checkIfInputIsType( input(retryText), type, retryText )
    
    return i

def saveWebPage(html: bytes, name: str = 'index.html', enc = 'utf-8') -> bool:
    '''
    Save a web page.
    '''
    from utils.cralwer import hostnameDir

    f = open(f'{hostnameDir}\\{name}', mode='w', encoding='utf8')
    f.write(codecs.decode(html, encoding='utf-8', errors='backslashreplace'))
    f.close()

    return True

def saveCrawlData(crawlData: dict, format: str = 'json') -> bool:
    '''
    Save the crawl data from dictionary to preferred format (as json)
    '''
    from utils.cralwer import hostnameDir

    formats = ('json', 'xml', 'csv')

    if format not in formats:
        raise Exception(f'Invalid format! These are valid formats {' '.join(formats)}')

    f = open( f'{hostnameDir}\\crawldata.{format}', "w")

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
        case 'all' | '--all-headers':
            headers['request'] = reqHeaders
            headers['response'] = resHeaders
        case 'request-headers' | '--res-headers':
            headers['request'] = reqHeaders
        case 'response-headers' | '--req-headers':
            headers['response'] = resHeaders

    return headers

__all__ = ['checkUrlStrict', 'saveHeaders', 'saveWebPage', 'saveCrawlData']