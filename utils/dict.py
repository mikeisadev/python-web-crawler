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

__all__ = ['updateTree']