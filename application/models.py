from .database import db


class User(db.Model):
    __tablename__ = 'user_database'
    u_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    u_name = db.Column(db.String, nullable = False, unique = True)
    u_email = db.Column(db.String, nullable = False, unique = True)
    u_passhash = db.Column(db.String(256), nullable=False, unique=True)
    u_role = db.Column(db.Integer, nullable=False, foreign_key = True)

class Role(db.Model):
    __tablename__ = "user_role"
    role_id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String, nullable = False, unique = True)

    
'''
class Customer(db.Model)
    __tablename__ = "customer_data"
    c_id = db.Column(db.Integer, primary_key = True)
'''