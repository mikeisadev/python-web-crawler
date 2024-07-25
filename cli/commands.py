import re

'''
    List of all types of commands and how them should be represented.

    Types of commands you can find here:
    - save
    - sitemap
    - json
    - user-agent
    - headers

    Commands I want to build:
    - save-images
    - save-css
    - save-js
    - save-all
    - crawl-depth
    - save-cookies
    - use-web-browser (instead of using the direct HTTP GET request)
    - scan-robots-txt
    - get-json-schemas
    - get-pixels
'''
COMMANDS_RULES = {
    'save': {
        'arg'           : False,
        'arg-required'  : False,
        'cmd'           : ('-s', '--save')
    },
    'sitemap': {
        'arg'           : False,
        'arg-required'  : False,
        'cmd'           : ('-sm', '--sitemap')
    },
    'json': {
        'arg'           : False,
        'arg-required'  : False,
        'cmd'           : ('--json')
    },
    'user-agent': {
        'arg'           : True,
        'arg-required'  : False,
        'cmd'           : ('-ua', '--user-agent')
    },
    'headers': {
        'arg'           : False,
        'arg-required'  : False,
        'cmd'           : ('--all-headers', '--res-headers', '--req-headers')
    }
}

def commandInPrompt(allArgs: str|tuple, commandType: str, returnCmd: bool = False) -> bool|str:
    '''
    Use this function to check if the prompt (allArgs), given ad tuple, has the specified command type inside it.
    '''
    allArgs = allArgs.split(' ') if type(allArgs) is str else allArgs

    commandRules: dict = COMMANDS_RULES[commandType]
    commands: list = commandRules['cmd']
    excludeArgs: list = ('py')
    res: bool = False

    for arg in allArgs:
        # continue loop for excluded args.
        if arg in excludeArgs or re.match(r'[A-z-_]+[.][p][y]+', arg):
            continue

        # If has '=' the arg has parameter, so split to get only the arg
        arg = (arg.split('='))[0] if '=' in arg else arg

        # Check arg
        if arg in commands and not returnCmd:
            res = True
            break
        elif returnCmd:
            res = arg
        else:
            res = False

        # Check arg parameter
        if commandRules['arg'] and commandRules['arg-required'] and len( arg.split('=') ) != 2:
            raise Exception(f'Missing parameter for the command {arg}')

    # print(arg)
    
    return res

# print(commandInPrompt('py crawler.py https://michelemincone.com -s -ua=moz5-lf5', 'user-agent'))

__all__ = ['COMMAND_RULES', 'commandInPrompt']