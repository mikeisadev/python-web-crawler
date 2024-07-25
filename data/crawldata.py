# Data structures of crawling
crawlData: dict = {
    'internal': {
        'sitemap': [],
        'hrefs': {},
        'img': {},
        'scripts': {},
        'styles': {}
    },
    'external': []
}

__all__ = ['crawlData']