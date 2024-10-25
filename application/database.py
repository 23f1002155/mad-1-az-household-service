from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from app import app

engine = None
Base = declarative_base()
db = SQLAlchemy(app)