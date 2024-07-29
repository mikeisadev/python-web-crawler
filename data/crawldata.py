# Data structures of crawling
crawlData: dict = {
    'root': None,
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