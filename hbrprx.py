import re
import requests

from lxml import html
from flask import Flask

app = Flask(__name__)

TMABLE = re.compile('(^|[^-\w])([-\w]{6})(?=($|[^-\w]))')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):  # pragma: no cover
    habr = f'http://habrahabr.ru/{path}'
    response = requests.get(habr)
    page = response.content
    if response.headers.get('Content-Type', '').startswith('text/html'):
        return improve(page)
    return page


def improve(html_bytes):
    try:
        etree = html.fromstring(html_bytes)
    except Exception:
        return html_bytes

    if etree is not None:
        body = etree.find('body')
        if body is not None:
            process_tree(body)
            return html.tostring(etree, encoding='unicode')

    return html_bytes


def process_tree(tree):
    for element in tree.iter():

        if element.tag == 'script' or element.tag == 'style':
            continue

        if element.text is not None:
            element.text = add_tm(element.text)

        if element.tail is not None:
            element.tail = add_tm(element.tail)

        if element.tag == 'a':
            link = element.attrib.get('href')
            if link:
                element.attrib['href'] = make_habr_rel_path(link)


def add_tm(content):
    return TMABLE.sub(r'\1\2™', content)


def make_habr_rel_path(link):
    abs_paths = ['https://habrahabr.ru',
                 'http://habrahabr.ru',
                 '//habrahabr.ru']
    match = next((path for path in abs_paths if link.startswith(path)), None)
    if match:
        return link[len(match):] or '/'
    return link
