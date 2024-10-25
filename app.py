import os
from flask import Flask, current_app, render_template
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from application.controllers import *
from application.models import *

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is set up.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
app.register_blueprint(my_blueprint)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)