import glob
from os import path

from bottle import route, run, template


DATA_DIR = "/home/kemal/projects/env/veg-hiv-env"

@route('/')
def index():
    files = glob.glob(path.join(DATA_DIR, '*/sequences.json'))
    names = list(path.split(path.dirname(f))[1]
                 for f in files)
    links = list('<li><a href="/{name}">{name}</a></li>'.format(name=n) for n in names)
    header = 'FLEA test server. Available data:\n<ul>\n'
    middle = '\n'.join(links)
    footer = '</ul>'
    html = '\n'.join([header, middle, footer])
    return template(html)

run(host='localhost', port=8090, debug=True)
