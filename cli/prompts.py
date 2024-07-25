'''
Data structures to give select choises to prompts.

Here all the data structure to define all the cmd inputs will be defined.

For example:
Save headers list will display all the choices you can take to define which headers you want to save in the JSON file inside the crawled folder.

In the future this python dictionary will be expanded with other choices you can select inside the prompt.
'''
prompts: dict = {
    'save-headers': ('all', 'request-headers', 'response-headers'),
}

__all__ = ['prompts']