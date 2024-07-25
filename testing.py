import requests
from bs4 import BeautifulSoup
import random
import string
import codecs

urls = [
    "https://michelemincone.com/chi-sono/",
    "https://michelemincone.com/dichiarazione-sulla-privacy-ue/",
    "https://michelemincone.com/contattami/",
    "https://michelemincone.com/blog/",
    "https://michelemincone.com/cookie-policy-ue/",
    "https://michelemincone.com/termini-e-condizioni/"
]

N=7

for url in urls:
    response = requests.get(url)
    htmlBytes = response.content

    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))

    f = open(f'crawled\\{res}.html', 'w', encoding='utf8')
    f.write(codecs.decode(htmlBytes, encoding='utf-8', errors='ignore'))
    f.close()