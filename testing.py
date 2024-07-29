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

url = ["https://michelemincone.com/blog/"]

N=7

for u in url:
    response = requests.get(u)
    htmlBytes = response.content

    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))

    parsed = BeautifulSoup(htmlBytes, 'html.parser')

    hrefs = parsed.select('a[href]')

    for href in hrefs: print(href)

    f = open(f'crawled\\{res}.html', 'w', encoding='utf8')
    f.write(codecs.decode(htmlBytes, encoding='utf-8', errors='ignore'))
    f.close()