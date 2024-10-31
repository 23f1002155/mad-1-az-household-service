from flask import request, flash, redirect, url_for, session
from flask import render_template
from flask import Blueprint
from application.models import *
from werkzeug.security import generate_password_hash, check_password_hash

my_blueprint = Blueprint('main', __name__)


@my_blueprint.route("/", methods = ["GET", "POST"])
def home():
    services = Service.query.all()
    return render_template("home.html", services = services)

@my_blueprint.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("All fields are required")
            return redirect(url_for("main.login"))
        

        user = User.query.filter_by(u_name = username).first()
        user_email = User.query.filter_by(u_email = username).first()

        if user or user_email:
            if user_email:
                if check_password_hash(user_email.u_passhash, password) and user_email.u_role == 0:
                    session["user_id"] = user_email.u_id

                    return redirect(url_for("main.admin_dashboard"))
                elif check_password_hash(user_email.u_passhash, password) and user_email.u_role == 1:
                    session["user_id"] = user_email.u_id

                    return redirect(url_for("main.customer_dashboard"))
                elif check_password_hash(user_email.u_passhash, password) and user_email.u_role == 2:
                    session["user_id"] = user_email.u_id

                    return redirect(url_for("main.service_provider_dashboard"))
                else:
                    flash("Invalid Password")
                    return redirect(url_for("main.login"))
            elif user:
                if check_password_hash(user.u_passhash, password) and user.u_role == 0:
                    session["user_id"] = user.u_id
                    return redirect(url_for("main.admin_dashboard"))
                elif check_password_hash(user.u_passhash, password) and user.u_role == 1:
                    session["user_id"] = user.u_id
                    return redirect(url_for("main.customer_dashboard"))
                elif check_password_hash(user.u_passhash, password) and user.u_role == 2:
                    session["user_id"] = user.u_id
                    return redirect(url_for("main.service_provider_dashboard"))
                else:
                    flash("Invalid Password")
                    return redirect(url_for("main.login"))
        else:
            flash("Invalid Username or Email")
            return redirect(url_for("main.login"))
                    


@my_blueprint.route("/sign-up-customer", methods = ["GET", "POST"])
def sign_up_customer():
    if request.method == "GET":
        return render_template("sign-up-customer.html")
    elif request.method == "POST":
        username = request.form.get("inputName")
        email = request.form.get("inputEmail4")
        password = request.form.get("inputPassword4")
        confirm_password = request.form.get("inputConfirmPassword4")
        city = request.form.get("inputCity")
        pincode = request.form.get("inputZip")

        if not username or not email or not password or not confirm_password or not city or not pincode:
            flash("All fields are required")
            return redirect(url_for("main.sign_up_customer"))
        if password != confirm_password:    
            flash("Passwords do not match")
            return redirect(url_for("main.sign_up_customer"))
        
        user = User.query.filter_by(u_name = username).first()
        user_email = User.query.filter_by(u_email = email).first()
        if user or user_email:
            flash("Email already exists")
            return redirect(url_for("main.sign_up_customer"))
        else:
            passhash = generate_password_hash(password)
            new_user = User(u_name = username, u_email = email, u_passhash = passhash, u_role = 1)
            new_customer = Customer(c_name = username, c_email = email, c_city = city, c_pincode = pincode, c_user_id = new_user.u_id)
            db.session.add(new_user)
            db.session.add(new_customer)
            db.session.commit()
            flash("Account Created Successfully")
            return redirect(url_for("main.login"))



@my_blueprint.route("/sign-up-serviceprovider", methods = ["GET", "POST"])
def sign_up_serviceprovider():
    if request.method == "GET":
        services = Service.query.all()
        return render_template("sign-up-serviceprovider.html", services = services)
    elif request.method == "POST":
        username = request.form.get("inputName")
        email = request.form.get("inputEmail4")
        password = request.form.get("inputPassword4")
        confirm_password = request.form.get("inputConfirmPassword4")
        contact_number = request.form.get("inputPhone")
        service_id= request.form.get("inputService")
        experience = request.form.get("inputExperience")
        rate = request.form.get("inputRate")
        service_description = request.form.get("inputServiceDescription")
        address = request.form.get("inputAddress")
        city = request.form.get("inputCity")
        pincode = request.form.get("inputZip")

        if not username or not email or not password or not confirm_password or not contact_number or not service_id or not experience or not rate or not service_description or not address or not city or not pincode:
            flash("All fields are required")
            return redirect(url_for("main.sign_up_serviceprovider"))
        if password != confirm_password:    
            flash("Passwords do not match")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        user = User.query.filter_by(u_email = email).first()
        if user:
            flash("Email already exists")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        passhash = generate_password_hash(password)

        new_user = User(u_name = username, u_email = email, u_passhash = passhash, u_role = 2)
        new_provider = ServiceProvider(p_name = username, p_email = email, p_contact_number = contact_number, p_experience = experience, p_city = city, p_pincode = pincode, p_user_id = new_user.u_id, p_service_id = service_id)
        db.session.add(new_user)
        db.session.add(new_provider)
        db.session.commit()
        new_service_details = ServiceDetail(sd_service_id = service_id, sd_provider_id = new_provider.p_id, sd_rate = rate, sd_description = service_description)
        db.session.add(new_service_details)
        db.session.commit()
        flash("Account Created Successfully")
        return redirect(url_for("main.login"))
    

@my_blueprint.route("/admin_dashboard")
def admin_dashboard():
    if "user_id" in session:
        flash("Logged In Successfully as Admin")
        return render_template("admin_dashboard.html")
    else:
        flash("Please Login")
        return redirect(url_for("main.login"))
    

@my_blueprint.route("/customer_dashboard")
def customer_dashboard():
    if "user_id" in session:
        flash("Logged In Successfully as Customer")
        return render_template("customer_dashboard.html")
    else:
        flash("Please Login")
        return redirect(url_for("main.login"))
    

@my_blueprint.route("/service_provider_dashboard")
def provider_dashboard():
    if "user_id" in session:
        flash("Logged In Successfully as Professional")
        return render_template("service_provider_dashboard.html")
    else:
        flash("Please Login")
        return redirect(url_for("main.login"))