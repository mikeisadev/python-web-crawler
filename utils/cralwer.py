from data.requestheaders import getReqHeaders
from utils.url import getPageName
from bs4 import BeautifulSoup
import requests, os, shutil

'''
Presave here crawling data.
'''
crawlCache: dict    = {}
urlsTree: dict      = {}
crawlDepth: int     = 0
crawledDir: str     = 'crawled'

def startCrawler(
    url: str, 
    options: dict, 
    cmdOptions: dict, 
    crawlData: dict,
    scanChildUrls: bool = False, 
    scanningChild: bool = False, 
    ): 
    '''
    The function to start crawling a web page
    '''
    from utils.utils import saveCrawlData, saveHeaders, saveWebPage
    from utils.mindmap import generateSitemapMindMap

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
        crawlData['internal']['styles'][url] = []
        print(stylesheet['href'])
        crawlData['internal']['styles'][url].append( stylesheet['href'] )

    # JS
    for script in all_scripts:
        crawlData['internal']['scripts'][url] = []
        crawlData['internal']['scripts'][url].append( script['src'] )

    # Hyperlinks:
    urlsTree[url] = {}

    for hyperlink in all_hyperlinks:
        href = hyperlink['href']

        if url in href:
            urlsTree[url][href] = ''
        else:
            crawlData['external'].append(href)

    # Images.
    for image in all_images:
        crawlData['internal']['img'][url] = []
        crawlData['internal']['img'][url].append( image['src'] )

    crawlData['internal']['hrefs'] = urlsTree

    # Do what prompt parameters said
    if not scanningChild:
        crawlData['headers'] = saveHeaders(
            cmdOptions['save']['headers'],
            headers,
            dict(response.headers)
        )                                       if cmdOptions['save']['headers']   else None
        saveCrawlData(crawlData)                if cmdOptions['save']['json']      else None
        generateSitemapMindMap(urlsTree)        if cmdOptions['save']['sitemap']   else None

    pageName = getPageName(url)

    saveWebPage(
        htmlBytes,
        pageName
    ) if cmdOptions['save']['web-page']  else None

    print(url)

    # Scan childs urls.
    if scanChildUrls:
        childUrls = list(urlsTree[url].keys())

        for childUrl in childUrls:
            startCrawler(
                url             = childUrl, 
                options         = options, 
                scanningChild   = True,
                cmdOptions      = cmdOptions,
                _crawlData      = crawlData
            )

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
    Clean the crawled dir
    '''
    for file in os.listdir(crawledDir) :
        path: str = os.path.join(crawledDir, file)

        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print('Error occurred while deleting "%": %' % (path, e))

__all__ = ['startCrawler', 'crawledDirExists', 'createCrawledDir', 'clearCrawledDir']