"""Convenience script for running development version of server.

For production, use nginx (see README.md).

"""

from flea_server import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
