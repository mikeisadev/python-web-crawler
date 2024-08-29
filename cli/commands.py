import re
import validators

'''
    List of all types of commands and how them should be represented.

    Types of commands you can find here:
    - save
    - sitemap
    - json
    - user-agent
    - headers
    - duplicate-links
    - crawl-depth
    
    Commands I want to build:
    - save-images
    - save-css
    - save-js
    - save-all
    - save-cookies
    - use-web-browser (instead of using the direct HTTP GET request)
    - scan-robots-txt
    - get-json-schemas
    - get-pixels
'''

COMMANDS_RULES: dict[str, dict[str, any]] = {
    'save': {
        'arg'           : False,
        'arg-required'  : False,
        'arg-type'      : None,
        'cmd'           : ('-s', '--save')
    },
    'sitemap': {
        'arg'           : False,
        'arg-required'  : False,
        'arg-type'      : None,
        'cmd'           : ('-sm', '--sitemap')
    },
    'json': {
        'arg'           : False,
        'arg-required'  : False,
        'arg-type'      : None,
        'cmd'           : ('--json', '-js')
    },
    'user-agent': {
        'arg'           : True,
        'arg-required'  : False,
        'arg-type'      : str,
        'cmd'           : ('-ua', '--user-agent')
    },
    'headers': {
        'arg'           : False,
        'arg-required'  : False,
        'arg-type'      : None,
        'cmd'           : ('--all-headers', '--res-headers', '--req-headers')
    },
    'duplicate-links': {
        'arg'           : False,
        'arg-required'  : False,
        'arg-type'      : None,
        'cmd'           : ('-sdl', '--save-dup-links')
    },
    'crawl-depth': {
        'arg'           : True,
        'arg-required'  : True,
        'arg-type'      : int,
        'cmd'           : ('--depth', '--crawl-depth', '-cd')
    }
}

def commandInPrompt(allArgs: str|tuple, commandType: str, returnCmd: bool = False) -> bool|str|int:
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
        if arg in excludeArgs or re.match(r'[A-z-_]+[.][p][y]+', arg) or validators.url(arg):
            continue

        if '=' in arg:
            arg = arg.split('=')

            if arg[0] not in commands:
                continue
            
            res = arg[1]
            arg = arg[0]
        else:
            if returnCmd:
                res = arg
            elif arg in commands:
                res = True
            
        if arg not in commands:
            continue

        if arg in commands and not res and commandRules['arg-requird']:
            raise Exception(f'Missing argument for the parameter {arg}')

        break

    return res

# ommandInPrompt('py crawler.py https://michelemincone.com -s -sm --json -ua=opera-38 --all-headers -sdl', 'headers', True)

__all__ = ['COMMAND_RULES', 'commandInPrompt']