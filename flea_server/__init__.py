import os

from flask import Flask

app = Flask(__name__)
app.config.from_object('flea_server.config')

# needs to be at bottom; see http://flask.pocoo.org/docs/0.10/patterns/packages/
import flea_server.views
