from flask import request, flash, redirect, url_for, session
from flask import render_template
from flask import Blueprint
from application.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

my_blueprint = Blueprint('main', __name__)


@my_blueprint.route("/", methods = ["GET", "POST"])
def home():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))
    service_categories = ServiceCategory.query.all()
    return render_template("home.html", service_categories = service_categories)

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
                    flash("Loggen In Successfully as Admin")
                    return redirect(url_for("main.dashboard"))
                

                elif check_password_hash(user_email.u_passhash, password) and user_email.u_role == 1:
                    session["user_id"] = user_email.u_id
                    flash("Loggen In Successfully as Customer")
                    return redirect(url_for("main.dashboard"))
                

                elif check_password_hash(user_email.u_passhash, password) and user_email.u_role == 2:
                    session["user_id"] = user_email.u_id
                    flash("Loggen In Successfully as Professional")
                    return redirect(url_for("main.dashboard"))
                else:
                    flash("Invalid Password")
                    return redirect(url_for("main.login"))
            elif user:
                if check_password_hash(user.u_passhash, password) and user.u_role == 0:
                    session["user_id"] = user.u_id
                    flash("Loggen In Successfully as Admin")
                    return redirect(url_for("main.dashboard"))
                elif check_password_hash(user.u_passhash, password) and user.u_role == 1:
                    session["user_id"] = user.u_id
                    flash("Loggen In Successfully as Customer")
                    return redirect(url_for("main.dashboard"))
                elif check_password_hash(user.u_passhash, password) and user.u_role == 2:
                    session["user_id"] = user.u_id
                    flash("Loggen In Successfully as Professional")
                    return redirect(url_for("main.dashboard"))
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
        blocked = False

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
            new_customer = Customer(c_name = username, c_email = email, c_city = city, c_pincode = pincode, c_user_id = new_user.u_id, c_blocked = blocked)
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
        approved = False
        blocked = False

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
        new_provider = ServiceProvider(p_name = username, p_email = email, p_contact_number = contact_number, p_experience = experience, p_city = city, p_pincode = pincode, p_user_id = new_user.u_id, p_service_id = service_id, p_approved = approved, p_blocked = blocked)
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



def requires_admin(my_fucntion):
    @wraps(my_fucntion)
    def main_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please Login")
            return redirect(url_for("main.login"))
        user = User.query.filter_by(u_id = session["user_id"]).first()
        if user.u_role != 0:
            flash("You do not have permission to access this page")
            return redirect(url_for("main.dashboard"))
        return my_fucntion(*args, **kwargs)
    return main_function

from datetime import datetime

@my_blueprint.route("/dashboard")
@requires_login
def dashboard():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 0:
        services = Service.query.all()
        services_providers = ServiceProvider.query.all()
       
        return render_template("admin_dashboard.html" , services = services, services_providers = services_providers)
    elif user.u_role == 1:
        services = Service.query.all()
        customer = Customer.query.filter_by(c_user_id = session["user_id"]).first()
        service_requests = ServiceRequest.query.filter_by(sr_customer_id = customer.c_id).all()
        service_categories = ServiceCategory.query.all()
        return render_template("customer_dashboard.html", services = services, service_requests = service_requests, service_categories = service_categories)

    elif user.u_role == 2:
        user = User.query.filter_by(u_id = session["user_id"]).first()
        service_provider = ServiceProvider.query.filter_by(p_user_id = user.u_id).first()
        service_requests = ServiceRequest.query.filter_by(sr_service_provider_id = service_provider.p_id).all()
        customer_ids = {request.sr_customer_id for request in service_requests}
        customers = Customer.query.filter(Customer.c_id.in_(customer_ids)).all()
        service_feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id = service_provider.p_id).all()
        return render_template("service_provider_dashboard.html", service_requests = service_requests, customers = customers, service_provider = service_provider, service_feedbacks = service_feedbacks)






@my_blueprint.route("/logout")
@requires_login
def logout():
    session.pop("user_id")
    flash("Logged Out Successfully")
    return redirect(url_for("main.login"))

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


            if not username:
                flash("All fields are required")
                return redirect(url_for("main.profile"))
        
            
            if username != user.u_name:
                new_username = User.query.filter_by(u_name = username).first()
                if new_username:
                    flash("Username already exist")
                    return redirect(url_for("main.profile"))
            user.u_name = username
            db.session.commit()
            flash("Profile Updated Successfully")
            return redirect(url_for("main.profile"))

        elif user.u_role == 1:
            username = request.form.get("username")
            city = request.form.get("City")
            pincode = request.form.get("pincode")

            if not username or not city or not pincode:
                flash("All fields are required")
                return redirect(url_for("main.profile"))
            


            
            if username != user.u_name:
                new_username = User.query.filter_by(u_name = username).first()
                if new_username:
                    flash("Username already exist")
                    return redirect(url_for("main.profile"))

            user.u_name = username

            c_user = Customer.query.filter_by(c_user_id = session["user_id"])
            c_user.c_name = username
            c_user.c_city = city
            c_user.c_pincode = pincode
            db.session.commit()
            flash("Profile Updated Successfully")
            return redirect(url_for("main.profile"))
        
        elif user.u_role == 2:
            username = request.form.get("username")
            contact_number = request.form.get("inputPhone")
            address = request.form.get("inputAddress")
            city = request.form.get("inputCity")
            pincode = request.form.get("inputPincode")

            if not username or not contact_number or not address or not city or not pincode:
                flash("All fields are required")
                return redirect(url_for("main.profile"))

            
            if username != user.u_name:
                new_username = User.query.filter_by(u_name = username).first()
                if new_username:
                    flash("Username already exist")
                    return redirect(url_for("main.profile"))

            user.u_name = username
            p_user = ServiceProvider.query.filter_by(p_user_id = session["user_id"]).first()
            p_user.p_name = username
            p_user.p_city = city
            p_user.p_pincode = pincode
            p_user.p_address = address
            p_user.p_contact_namer = contact_number
            db.session.commit()
            flash("Profile Updated Successfully")
            return redirect(url_for("main.profile"))
        

