from .database import db


class User(db.Model):
    __tablename__ = 'user_database'
    u_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    u_name = db.Column(db.String, nullable = False, unique = True)
    u_email = db.Column(db.String, nullable = False, unique = True)
    u_password = db.Column(db.String, nullable=False, unique=True)
    u_role = db.Column(db.String, nullable=False)

'''class Sevice(db.Model):
    __tablename__ = 'service database'
'''