# Data structures of crawling
crawlData: dict = {
    'in-action': False,
    'errors': None,
    'root': None,
    'crawl-depth': 0,
    'ip': {
        'v4': None,
        'v6': None
    },
    'internal': {
        'hrefs': {},
        'img': {},
        'scripts': {},
        'styles': {}
    },
    'external': []
}

# Downloaded and Crawled Pages.
crawledPages: tuple = []

__all__ = ['crawlData', 'crawledPages']