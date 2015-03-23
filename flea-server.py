#!/usr/bin/env python

"""
Usage:
  flea-server.py [options]
  flea-server.py -h | --help

Options:
  -v --verbose      Print progress to STDERR
  --data <STRING>   Data directory
  --app <STRING>    flea-app frontent directory
  --host <STRING>   Host  [default: localhost]
  -p --port=<INT>   Port to run [default: 8080]
  -d --debug        Debug mode
  -h --help         Show this screen

"""

import glob
import os
from os import path
import json
import csv

from docopt import docopt

from bottle import route, run, template, get
from bottle import static_file
from bottle import response
from bottle import redirect

ROOT = ''

SERVER_DIR = path.dirname(path.realpath(__file__))
FRONTEND_DIR = path.join(SERVER_DIR, 'flea-ember-app')
DATA_DIR = path.join(SERVER_DIR, 'mock-data')

NAME_MAPPER = {
    'frequencies': 'frequencies.json',
    'structure': 'secondaryStruct.pdb',
    'trees': 'trees.json',
    'neutralization': 'mab.json',
    'sequences': 'sequences.json',
    'rates_pheno': 'rates_pheno.tsv',
    'dates': 'dates.json',
    'rates': 'rates.json',
    'turnover': 'turnover.json',
}

def parent(f):
    return path.split(path.dirname(f))[1]


def sessions():
    files = glob.glob(path.join(DATA_DIR, '*/sequences.json'))
    names = list(parent(f) for f in files)
    return names


@route('{}/'.format(ROOT))
def index():
    links = list('<li><a href="{base}/{name}/">{name}</a></li>'.format(base=ROOT, name=n)
                 for n in sessions())
    header = 'FLEA test server. Available data:\n<ul>\n'
    middle = '\n'.join(links)
    footer = '</ul>'
    html = '\n'.join([header, middle, footer])
    return template(html)


@route('{}/assets/<filename>'.format(ROOT))
def serve_static(filename):
    root = os.path.join(FRONTEND_DIR, 'assets')
    return static_file(filename, root=root)


@get('{}/favicon.ico'.format(ROOT))
def get_favicon():
    return serve_static('favicon.ico')


@route('{}/fonts/<filename>'.format(ROOT))
def server_font(filename):
    root = os.path.join(FRONTEND_DIR, 'fonts')
    try:
        idx = filename.index('?')
        filename = filename[:idx]
    except:
        pass
    return static_file(filename, root=root)


def tsv_to_json(contents):
    contents = contents.split('\n')
    lines = list(csv.reader(contents, delimiter='\t'))
    result = {}
    keys = lines[0]
    result = [{key: value for key, value in zip(keys, line)}
              for line in lines[1:]]
    return json.dumps(result)


@route('{}/data/<session_id>/<resource>'.format(ROOT))
def data_file(session_id, resource):
    if session_id not in sessions():
        return {}
    filename = path.join(DATA_DIR, session_id, NAME_MAPPER[resource])
    with open(filename) as handle:
        contents = handle.read()
    if filename[-len('json'):] == 'json':
        response.content_type = 'application/json'
    if filename[-len('tsv'):] == 'tsv':
        response.content_type = 'application/json'
        contents = tsv_to_json(contents)
    return contents


@route('{}/<session>/'.format(ROOT))
def serve_session(session):
    if session not in sessions():
        return "{} not found".format(session)
    result = path.join(FRONTEND_DIR, 'index.html')
    with open(result) as handle:
        html = handle.read()
    return template(html)


@route('{}/<session>/<subpath:path>'.format(ROOT))
def serve_session_with_subpath(session, subpath):
    """Serve the app on all subpaths.

    In conjuction with Ember's HistoryLocation, this allows the client
    to navigate directly to a url in the Ember app.

    """
    return serve_session(session)


if __name__ == "__main__":
    opts = docopt(__doc__)
    if opts['--data'] is not None:
        DATA_DIR = path.abspath(opts['--data'])
    if not path.exists(DATA_DIR):
        raise Exception('data directory "{}" does not exist'.format(DATA_DIR))
    if opts['--app'] is not None:
        FRONTEND_DIR = path.abspath(opts['--app'])
    if not path.exists(FRONTEND_DIR):
        raise Exception('app directory"{}" does not exist'.format(FRONTEND_DIR))
    host = opts['--host']
    port = int(opts['--port'])
    debug = opts['--debug']
    run(host=host, port=port, debug=debug)
