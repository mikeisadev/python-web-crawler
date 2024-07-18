from useragents import USER_AGENTS, getUserAgent
from utils import checkUrlStrict, saveWebPage, saveCrawlData, saveHeaders
from commands import commandInPrompt
from prompts import prompts
import requests
import sys
from bs4 import BeautifulSoup
import questionary

# NOTE: Save this inside a function or class (in the future) and call everything inside a non .py file to avoid typing the extension, call the file directy (py crawl) instead of (py crawl.py)

# Init data.
url: str                = ''
args: list              = sys.argv
askAll: bool            = False
save: bool              = False
saveJson: bool          = False
getSitemap: bool        = False
userAgent: bool         = USER_AGENTS['moz']['moz5-mac'] # Set a default user agent
customUserAgent: bool   = False
saveTheHeaders: bool|str   = False

# Data structures of crawling
crawlData: dict = {
    'internal': {
        'sitemap': [],
        'hrefs': [],
        'img': [],
        'scripts': [],
        'styles': []
    },
    'external': []
}

# Getting data (if -> prompt, else -> prompt line)
if (len(args) == 1):
    url = checkUrlStrict( input('Type an URL to crawl: ') ) # Get and validate URL

    askAll = True if input('Ask all questions to configure the crawl options: ') == 'yes' else False

    if askAll:
        save = True if input('Do you want to save this page: ') == 'yes' else False
        saveJson = True if input('Do you want to save crawl data as JSON: ') == 'yes' else False
        getSitemap = True if input('Do you want to get the sitemap of the website: ') == 'yes' else False
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
    url = args[1]
    save = commandInPrompt(args, 'save')
    saveJson = commandInPrompt(args, 'json')
    getSitemap = commandInPrompt(args, 'sitemap')

# Crawl URL
# If you remove this, you can get an error like 403 because you can be recognized as bot.
headers = {
    'User-Agent': userAgent,
    'Content-Type': 'text/html'
}

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

# Do what prompt parameters said
crawlData['headers'] = saveHeaders(
    saveTheHeaders,
    headers,
    dict(response.headers)
)                           if saveTheHeaders   else None
saveWebPage(htmlBytes)      if save             else None
saveCrawlData(crawlData)    if saveJson         else None

# print(crawlData['internal']['hrefs'])

print('Web page crawled successfully!')