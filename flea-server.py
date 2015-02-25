"""

Usage:
  flea-server.py [options]
  flea-server.py -h | --help

Options:
  -v --verbose     Print progress to STDERR
  --data <STRING>  Data directory
  --host <STRING>  Host  [default: localhost]
  -p --port=<INT>  Port to run [default: 8080]
  -d --debug       Debug mode
  -h --help        Show this screen


"""

import glob
import os
from os import path
import json

from docopt import docopt

from bottle import route, run, template
from bottle import static_file
from bottle import response
from bottle import redirect


SERVER_DIR = path.dirname(path.realpath(__file__))
FRONTEND_DIR = path.join(SERVER_DIR, 'flea-ember-app')
DATA_DIR = path.join(SERVER_DIR, 'mock-data')

NAME_MAPPER = {
    'frequencies': 'frequencies.json',
    'structure': 'secondaryStruct.pdb',
    'trees': 'trees.json',
    'neutralization': 'mab.json',
    'sequences': 'sequences.json',
    'rates_pheno': 'rates_pheno.json',
    'dates': 'dates.json',
    'rates': 'rates.json',
}

def parent(f):
    return path.split(path.dirname(f))[1]


def sessions():
    files = glob.glob(path.join(DATA_DIR, '*/sequences.json'))
    names = list(parent(f) for f in files)
    return names


@route('/')
def index():
    links = list('<li><a href="/{name}/">{name}</a></li>'.format(name=n)
                 for n in sessions())
    header = 'FLEA test server. Available data:\n<ul>\n'
    middle = '\n'.join(links)
    footer = '</ul>'
    html = '\n'.join([header, middle, footer])
    return template(html)


@route('/assets/<filename>')
def serve_static(filename):
    root = os.path.join(FRONTEND_DIR, 'assets')
    return static_file(filename, root=root)


@route('/fonts/<filename>')
def server_font(filename):
    root = os.path.join(FRONTEND_DIR, 'fonts')
    try:
        idx = filename.index('?')
        filename = filename[:idx]
    except:
        pass
    return static_file(filename, root=root)


@route('/api/<session_id>/<resource>')
def data_file(session_id, resource):
    if session_id not in sessions():
        return {}
    filename = path.join(DATA_DIR, session_id, NAME_MAPPER[resource])
    with open(filename) as handle:
        contents = handle.read()
    if filename[-len('json'):] == 'json':
        response.content_type = 'application/json'
    return contents


@route('/<session>')
def redirect_session(session):
    """Ember requires the rootUrl to end in a slash"""
    redirect('/{}/'.format(session))


@route('/<session>/')
def serve_session(session):
    if session not in sessions():
        return "{} not found".format(session)
    result = path.join(FRONTEND_DIR, 'index.html')
    with open(result) as handle:
        return template(handle.read())


@route('/<session>/<subpath:path>')
def serve_session_with_subpath(session, subpath):
    """Serve the app on all subpaths.

    In conjuction with Ember's HistoryLocation, this allows the client
    to navigate directly to a url in the Ember app.

    """
    return serve_session(session)


if __name__ == "__main__":
    opts = docopt(__doc__)
    if '--data' in opts:
        DATA_DIR = path.abspath(opts['--data'])
    host = opts['--host']
    port = int(opts['--port'])
    debug = opts['--debug']
    run(host=host, port=port, debug=debug)
