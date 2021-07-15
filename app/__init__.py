from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'HomePage'

    from .api.create import create_api as create_api_blueprint
    app.register_blueprint(create_api_blueprint)

    from .api.read import read_api as read_api_blueprint
    app.register_blueprint(read_api_blueprint)

    from .api.read_all import read_all_api as read_all_api_blueprint
    app.register_blueprint(read_all_api_blueprint)

    from .api.update import update_api as update_api_blueprint
    app.register_blueprint(update_api_blueprint)

    from .api.delete import delete_api as delete_api_blueprint
    app.register_blueprint(delete_api_blueprint)

    return app
