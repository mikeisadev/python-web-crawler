from data.useragents import USER_AGENTS, getUserAgent
from data.crawldata import crawlData
from utils.utils import checkUrlStrict
from cli.commands import commandInPrompt
from cli.prompts import prompts
from utils.cralwer import startCrawler
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
    url             = args[1]

    url             = checkUrlStrict(url)

    save            = commandInPrompt(args, 'save')
    saveTheHeaders  = commandInPrompt(args, 'headers', True)
    saveJson        = commandInPrompt(args, 'json')
    saveSitemap     = commandInPrompt(args, 'sitemap')
    
# Start the crawl process
startCrawler(
    url=url,
    options={
        'user-agent': userAgent
    },
    cmdOptions={
        'save': {
            'headers': saveTheHeaders,
            'web-page': save,
            'json': saveJson,
            'sitemap': saveSitemap
        }
    },
    crawlData=crawlData,
    scanChildUrls=True,
    scanningChild=False
)

print(crawlData)

print('Web page crawled successfully!')