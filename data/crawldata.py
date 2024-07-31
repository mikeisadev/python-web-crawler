# Data structures of crawling
crawlData: dict = {
    'in-action': False,
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