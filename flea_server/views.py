#!/usr/bin/env python

import glob
import os
import json
import csv

from flask import render_template
from flask import send_from_directory
from flask import jsonify
from flask import json
from flask import abort

from flea_server import app, config, SITE_ROOT


NAME_MAPPER = {
    'runinfo': 'run_info.json',
    'coordinates': 'coordinates.json',
    'trees': 'trees.json',
    'manifold': 'manifold.json',
    'neutralization': 'mab.json',
    'sequences': 'sequences.json',
    'rates_pheno': 'rates_pheno.json',
    'dates': 'dates.json',
    'copynumbers': 'copynumbers.json',
    'rates': 'rates.json',
    'divergence': 'js_divergence.json',
}


def parent(f):
    return os.path.split(os.path.dirname(f))[1]


def find_sessions():
    files = glob.glob(os.path.join(config.DATA_DIR, '*/sequences.json'))
    names = list(parent(f) for f in files)
    return names


@app.route('/api/pdbs/<pdbname>/')
def serve_pdb(pdbname):
    fn = os.path.join(SITE_ROOT, 'static', 'flea', 'dist', 'assets', 'pdbs', '{}.pdb'.format(pdbname))
    print(fn)
    with open(fn) as h:
        lines = h.read().split('\n')
    return jsonify({'data': lines})


@app.route('/api/sessions/<session_id>/<resource>/')
def session_api(session_id, resource, methods=['GET']):
    if session_id not in find_sessions():
        abort(404)
    directory = os.path.join(config.DATA_DIR, session_id)
    filename = NAME_MAPPER[resource]
    return send_from_directory(directory, filename)


@app.route('/assets/<filename>/')
def serve_assets(filename):
    return send_from_directory('static/flea/dist/assets', filename)


@app.route('/fonts/<filename>/')
def serve_font(filename):
    try:
        idx = filename.index('?')
        filename = filename[:idx]
    except:
        pass
    return send_from_directory('static/flea/dist/fonts', filename)


@app.route('/results/<session_id>/', defaults={'path': ''})
@app.route('/results/<session_id>/<path:path>/')
def serve_ember_session(session_id, path):
    """Serve the app on all subpaths.

    In conjuction with Ember's HistoryLocation, this allows the client
    to navigate directly to a url in the Ember app.

    """
    return send_from_directory('static/flea/dist', 'index.html')


@app.route('/results/')
def server_results_list():
    sessions = find_sessions()
    return render_template('show_sessions.html', sessions=sessions)


@app.route('/')
def index():
    return render_template('index.html')
