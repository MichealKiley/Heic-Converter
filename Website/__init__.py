from flask import Flask

def create_app():
    app = Flask(__name__)

    from .heic.heic_route import heic_route

    app.register_blueprint(heic_route, url_prefix=("/"))

    return app