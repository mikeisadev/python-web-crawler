from data.useragents    import USER_AGENTS, getUserAgent
from utils.utils        import checkUrlStrict, saveHeaders, saveCrawlData
from cli.commands       import commandInPrompt
from cli.prompts        import prompts
from utils.cralwer      import startCrawler, crawlChildUrls
from data.crawldata     import crawlData
from utils.mindmap      import generateSitemapMindMap
import sys
import questionary

# NOTE: Save this inside a function or class (in the future) and call everything inside a non .py file to avoid typing the extension, call the file directy (py crawl) instead of (py crawl.py)

# Init data.
url: str                  = ''
args: list                = sys.argv
askAll: bool              = False
save: bool                = False
saveJson: bool            = False
saveSitemap: bool         = False
userAgent: bool           = USER_AGENTS['moz']['moz5-mac'] # Set a default user agent
customUserAgent: bool     = False
saveTheHeaders: bool|str  = False

# Getting data (if -> prompt, else -> prompt line)
if (len(args) == 1):
    url = checkUrlStrict( input('Type an URL to crawl: ') ) # Get and validate URL

    askAll = True if input('Ask all questions to configure the crawl options: ') == 'yes' else False

    if askAll:
        save            = True if input('Do you want to save this page: ') == 'yes' else False
        saveJson        = True if input('Do you want to save crawl data as JSON: ') == 'yes' else False
        saveSitemap     = True if input('Do you want to get the sitemap of the website: ') == 'yes' else False
        customUserAgent = True if input('Do you want to set a custom User Agent? ') == 'yes' else False

        # Custom user agent selection process
        if customUserAgent:
            userAgent = getUserAgent( input('Insert the model of the user agent you want: ') )

        saveTheHeaders = True if input('Do you want to save headers? ') == 'yes' else False

        # Saving headers process
        if saveTheHeaders:
            saveTheHeaders = questionary.select(
                'Which headers do you want to select',
                prompts.get('save-headers')
            ).ask()

            print(f'Perfect! You selected {saveTheHeaders} for header saving process...')
else:
    url             = checkUrlStrict( args[1] )

    save            = commandInPrompt(args, 'save')
    saveTheHeaders  = commandInPrompt(args, 'headers', True)
    saveJson        = commandInPrompt(args, 'json')
    saveSitemap     = commandInPrompt(args, 'sitemap')
    
# Start the crawl process
requestOptions: dict = {
    'user-agent': userAgent
}

request = startCrawler(
    url             = url,
    options         = requestOptions,
    saveWebPage     = True
)

# Crawl child URLs
crawlChildUrls(
    list(crawlData['internal']['hrefs'][url].keys()),
    requestOptions,
    saveWebPage= True
)

# Save headers.
crawlData['headers'] = saveHeaders(
        saveTheHeaders,
        request['headers']['request'],
        request['headers']['response']
)                                                       if saveTheHeaders   else None
saveCrawlData(crawlData)                                if saveJson         else None
generateSitemapMindMap(crawlData['internal']['hrefs'])  if saveSitemap      else None

print('Web page crawled successfully!')