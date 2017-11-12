# README #

A Flask server for serving results from
[flea-pipeline](https://github.com/veg/flea-pipeline) and visualizing
them with [flea-web-app](https://github.com/veg/flea-web-app).

### Dependencies ###

Python dependencies are listed in `requirements.in`. Install using
[pip-tools](https://github.com/jazzband/pip-tools), or just call `pip
-r requirements.txt`.

### Setup ###

A build of [flea-web-app](https://github.com/veg/flea-web-app) is
expected to be in `flea_server/static/web-app`.

By default, results from the FLEA pipeline go in their directories in
the `results` directory, e.g.:

    ./results/P018/session.json
    ./results/P018/session.zip

Update the configuration file `flea_server/config.py` to specify a
different results directory.

### Running ###

For development purposes, just use the Flask server:

    python run_flea_server.py

For deployment, this server has been tested with
[Gunicorn](http://gunicorn.org/) and [Nginx](http://nginx.org/).
