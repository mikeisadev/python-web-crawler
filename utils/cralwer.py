from data.requestheaders    import getReqHeaders
from utils.url              import getPageName, urlToStructure
from utils.dict             import updateTree, getMissingUrlsMinMax
from data.crawldata         import crawlData, crawledPages
from bs4                    import BeautifulSoup
import requests, os, shutil, socket

'''
Presave here crawling data.
'''
crawledDir: str         = 'crawled'
hostnameDir: str        = None
urlTree: dict           = {}
internalUrlCache: tuple = []

def startCrawler(url: str, options: dict, cmdOptions: dict, firstScan: bool = False) -> dict: 
    '''
    The function to start crawling a web page
    '''
    global hostnameDir
    from utils.utils import saveWebPage

    # Clear the crawled folder at first start.
    if not crawlData['in-action']:
        urlStruct = urlToStructure(url)

        if not crawledDirExists():
            createCrawledDir()

        hostnameDir = createHostNameDir(url)

        # serverInfo = socket.getaddrinfo(urlStruct['url'][1], urlStruct['port'])

        # Save IPv4
        crawlData['ip']['v4'] = socket.gethostbyname(urlStruct['url'][1])
        crawlData['ip']['v6'] = None

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

    response = requests.get(url, headers=headers, stream=True)
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

            # print(href)

            if (href == crawlData['root']) or (href == f'{crawlData['root']}/') or (href in internalUrlCache) or ('?' in href):
                if not cmdOptions['save']['duplicate-links']: continue
            
            urlTree[url][href] = '' 

            internalUrlCache.append(href) # Save urls in cache
        else:
            crawlData['external'].append(href)

    # Update URL tree using dict traverse algorithm.
    updateTree(crawlData['internal']['hrefs'], url, urlTree[url])

    # Update the URL list to know which URLs have been crawled
    if url not in crawledPages:
        crawledPages.append(url)

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

    # Crawl depth
    if firstScan and int(crawlData['crawl-depth']) == 0:
        print(f'INDEX CRAWLED - DEPTH: {crawlData['crawl-depth']} - {url}')

        crawlData['crawl-depth'] += 1
    else:
        print(f'PAGE CRAWLED - DEPTH: {crawlData['crawl-depth']} - {url}')
    
    # Return crawl data.
    return {
        'headers': {
            'request': headers,
            'response': dict(response.headers)
        }
    }

def crawlChildUrls(urls: list, options: dict, cmdOptions: dict):
    '''
    Crawl sub pages got from first scan.
    '''
    # Init
    missingUrlsDepth: dict = {}

    # Crawl first scan child URLs
    for url in urls: 
        startCrawler(url, options, cmdOptions, False)

    # Increase crawl depth by one
    crawlData['crawl-depth'] += 1

    # Log crawled pages
    # print(json.dumps( crawledPages, indent=True ) )

    # Log missing URLs
    # print( json.dumps( 
    #     getMissingUrlsMinMax(
    #         crawlData['internal']['hrefs'], 
    #         crawledPages, 
    #         0
    #     ), 
    #     indent=True 
    # ) )

    # Log crawl depth
    # print(crawlData['crawl-depth'])

    '''
    Get missing URLs by depth excluding the already crawled ones.
    '''
    missingUrlsDepth = getMissingUrlsMinMax(
        crawlData['internal']['hrefs'],
        crawledPages,
        0
    )

    # print(cmdOptions)

    # print(json.dumps( missingUrlsDepth, indent=True ))

    while crawlData['crawl-depth'] <= cmdOptions['crawler']['depth']:
        try:
            urls = missingUrlsDepth[ crawlData['crawl-depth'] ]

            # print(json.dumps( urls, indent=True ))

            for url in urls:
                startCrawler(url, options, cmdOptions, False)

            crawlData['crawl-depth'] += 1

            # print(json.dumps(crawlData['crawl-depth']))
        except:
            print(f'Invalid crawl depth! Cannot go depeer than {crawlData['crawl-depth']} levels')
            break

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