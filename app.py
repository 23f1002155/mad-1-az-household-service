import os
from dotenv import load_dotenv
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from application.controllers import *


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is set up.")
    else:
        print("Starting Local Development...")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

load_dotenv()
app = create_app()
app.register_blueprint(my_blueprint)

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(u_role = 0).first()
    if not admin:
        passhash = generate_password_hash("password")
        admin = User(u_name = "admin", u_email = "23f1002155@ds.study.iitm.ac.in", u_passhash = passhash, u_role = 0)
        db.session.add(admin)
        db.session.commit()
        print("Admin Created")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)