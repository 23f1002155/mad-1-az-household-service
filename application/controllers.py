from flask import request, flash, redirect, url_for, session
from flask import render_template
from flask import Blueprint
from application.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

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
        address = request.form.get("inputAddress")
        city = request.form.get("inputCity")
        pincode = request.form.get("inputZip")

        if not username or not email or not password or not confirm_password or not contact_number or not service_id or not experience or not address or not city or not pincode:
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
        
        db.session.add(new_user)
        db.session.commit()
        new_provider = ServiceProvider(p_name = username, p_email = email, p_contact_number = contact_number, p_experience = experience, p_city = city, p_pincode = pincode, p_user_id = new_user.u_id, p_service_id = service_id)
        db.session.add(new_provider)
        db.session.commit()
        flash("Account Created Successfully")
        return redirect(url_for("main.login"))



def requires_login(my_fucntion):
    @wraps(my_fucntion)
    def main_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please Login")
            return redirect(url_for("main.login"))
        return my_fucntion(*args, **kwargs)
    return main_function

@my_blueprint.route("/admin_dashboard")
@requires_login
def admin_dashboard():
    flash("Logged In Successfully as Admin")
    return render_template("admin_dashboard.html")

    

@my_blueprint.route("/customer_dashboard")
@requires_login
def customer_dashboard():
    flash("Logged In Successfully as Customer")
    return render_template("customer_dashboard.html")

    

@my_blueprint.route("/service_provider_dashboard")
@requires_login
def service_provider_dashboard():
    flash("Logged In Successfully as Professional")
    return render_template("service_provider_dashboard.html")


@my_blueprint.route("/logout")
@requires_login
def logout():
    session.pop("user_id")
    flash("Logged Out Successfully")
    return redirect(url_for("main.home"))

@my_blueprint.route("/profile", methods = ["GET", "POST"])
@requires_login
def profile():
    if request.method == "GET":
        user = User.query.filter_by(u_id = session["user_id"]).first()
        if user.u_role == 1:
            c_user = Customer.query.filter_by(c_user_id = user.u_id).first()
            return render_template("profile.html", user = user, c_user = c_user)
        elif user.u_role == 2:
            p_user = ServiceProvider.query.filter_by(p_user_id = user.u_id).first()
            p_service = Service.query.filter_by(s_id = p_user.p_service_id).first()
            return render_template("profile.html", user = user, p_user = p_user, p_service = p_service)
        return render_template("profile.html", user = user)
    elif request.method == "POST":
        user = User.query.filter_by(u_id = session["user_id"]).first()
        if user.u_role == 0:
            username = request.form.get("username")
            email = request.form.get("email")
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            if not username or not current_password or not new_password or not confirm_password:
                flash("All fields are required")
                return redirect(url_for("main.profile"))
            
            if not check_password_hash(user.u_passhash, current_password):
                flash("Invalid Password")
                return redirect(url_for("main.profile"))
            
            if new_password != confirm_password:
                flash("Passwords do not match")
                return redirect(url_for("main.profile"))
            
            if username != user.u_name:
                new_username = User.query.filter_by(u_name = username).first()
                if new_username:
                    flash("Username already exist")
                    return redirect(url_for("main.profile"))
            new_passhash = generate_password_hash(new_password)
            user.u_name = username
            user.u_passhash = new_passhash
            db.session.commit()
            flash("Profile Updated Successfully")
            return redirect(url_for("main.profile"))

        elif user.u_role == 1:
            username = request.form.get("username")
            email = request.form.get("email")
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")
            city = request.form.get("City")
            pincode = request.form.get("pincode")

            if not username or not current_password or not new_password or not confirm_password or not city or not pincode:
                flash("All fields are required")
                return redirect(url_for("main.profile"))
            
            if not check_password_hash(user.u_passhash, current_password):
                flash("Invalid Password")
                return redirect(url_for("main.profile"))
            
            if new_password != confirm_password:
                flash("Passwords do not match")
                return redirect(url_for("main.profile"))
            
            if username != user.u_name:
                new_username = User.query.filter_by(u_name = username).first()
                if new_username:
                    flash("Username already exist")
                    return redirect(url_for("main.profile"))
            new_passhash = generate_password_hash(new_password)
            user.u_name = username
            user.u_passhash = new_passhash
            c_user = Customer.query.filter_by(c_user_id = session["user_id"])
            c_user.c_name = username
            c_user.c_city = city
            c_user.c_pincode = pincode
            db.session.commit()
            flash("Profile Updated Successfully")
            return redirect(url_for("main.profile"))
        
        elif user.u_role == 2:
            username = request.form.get("username")
            email = request.form.get("email")
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")
            contact_number = request.form.get("inputPhone")
            service_id = request.form.get("inputService")
            experience = request.form.get("inputExperience")
            address = request.form.get("inputAddress")
            city = request.form.get("inputCity")
            pincode = request.form.get("inputPincode")

            if not username or not current_password or not new_password or not confirm_password or not contact_number or not service_id or not experience or not address or not city or not pincode:
                flash("All fields are required")
                return redirect(url_for("main.profile"))


            if not check_password_hash(user.u_passhash, current_password):
                flash("Invalid Password")
                return redirect(url_for("main.profile"))
            
            if new_password != confirm_password:
                flash("Passwords do not match")
                return redirect(url_for("main.profile"))
            
            if username != user.u_name:
                new_username = User.query.filter_by(u_name = username).first()
                if new_username:
                    flash("Username already exist")
                    return redirect(url_for("main.profile"))
            new_passhash = generate_password_hash(new_password)
            user.u_name = username
            user.u_passhash = new_passhash
            p_user = ServiceProvider.query.filter_by(p_user_id = session["user_id"]).first()
            p_user.p_name = username
            p_user.p_city = city
            p_user.p_pincode = pincode
            p_user.p_address = address
            p_user.p_contact_namer = contact_number
            db.session.commit()
            flash("Profile Updated Successfully")

@my_blueprint.route("/search", methods = ["GET", "POST"])
@requires_login
def search():
    return "Search Page"

@my_blueprint.route("/summary")
@requires_login
def summary():
    return "Summary Page"


    