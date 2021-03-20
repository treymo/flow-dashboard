import os
from flask import Flask, send_from_directory, current_app, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        constants = {
            'dev': True
        }
        gmap_api_key = current_app.config['G_MAPS_API_KEY']
        return render_template('index.html',
                               alt_bootstrap='blah',
                               constants=constants,
                               gmap_api_key=gmap_api_key)

    @app.route('/static/js/<path:path>')
    def send_js(path):
        return send_from_directory('dist/src', path)

    @app.route('/images/<path:path>')
    def send_images(path):
        return send_from_directory('images', path)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8081, debug=True)
