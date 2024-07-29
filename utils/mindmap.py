from utils.url import urlDelProt, getPageSlug
import pydot

def generateSitemapMindMap(urls: dict, scanningChilds = False, graph = None, root = None) -> any:
    '''
    Generate a mind map from the URL structure inside the dictionary.

    The result will be a sitemap in PNG format where all the nodes of URL will be reported as they are as a real mind map.

    Pydot will be used to generate the mindmap. Pydot is an interface for pygraphviz
    '''
    graph = pydot.Dot(graph_type='graph', rankdir='TD') if not graph else graph

    urlKeys = list(urls.keys())

    if len(urlKeys) == 1 and not root:
        root = urlKeys[0]

    _urls = list( (urls[root]).keys() )

    for _url in _urls:
        edge = urlDelProt(root).split('.')[0] if not scanningChilds else getPageSlug(root)

        graph.add_edge( 
            pydot.Edge( 
                edge, 
                getPageSlug(_url)
            ) 
        )

        # Check for childs URLs for current URL
        childs = urls[root][_url]

        if type(childs) is dict:
            childsTree: dict = { _url: childs }

            graph = generateSitemapMindMap(
                urls=           childsTree, 
                scanningChilds= True, 
                graph=          graph,
                root=           _url
            )

    if scanningChilds:
        return graph
    else:
        graph.write_png('crawled/sitemap.png')