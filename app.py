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

def interwiki_for_page(lang, entitle):
    host = host_for_lang(lang)
    url = 'http://en.wikipedia.org/w/api.php?action=query&prop=langlinks&lllimit=500&format=json&titles=%s' % (entitle, )
    data = cache.get(url)
    if data == None:
        res = requests.get(url)
        data = json.loads(res.content)
    title = '' 
    if '-1' not in data['query']['pages']:
        langlinks = data['query']['pages'].values()[0]['langlinks']
        for langlink in langlinks:
            if langlink['lang'] == lang:
                title = langlink['*']
                break

    return '%s/wiki/%s' % (host, title)


@app.route('/s/<lang>/<shortkey>/')
def do_redirect(lang, shortkey):
    page_id = int(shortkey, 36)
    return redirect(url_for_page(lang, page_id))

@app.route('/en/<lang>/<entitle>/')
def interwiki_redirect(lang, entitle):
    return redirect(interwiki_for_page(lang, entitle))

if __name__ == '__main__':
    app.run()
