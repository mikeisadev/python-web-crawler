# Data structures of crawling
crawlData: dict = {
    'in-action': False,
    'errors': None,
    'root': None,
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

__all__ = ['crawlData']