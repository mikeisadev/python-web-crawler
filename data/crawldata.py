# Data structures of crawling
crawlData: dict = {
    'root': None,
    'internal': {
        'hrefs': {},
        'img': {},
        'scripts': {},
        'styles': {}
    },
    'external': []
}

__all__ = ['crawlData']