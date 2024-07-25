"""
    Here there is a list of user agents that you can use with this crawler.

    You can add your favourite user agents.

    These user agents are taken from:
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
"""
USER_AGENTS: dict = {
    'moz': {
        'moz5-winnt-10': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'moz5-winnt-61': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'moz5-mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'
    },
    'chrome': {
        'chrome-51': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    },
    'opera': {
        'opera-38': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
        'opera-980': 'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00',
        'opera-960': 'Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1'
    },
    'edge': {
        'edge-91': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
    },
    'safari': {
        'safari-604': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1'
    }
}

def getUserAgent(userAgent: str, requestAgainOnFail = True, exceptionOnFail = False) -> str|bool:
    '''
    Get the desired user agent from the available ones.
    '''
    agent: str|bool = False

    agent_keys: list = list( USER_AGENTS.keys() )

    for key in agent_keys:
        if key in userAgent:
            agent = USER_AGENTS.get(key).get(userAgent)

    if not agent:
        err: str = f'User Agent {agent} not found! Please try again...'

        if exceptionOnFail:
            raise Exception(err)
        else:
            print(err)
    
        if requestAgainOnFail:
            return getUserAgent( input('Select again the model of user agent you want: ') )
    
    return agent

__all__ = ['USER_AGENTS', 'getUserAgent']