@my_blueprint.route("/update_password", methods = ["GET", "POST"])
@requires_login
def update_password():
    if request.method == "GET":
        return render_template("update_password.html")
    elif request.method == "POST":
        user = User.query.filter_by(u_id = session["user_id"]).first()
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_password or not new_password or not confirm_password:
            flash("All fields are required")
            return redirect(url_for("main.update_password"))
        
        if not check_password_hash(user.u_passhash, current_password):
            flash("Invalid Password")
            return redirect(url_for("main.update_password"))
        
        if new_password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("main.update_password"))
        
        new_passhash = generate_password_hash(new_password)
        user.u_passhash = new_passhash
        db.session.commit()
        flash("Password Updated Successfully")
        return redirect(url_for("main.profile"))
    
@my_blueprint.route("/category_services/<int:s_category_id>")
@requires_login
def services(s_category_id):
    services = Service.query.filter_by(s_category_id = s_category_id).all()
    service_category = ServiceCategory.query.filter_by(sc_id = s_category_id).first()
    return render_template("services.html", services = services, service_category = service_category)

@my_blueprint.route("/category_service/<int:s_category_id>")
def service(s_category_id):
    if "user_id" in session:
        return redirect(url_for("main.services", s_category_id = s_category_id))
    services = Service.query.filter_by(s_category_id = s_category_id).all()
    service_category = ServiceCategory.query.filter_by(sc_id = s_category_id).first()
    return render_template("service.html", services = services, service_category = service_category)

@my_blueprint.route("/search", methods = ["GET", "POST"])
@requires_login
def search():
    return "Search Page"

@my_blueprint.route("/summary")
@requires_login
def summary():
    return "Summary Page"


@my_blueprint.route("/service/<int:service_id>/edit", methods = ["GET", "POST"])
@requires_admin
def edit_service(service_id):
    service = Service.query.filter_by(s_id = service_id).first()
    service_categories = ServiceCategory.query.all()
    if request.method == "GET":
        return render_template("edit_service.html", service = service, service_categories = service_categories)
    elif request.method == "POST":
        s_name = request.form.get("s_name")
        s_rate = request.form.get("s_rate")
        s_description = request.form.get("s_description")
        s_time_required = request.form.get("s_time_required")
        s_category_id = request.form.get("s_category_id")

        if not s_name or not s_rate or not s_description or not s_time_required or not s_category_id:
            flash("All fields are required")
            return redirect(url_for("main.edit_service", service_id = service_id))
        
        service.s_name = s_name
        service.s_rate = s_rate
        service.s_description = s_description
        service.s_time_required = s_time_required
        service.s_category_id = s_category_id
        db.session.commit()
        flash("Service Updated Successfully")
        return redirect(url_for("main.dashboard"))


@my_blueprint.route("/service/<int:service_id>/delete")
@requires_admin
def delete_service(service_id):
    service = Service.query.filter_by(s_id = service_id).first()
    db.session.delete(service)
    db.session.commit()
    flash("Service Deleted Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service/add", methods = ["GET", "POST"])
@requires_admin
def add_service():
    if request.method == "GET":
        service_categories = ServiceCategory.query.all()
        return render_template("add_service.html", service_categories = service_categories)
    elif request.method == "POST":
        s_name = request.form.get("s_name")
        s_rate = request.form.get("s_rate")
        s_description = request.form.get("s_description")
        s_time_required = request.form.get("s_time_required")
        s_catergory_id = request.form.get("s_category_id")

        if not s_name or not s_rate or not s_description or not s_time_required or not s_catergory_id:
            flash("All fields are required")
            return redirect(url_for("main.add_service"))
        
        new_service = Service(s_name = s_name, s_rate = s_rate, s_description = s_description, s_time_required = s_time_required, s_category_id = s_catergory_id)
        db.session.add(new_service)
        db.session.commit()
        flash("Service Added Successfully")
        return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_request/<int:s_id>")
