def updateTree(tree, key, value):
        '''
        An algorithm to parse and update an URL tree.
        '''
        if len(tree) == 0:
                tree[key] = value
                return 
        
        for k, v in tree.items():
                if key in k:
                        if k in value:
                                del value[k]
                        
                        tree[k] = value if len(value) > 1 else ''

                elif type(v) is dict:
                        tree[k] = updateTree(v, key, value)

        return tree

def treeDepth(tree: dict) -> int:
        '''
        Calc the depth of a tree.
        '''
        if not isinstance(tree, dict): return 0
        return 1 + (max(map(treeDepth, tree.values())) if tree else 0)

'''
The functions from here below becomes more and more specific and they use global variables declared in global scope.

This is made for memory reference purposes.

For example, the algo "returnUrlsInTree", uses external variables to elaborate data like:
- "c" to take count of URLs
- "d" to take count of the depth of the dictionary
- "miss" to collect missed urls in the crawling process comparing to the effectively crawled URLs.
- "rUrls" (or returning urls) to collect the urls to be analized


'''
c:        int   = 0 # URL count
d:        int   = 0 # DEPTH count
miss:     dict  = {}
rUrls:    tuple = []
maxDepth: int   = 4

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
                        #print(f'INDEX - DEPTH {d}', k)
                        None

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
        _c:            int       = minDepth              # Count. From minDepth.
        maxTreeDepth:  int       = (treeDepth(tree) - 1) # Max depth
        urlsDepth:     dict      = {} 

        while True:
                if crawdUrls:
                        urlsDepth[_c] = getMissingUrlsInTree( tree, crawdUrls, _c )
                else:
                        urlsDepth[_c] = returnUrlsInTree(tree, _c)

                #print(json.dumps(returnUrlsInTree(tree, c), indent=True))

                rUrls = []
                _c+=1

                if _c > maxTreeDepth: break # Or replace True in while loop with c <= maxTreeDepth
        
        return urlsDepth

####### EXPORTING ######
__all__ = ['updateTree', 'treeDepth', 'getMissingUrlsMinMax']