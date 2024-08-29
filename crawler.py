'''
Simple Web Crawler and Analyzer in Python - Multitool

Realized by Michele Mincone - 15/07/2024 - Italy

Short description:
This is a simple web crawler and analyzer (multi tool) to scan the web page you insert as URL. This web crawler can go deep scanning child URLS (and child urls of child ones).

For each scanned URL you can decide to save the web page in HTML format, get CSS, JS, IMG and font files.

In the future this crawler will have much more powerful tools you can calibrate through cmd commands or interface. There will be also a GUI for this crawler to have a much more simplified interface to use this tool, but this will be available in a higher version.

You can calibrate this web crawler choosing multiple commands (you can find inside "/cli/commands.py").

In the future this code will be exectuable with a runnable Dockerfile to avoid installing each component in Python.

I have to say a lot about this web crawler, but you'll find more inside readme file.
'''

from data.useragents    import USER_AGENTS, getUserAgent
from utils.utils        import checkUrlStrict, saveHeaders, saveCrawlData
from cli.commands       import commandInPrompt
from cli.prompts        import prompts
from utils.cralwer      import startCrawler, crawlChildUrls
from data.crawldata     import crawlData, crawledPages
from utils.mindmap      import generateSitemapMindMap
import sys
import questionary

# NOTE: Save this inside a function or class (in the future) and call everything inside a non .py file to avoid typing the extension, call the file directy (py crawl) instead of (py crawl.py)

# Init data.
url: str                  = ''
args: list                = sys.argv
askAll: bool              = False
save: bool                = False
saveJson: bool            = True
saveSitemap: bool         = False
userAgent: bool           = USER_AGENTS['moz']['moz5-mac'] # Set a default user agent
customUserAgent: bool     = False
saveTheHeaders: bool|str  = False
saveDupLinks              = False
_crawlDepth: bool|int     = False

# Getting data (if -> prompt, else -> prompt line)
if (len(args) == 1):
    url = checkUrlStrict( input('Type an URL to crawl: ') ) # Get and validate URL

    askAll = True if input('Ask all questions to configure the crawl options (yes/no): ') == 'yes' else False

    if askAll:
        save            = True if input('Do you want to save this page (yes/no): ') == 'yes' else False
        saveJson        = True if input('Do you want to save crawl data as JSON (yes/no): ') == 'yes' else False
        saveSitemap     = True if input('Do you want to get the sitemap of the website (yes/no): ') == 'yes' else False
        customUserAgent = True if input('Do you want to set a custom User Agent? (yes/no) ') == 'yes' else False

        # Custom user agent selection process
        if customUserAgent:
            userAgent = getUserAgent( input('Insert the model of the user agent you want (opera-38/opera-980): ') )

        saveTheHeaders = True if input('Do you want to save headers? (yes/no) ') == 'yes' else False

        # Saving headers process
        if saveTheHeaders:
            saveTheHeaders = questionary.select(
                'Which headers do you want to select',
                prompts.get('save-headers')
            ).ask()

            print(f'Perfect! You selected {saveTheHeaders} for header saving process...')
        
        # Save duplicate links.
        saveDupLinks = True if input('Do you want to save duplicate links (useful for internal linking analysis)? (yes/no)') else False

        # Get the crawl depth
        if 'yes' == input('Do you want to set a crawl depth? (yes/no) '):
            _crawlDepth = int(input('Set a crawl depth inserting a number (insert a number): '))

else:
    url             = checkUrlStrict( args[1] )

    save            = commandInPrompt(args, 'save')
    userAgent       = getUserAgent( commandInPrompt(args, 'user-agent') )
    saveTheHeaders  = commandInPrompt(args, 'headers', True)
    saveJson        = commandInPrompt(args, 'json')
    saveSitemap     = commandInPrompt(args, 'sitemap')
    saveDupLinks    = commandInPrompt(args, 'duplicate-links')
    _crawlDepth     = int( commandInPrompt(args, 'crawl-depth') )

# Start the crawl process
requestOptions: dict = {
    'user-agent': userAgent
}

cmdOptions: dict = {
    'save': {
        'web-page'          : save,
        'duplicate-links'   : saveDupLinks
    },
    'crawler': {
        'depth': _crawlDepth
    }
}

request = startCrawler(
    url             = url,
    options         = requestOptions,
    cmdOptions      = cmdOptions,
    firstScan       = True
)

# Crawl child URLs
crawlChildUrls(
    urls            = list(crawlData['internal']['hrefs'][url].keys()),
    options         = requestOptions,
    cmdOptions      = cmdOptions
)

# Save headers.
crawlData['headers'] = saveHeaders(
    saveTheHeaders,
    request['headers']['request'],
    request['headers']['response']
)                                                       if saveTheHeaders   else None
saveCrawlData(crawlData)                                if saveJson         else None
generateSitemapMindMap(crawlData['internal']['hrefs'])  if saveSitemap      else None

print(
    f'Web page crawled successfully!' 
    if len(crawledPages) < 2 else 
    f'Website crawled successfully (total crawl depth {crawlData['crawl-depth']})'
)