@requires_login
def service_request(s_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        sr_customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        sr_service_provider = ServiceProvider.query.filter_by(p_service_id = s_id).first()
        sr_status = "Requested"
        sr_date_time = datetime.now(tz=None)
        new_service_request = ServiceRequest(sr_customer_id = sr_customer.c_id, sr_service_provider_id = sr_service_provider.p_id, sr_service_id = s_id, sr_status = sr_status, sr_date_time = sr_date_time)
        db.session.add(new_service_request)
        db.session.commit()
        flash("Service Requested Successfully")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 2:
        flash("Professional cannot request service")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 0:
        flash("Admin cannot request service")
        return redirect(url_for("main.dashboard"))


@my_blueprint.route("/service_provider/<int:provider_id>/approve")
@requires_admin
def approve_service_provider(provider_id):
    provider = ServiceProvider.query.filter_by(p_id = provider_id).first()
    provider.p_approved = True
    db.session.commit()
    flash("Service Provider Approved Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_provider/<int:provider_id>/block")
@requires_admin
def block_service_provider(provider_id):
    provider = ServiceProvider.query.filter_by(p_id = provider_id).first()
    provider.p_blocked = True
    db.session.commit()
    flash("Service Provider Blocked Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_provider/<int:provider_id>/unblock")
@requires_admin
def unblock_service_provider(provider_id):
    provider = ServiceProvider.query.filter_by(p_id = provider_id).first()
    provider.p_blocked = False
    db.session.commit()
    flash("Service Provider Unblocked Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_provider/<int:provider_id>/delete")
@requires_admin
def delete_service_provider(provider_id):
    provider = ServiceProvider.query.filter_by(p_id = provider_id).first()
    user = User.query.filter_by(u_id = provider.p_user_id).first()
    db.session.delete(user)
    db.session.delete(provider)
    db.session.commit()
    flash("Service Provider Deleted Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_provider/<int:provider_id>/")
def view_service_provider(provider_id):
    provider = ServiceProvider.query.filter_by(p_id = provider_id).first()
    service = Service.query.filter_by(s_id = provider.p_service_id).first()
    service_requests = ServiceRequest.query.filter_by(sr_service_provider_id = provider_id).all()
    service_feedback = ServiceFeedback.query.filter_by(sf_service_provider_id = provider_id).all()
    return render_template("service_provider_profile.html", provider = provider, service = service, service_requests = service_requests, service_feedback = service_feedback)

@my_blueprint.route("/service_request/<int:sr_id>/accept")
@requires_login
def accept_request(sr_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 2:
        service_request = ServiceRequest.query.filter_by(sr_id = sr_id).first()
        service_request.sr_status = "Assigned"
        db.session.commit()
        flash("Service Request Approved Successfully")
        return redirect(url_for("main.dashboard"))
    else:
        flash("You do not have permission to access this page")
        return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_request/<int:sr_id>/reject")
@requires_login
def reject_request(sr_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 2:
        service_request = ServiceRequest.query.filter_by(sr_id = sr_id).first()
        service_request.sr_status = "Rejected"
        db.session.commit()
        flash("Service Request Rejected")
        return redirect(url_for("main.dashboard"))
    else:
        flash("You do not have permission to access this page")
        return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_request/<int:sr_id>/completed", methods = ["GET", "POST"])
@requires_login
def service_completed(sr_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        if request.method == "GET":
            service_request = ServiceRequest.query.filter_by(sr_id = sr_id).first()
            service_provider = ServiceProvider.query.filter_by(p_id = service_request.sr_service_provider_id).first()
            service = Service.query.filter_by(s_id = service_request.sr_service_id).first()
            completion_date_time = datetime.now(tz=None)
            service_request.sr_date_time = completion_date_time
            return render_template("feedback.html", service_request = service_request, service_provider = service_provider, service = service, completion_date_time = completion_date_time)
        elif request.method == "POST":
            service_request = ServiceRequest.query.filter_by(sr_id = sr_id).first()
            sf_service_request_id = service_request.sr_service_provider_id
            sf_rating = request.form.get("service_rating")
            sf_customer_id  = service_request.sr_customer_id
            sf_service_provider_id = service_request.sr_service_provider_id
            sf_feedback = request.form.get("service_feedback")

            if not sf_rating or not sf_feedback:
                flash("All fields are required")
                return redirect(url_for("main.service_completed", sr_id = sr_id))
            
            new_service_feedback = ServiceFeedback(sf_service_request_id = sf_service_request_id, sf_rating = sf_rating, sf_customer_id = sf_customer_id, sf_service_provider_id = sf_service_provider_id, sf_feedback = sf_feedback)
            service_request.sr_status = "Closed"
            db.session.add(new_service_feedback)
            db.session.commit()
            flash("Service Request Completed Successfully")
            return redirect(url_for("main.dashboard"))
    else:
        flash("You do not have permission to access this page")
        return redirect(url_for("main.dashboard"))

@my_blueprint.route("/blocked")
@requires_login
def blocked():
    flash("You have been blocked by the admin. Please contact the admin for further details")
    return redirect(url_for("main.dashboard"))