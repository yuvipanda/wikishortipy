import json

from flask import Flask, redirect
import requests

import base36

app = Flask(__name__)
app.debug = True

def host_for_lang(lang):
    return 'http://%s.wikipedia.org' % lang

def url_for_page(lang, id):
    host = host_for_lang(lang)
    url = '%s/w/api.php?action=query&prop=info&inprop=url&format=json&pageids=%s' % (host, id)
    res = requests.get(url)
    data = json.loads(res.content)
    page = data['query']['pages'][str(id)]
    if 'missing' in page:
        return 'google.com'
    else:
        print page
        print repr(page['fullurl'])
        return '%s/wiki/%s' % (host, page['title'])

@app.route('/<lang>/<shortkey>')
def do_redirect(lang, shortkey):
    page_id = int(shortkey, 36)
    return redirect(url_for_page(lang, page_id))

if __name__ == '__main__':
    app.run()
