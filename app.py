import json

from flask import Flask, redirect
import requests

import settings

app = Flask(__name__)
app.debug = True

app.config.from_envvar('WIKISHORTIPY_SETTINGS')

cache = app.config['CACHE']

def host_for_lang(lang):
    return 'http://%s.wikipedia.org' % lang

def url_for_page(lang, id):
    host = host_for_lang(lang)
    url = '%s/w/api.php?action=query&prop=info&inprop=url&format=json&pageids=%s' % (host, id)
    title = cache.get(url) 
    if title == None:
        res = requests.get(url)
        data = json.loads(res.content)
        page = data['query']['pages'][str(id)]
        if 'missing' in page:
            title = ''
        else:
            title = page['title']
            cache.set(url, title)
    return '%s/wiki/%s' % (host, title)

@app.route('/s/<lang>/<shortkey>/')
def do_redirect(lang, shortkey):
    page_id = int(shortkey, 36)
    return redirect(url_for_page(lang, page_id))

if __name__ == '__main__':
    app.run()
