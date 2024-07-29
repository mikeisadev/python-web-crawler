import collections.abc
import json

tree = {"https://michelemincone.com": {
    "https://michelemincone.com/blog/": {
        "https://michelemincone.com/blog/page/2/": "",
        "https://michelemincone.com/blog/page/11/": ""
    },
    "https://michelemincone.com/contattami/": "",
    "https://michelemincone.com/chi-sono/": "",
    "https://michelemincone.com/dichiarazione-sulla-privacy-ue/": "",
    "https://michelemincone.com/cookie-policy-ue/": {
        "https://michelemincone.com/cookie-policy-ue/cock": ''
    },
    "https://michelemincone.com/termini-e-condizioni/": ""
}}

update = {
    'https://ddd.com': ''
}


def updateTree(tree, key, value): 
    for k, v in tree.items():
        if key in k:
            tree[k] = value 
        elif type(v) is dict:
            tree[k] = updateTree(v, key, value)

    return tree

updateTree(tree, 'https://michelemincone.com/cookie-policy-ue/cock', update)

f = open('tree.json', 'w')
f.write( json.dumps(tree, indent=8) )
f.close()