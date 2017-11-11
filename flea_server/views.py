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
from flask import redirect

from flea_server import app, config, SITE_ROOT


def parent(f):
    return os.path.split(os.path.dirname(f))[1]


def find_sessions():
    files = glob.glob(os.path.join(config.DATA_DIR, '*/sequences.json'))
    names = list(parent(f) for f in files)
    return names


@app.route('/api/zips/<session_id>.zip')
def zip_api(session_id, methods=['GET']):
    directory = os.path.join(config.DATA_DIR, session_id)
    return send_from_directory(directory, 'session.zip',
                               as_attachment=True,
                               attachment_filename="{}.zip".format(session_id))


@app.route('/api/sessions/<session_id>/')
def session_api(session_id, methods=['GET']):
    if session_id not in find_sessions():
        abort(404)
    directory = os.path.join(config.DATA_DIR, session_id)
    with open(os.path.join(directory, 'session.json')) as handle:
        result = json.load(handle)

    result['session_id'] = session_id

    # insert predefined regions
    regions_file = os.path.join(directory, 'predefined_regions.json')
    if not os.path.exists(regions_file):
        regions_file = os.path.join(SITE_ROOT, 'static', 'web-app', 'assets', regions_file)
    with open(regions_file) as handle:
        regions_json = json.load(handle)
    result['predefined_regions'] = regions_json['regions']

    # insert structure
    pdb_file = os.path.join(directory, 'structure.pdb')
    if not os.path.exists(pdb_file):
        pdb_file = os.path.join(SITE_ROOT, 'static', 'web-app', 'assets', 'pdbs', 'env_structure.pdb')
    with open(pdb_file) as h:
        lines = h.read().split('\n')
    result['pdb'] = lines

    return jsonify(result)


@app.route('/assets/fonts/<filename>/')
def serve_font(filename):
    return send_from_directory('static/web-app/assets/fonts', filename)


@app.route('/assets/<filename>/')
def serve_assets(filename):
    return send_from_directory('static/web-app/assets', filename)


@app.route('/view/<session_id>/', defaults={'path': ''})
@app.route('/view/<session_id>/<path:path>/')
def serve_ember_session(session_id, path):
    """Serve the app on all subpaths.

    In conjuction with Ember's HistoryLocation, this allows the client
    to navigate directly to a url in the Ember app.

    """
    return send_from_directory('static/web-app/', 'index.html')


@app.route('/view/')
def redirect_view():
    return redirect("/", code=302)


@app.route('/')
def index():
    return render_template('index.html')
