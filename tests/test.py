import json

urls: dict = {
        "https://michelemincone.com": {
                "https://michelemincone.com/photogallery-tesi/": "",
                "https://michelemincone.com/stampa-documento/": "",
                "https://michelemincone.com/registrati": "",
                "https://michelemincone.com/mio-account": "",
                "https://michelemincone.com/privacy-policy/": "",
                "https://michelemincone.com/cookie-policy/": "",
                "https://michelemincone.com/termini-e-condizioni/": {
                        "https://michelemincone.com/termini-e-condizioni/abc": "",
                        "https://michelemincone.com/termini-e-condizioni/abc123": {
                                "https://michelemincone.com/termini-e-condizioni/abc123/hello0" : "",
                                "https://michelemincone.com/termini-e-condizioni/abc123/hello1" : "",
                                "https://michelemincone.com/termini-e-condizioni/abc123/hello2" : "",
                                "https://michelemincone.com/termini-e-condizioni/abc123/hello3" : "",
                                "https://michelemincone.com/termini-e-condizioni/abc123/hello4" : {
                                        "https://michelemincone.com/termini-e-condizioni/abc123/hello4/ciao" : {
                                            "https://michelemincone.com/termini-e-condizioni/abc123/hello4/ciao/c": "" 
                                        }
                                },
                                "https://michelemincone.com/termini-e-condizioni/abc123/hello5" : ""
                        },
                        "https://michelemincone.com/termini-e-condizioni/abc1233": "",
                },
                "https://michelemincone.com/segnalazione-bug/": ""
        }
}

crawledUrls: tuple = ['https://michelemincone.com', 'https://michelemincone.com/photogallery-tesi/', 'https://michelemincone.com/stampa-documento/','https://michelemincone.com/registrati','https://michelemincone.com/mio-account','https://michelemincone.com/privacy-policy/','https://michelemincone.com/cookie-policy/',]

c: int = 0 # URL count
d: int = 0 # DEPTH count
miss: dict = {}
rUrls: tuple = []
maxDepth: int = 4

def returnUrlsInTree(tree: dict, getUrlOfDepth: int|bool = False)-> dict|None:
        '''
        Return URLS of a certain tree depth. Very useful when you have to know the exact 
        crawl depth.
        '''
        global c, d, miss, rUrls

        url:    str        = ''

        for k, v in tree.items():
                # Depth 0 and URL 0 = INDEX
                if c==0 and d==0:
                        print(f'INDEX - DEPTH {d}', k)

                # Scan the value
                if type(v) is dict and len(v.items()) > 0:
                        if c != 0 and c != 1: url = k

                        d += 1
                        rUrls = returnUrlsInTree(v, getUrlOfDepth)
                        d -= 1

                # Get the url from key
                else: url = k

                # If we are in root url
                if d==0:
                        if d == getUrlOfDepth:
                                rUrls.append(k)

                # If we are not in the root url, go next getting URLs.
                if d!=0:
                        c+=1
                        # print(f'DEPTH {d} - {url}')

                        if d == getUrlOfDepth:
                                rUrls.append(url)
        
        return rUrls

def treeDepth(tree: dict) -> int:
        '''
        Calc the depth of a tree.
        '''
        if not isinstance(tree, dict): return 0
        return 1 + (max(map(treeDepth, tree.values())) if tree else 0)

def getMissingUrlsInTree(tree:dict, crawdUrls: list|tuple, maxDepth: int)-> tuple:
        '''
        Get a tuple of missing URLs to be crawled in a certain crawl depth.
        '''
        urls = returnUrlsInTree(tree, maxDepth)

        missing: tuple = []

        for url in urls:
                missing.append(url) if url not in crawdUrls else None

        return missing

def getMissingUrlsMinMax(tree:dict, crawdUrls: list|tuple|bool, minDepth: int = 0):
        '''
        With this function you can enter an url tree and return a dictionary with depth as key and urls as value.
        '''
        global rUrls

        # Init
        c: int          = minDepth              # Count. From minDepth.
        maxTreeDepth: int   = (treeDepth(tree) - 1) # Max depth
        urlsDepth: dict = {} 

        while True:
                if crawdUrls:
                        urlsDepth[c] = getMissingUrlsInTree( tree, crawdUrls, c )
                else:
                        urlsDepth[c] = returnUrlsInTree(tree, c)

                #print(json.dumps(returnUrlsInTree(tree, c), indent=True))

                rUrls = []
                c+=1

                if c > maxTreeDepth: break # Or replace True in while loop with c <= maxTreeDepth
        
        return urlsDepth

# print( json.dumps( returnUrlsInTree(urls, True, 2) ) )

print( json.dumps( getMissingUrlsMinMax(urls, crawledUrls, 0), indent=True))

# print( json.dumps( getMissingUrlsInTree(urls, crawledUrls, 1) ) )