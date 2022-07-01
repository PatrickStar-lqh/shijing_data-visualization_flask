from flask import Flask



def create_app():
    app = Flask(__name__)


    from .shijing_dataviz import sjdv as sjdv_blueprint
    app.register_blueprint(sjdv_blueprint)

    return app