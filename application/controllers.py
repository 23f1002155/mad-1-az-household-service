from flask import Flask, request
from flask import render_template
from flask import Blueprint
from application.models import *

my_blueprint = Blueprint('main', __name__)


@my_blueprint.route("/", methods = ["GET", "POST"])
def home():
    return render_template("home.html")

@my_blueprint.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html")

@my_blueprint.route("/sign-up-customer", methods = ["GET", "POST"])
def sign_up_customer():
    return render_template("sign-up-customer.html")

@my_blueprint.route("/sign-up-serviceprovider", methods = ["GET", "POST"])
def sign_up_serviceprovider():
    return render_template("sign-up-serviceprovider.html")