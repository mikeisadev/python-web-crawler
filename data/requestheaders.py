def getReqHeaders(headers: dict) -> dict:
    '''
    Get request headers from this function.

    Headers can be very important to crawl a web page.

    For example, setting the proper user agent can be crucial for getting errors during the crawl process.

    You could get a 403 HTTP Error (Forbidden) without the proper user agent set in the headers.
    '''
    
    return {
        'User-Agent': headers.get('user-agent'),
        'Content-Type': 'text/html'
    }

__all__ = ['getReqHeaders']