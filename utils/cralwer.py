from data.requestheaders    import getReqHeaders
from utils.url              import getPageName, urlToStructure
from utils.dict             import updateTree
from data.crawldata         import crawlData
from bs4                    import BeautifulSoup
import requests, os, shutil

'''
Presave here crawling data.
'''
crawledDir: str         = 'crawled'
hostnameDir: str        = None
urlTree: dict           = {}
internalUrlCache: tuple = []

def startCrawler(url: str, options: dict, cmdOptions: dict, scanningChilds: bool = False)-> dict: 
    '''
    The function to start crawling a web page
    '''
    global hostnameDir
    from utils.utils import saveWebPage

    # Clear the crawled folder at first start.
    if not crawlData['in-action']:
        if not crawledDirExists():
            createCrawledDir()

        hostnameDir = createHostNameDir(url)

        clearCrawledDir()
        

    # Set the status of the crawler
    if not crawlData['in-action']:
        crawlData['in-action'] = True

    # Set up root url
    if not crawlData['root']: crawlData['root'] = url

    # Get request headers.
    headers = getReqHeaders({
        'user-agent': options.get('user-agent')
    })

    response = requests.get(url, headers=headers)
    htmlBytes = response.content

    # Parse HTML
    parsed = BeautifulSoup(htmlBytes, 'html.parser')

    # Find links, scripts, stylesheets
    all_stylesheets = parsed.select('link[rel="stylesheet"][href]')
    all_scripts     = parsed.select('script[src]')
    all_hyperlinks  = parsed.select('a[href]')
    all_images      = parsed.select('img[src]')

    # CSS
    for stylesheet in all_stylesheets:
        if url not in crawlData['internal']['styles'].keys():
            crawlData['internal']['styles'][url] = []

        crawlData['internal']['styles'][url].append( stylesheet['href'] )

    # JS
    for script in all_scripts:
        if url not in crawlData['internal']['scripts'].keys():
            crawlData['internal']['scripts'][url] = []

        crawlData['internal']['scripts'][url].append( script['src'] )

    # Hyperlinks:
    urlTree[url] = {}

    for hyperlink in all_hyperlinks:
        href = hyperlink['href']

        if crawlData['root'] in href:

            print(href)

            if (href == crawlData['root']) or (href == f'{crawlData['root']}/') or (href in internalUrlCache) or ('?' in href):
                if not cmdOptions['save']['duplicate-links']: continue
            
            urlTree[url][href] = '' 

            internalUrlCache.append(href) # Save urls in cache
        else:
            crawlData['external'].append(href)

    # Update URL tree using dict traverse algorithm.
    updateTree(crawlData['internal']['hrefs'], url, urlTree[url])

    # Images.
    for image in all_images:
        if url not in crawlData['internal']['img'].keys():
            crawlData['internal']['img'][url] = []

        crawlData['internal']['img'][url].append( image['src'] )

    # Save web page
    pageName = getPageName(url)

    saveWebPage(
        htmlBytes,
        pageName
    ) if cmdOptions['save']['web-page'] else None

    print(f'{url} - {pageName}')
    
    # Return crawl data.
    return {
        'headers': {
            'request': headers,
            'response': dict(response.headers)
        }
    }

def crawlChildUrls(urls: list, options: dict, cmdOptions: dict):
    '''
    Crawl sub pages.
    '''
    for url in urls: startCrawler(url, options, cmdOptions)

def crawledDirExists(createDirIfNot = False) -> bool:
    '''
    Check if "crawled" dir exists in the current project folder
    '''
    exists = os.path.exists( os.path.join(os.getcwd(), crawledDir) )

    if createDirIfNot:
        createCrawledDir()

    return exists 

def createCrawledDir() -> str: 
    '''
    Create the "crawled" dir on the base path
    '''
    path = os.path.join( os.getcwd(), 'crawled' )

    if not os.path.exists( os.path.join(os.getcwd(), crawledDir) ):
        os.mkdir( path )

    return path

def clearCrawledDir() -> bool:
    '''
    Clean the crawled dir for the current working hostname dir.
    '''
    print(hostnameDir)
    for file in os.listdir( hostnameDir ) :
        path: str = os.path.join(hostnameDir, file)

        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print('Error occurred while deleting "%": %' % (path, e))

def createHostNameDir(url: str) -> str:
    '''
    Create a directory with the name of the inserted hostname
    '''
    struct = urlToStructure(url)
    hostname = struct['url'][1]

    path = os.path.join('crawled', hostname)

    if not os.path.exists( path ):
        os.mkdir(path)

    return path

__all__ = ['startCrawler', 'crawledDirExists', 'createCrawledDir', 'clearCrawledDir', 'crawlChildUrls', 'crawledDir', 'hostnameDir', 'createHostNameDir']