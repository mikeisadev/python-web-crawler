def missingUrlsInTree(tree: dict, crawdURLS: tuple, depth: int, stopOnDepth = False, stopOnMissUrlsFound: bool = False)-> dict|None:
        '''
        An algorithm to parse and update an URL tree.
        '''
        global c, d, miss

        url: str   = ''

        for k, v in tree.items():

                # Find the index URL. depth 0 and count url 0
                if type(k) is str and c==0 and d==0:
                        print(f'INDEX - URL {c} - DEPTH {d}', k)

                # Scan the value
                if type(v) is dict and len(v.items()) > 0:
                        if c != 0 and c != 1: url = k

                        d += 1
                        miss = missingUrlsInTree(v, crawdURLS, depth= d)

                        # Get urls on a certain Crawl Depth.
                        if d == stopOnDepth:
                                return url
                
                        d -= 1

                # Get the url from key
                else: url = k

                # If we are not in the root url, go next getting URLs.
                if d!=0:
                        c+=1
                        # print(f'URL {c} - DEPTH {d}', url, '\n\n')

                        '''
                        We need to get not scanned URLs.

                        This can be the key or the value of the dictionary.

                        If it is the key we need to get all the keys of that depth level.

                        Otherwise we get the values.
                        '''
                        if stopOnMissUrlsFound:
                        # if url not in crawdURLS and k not in crawdURLS:
                                miss = {
                                        'missed': url,
                                        'depth' : d
                                }
        if stopOnDepth:
                return url
        
        return miss