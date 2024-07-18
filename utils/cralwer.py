from data.requestheaders import getReqHeaders
from data.crawldata import crawlData
from bs4 import BeautifulSoup
import requests
import os

def startCrawler(url: str, options: dict): 
    '''
    The function to start crawling a web page
    '''

    headers = getReqHeaders({
        'user-agent': options.get('user-agent')
    })

    response = requests.get(url, headers=headers)
    htmlBytes = response.content

    # Parse HTML
    parsed = BeautifulSoup(htmlBytes, 'html.parser')

    # Find links, scripts, stylesheets
    all_stylesheets = parsed.select('link[rel="stylesheet"][href]')
    all_scripts = parsed.select('script[src]')
    all_hyperlinks = parsed.select('a[href]')
    all_images = parsed.select('img[src]')

    for stylesheet in all_stylesheets:
        crawlData['internal']['styles'].append( stylesheet['href'] )

    for script in all_scripts:
        crawlData['internal']['scripts'].append( script['src'] )

    for hyperlink in all_hyperlinks:
        href = hyperlink['href']

        if url in href:
            crawlData['internal']['hrefs'].append(href)
        else:
            crawlData['external'].append(href)

    for image in all_images:
        crawlData['internal']['img'].append( image['src'] )

    print(response)

    return {
        'headers': {
            'request': headers,
            'response': dict(response.headers)
        },
        'page': {
            'html': htmlBytes
        }
    }

def crawledDirExists(createDirIfNot = False) -> bool:
    '''
    Check if "crawled" dir exists in the current project folder
    '''
    exists = os.path.exists( os.path.join(os.getcwd(), 'crawled') )

    if createDirIfNot:
        createCrawledDir()

    return exists 

def createCrawledDir() -> str: 
    '''
    Create the "crawled" dir on the base path
    '''
    path = os.path.join( os.getcwd(), 'crawled' )

    if not os.path.exists( os.path.join(os.getcwd(), 'crawled') ):
        os.mkdir( path )

    return path

__all__ = ['startCrawler', 'crawledDirExists', 'createCrawledDir']