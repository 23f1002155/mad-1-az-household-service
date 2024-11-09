from flask import request, flash, redirect, url_for, session
from flask import render_template
from flask import Blueprint
from application.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from functools import wraps

my_blueprint = Blueprint('main', __name__)


@my_blueprint.route("/", methods = ["GET", "POST"])
def home():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))
    service_categories = ServiceCategory.query.all()
    top_services = Service.query.order_by(func.random()).limit(2).all()
    all_services = Service.query.all()
    return render_template("home.html", service_categories = service_categories, services = top_services, all_services = all_services)

@my_blueprint.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("main.dashboard"))
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
        if "user_id" in session:
            return redirect(url_for("main.dashboard"))
        return render_template("sign-up-customer.html")
    elif request.method == "POST":
        c_name = request.form.get("inputName")
        c_email = request.form.get("inputEmail4")
        c_fname = request.form.get("inputFirstName")
        c_lname = request.form.get("inputLastName")
        c_password = request.form.get("inputPassword4")
        c_confirm_password = request.form.get("inputConfirmPassword4")
        c_address = request.form.get("inputAddress")
        c_city = request.form.get("inputCity")
        c_pincode = request.form.get("inputZip")
        blocked = False

        if not c_name or not c_email or not c_password or not c_confirm_password or not c_city or not c_pincode or not c_address or not c_fname or not c_lname:
            flash("All fields are required")
            return redirect(url_for("main.sign_up_customer"))
        if " " in c_name:
            flash("Username cannot have spaces")
            return redirect(url_for("main.sign_up_customer"))
        
        if ' ' in c_email:
            flash("Email cannot have spaces")
            return redirect(url_for("main.sign_up_customer"))
        
        if len(c_password) < 8:
            flash("Password should be atleast 8 characters long")
            return redirect(url_for("main.sign_up_customer"))
        
        if c_password != c_confirm_password:    
            flash("Passwords do not match")
            return redirect(url_for("main.sign_up_customer"))
        
        username = User.query.filter_by(u_name = c_name).first()
        user_email = User.query.filter_by(u_email = c_email).first()

        if username:
            flash("Username already exists")
            return redirect(url_for("main.sign_up_customer"))
        if user_email:
            flash("Email already exists")
            return redirect(url_for("main.sign_up_customer"))
        else:
            passhash = generate_password_hash(c_password)
            new_user = User(u_name = c_name, u_email = c_email, u_passhash = passhash, u_role = 1)
            db.session.add(new_user)
            db.session.commit()
            new_customer = Customer(c_name = c_name, c_email = c_email, c_fname = c_fname, c_lname = c_lname, c_address = c_address, c_city = c_city, c_pincode = c_pincode, c_user_id = new_user.u_id, c_blocked = blocked)
            db.session.add(new_customer)
            db.session.commit()
            flash("Account Created Successfully")
            return redirect(url_for("main.login"))



@my_blueprint.route("/sign-up-serviceprovider", methods = ["GET", "POST"])
def sign_up_serviceprovider():
    if request.method == "GET":
        if "user_id" in session:
            return redirect(url_for("main.dashboard"))
        services = Service.query.all()
        return render_template("sign-up-serviceprovider.html", services = services)
    elif request.method == "POST":
        p_name = request.form.get("inputName")
        p_email = request.form.get("inputEmail4")
        p_fname = request.form.get("inputFirstName")
        p_lname = request.form.get("inputLastName")
        p_password = request.form.get("inputPassword4")
        p_confirm_password = request.form.get("inputConfirmPassword4")
        p_contact_number = request.form.get("inputPhone")
        p_service_id= request.form.get("inputService")
        p_experience = request.form.get("inputExperience")
        p_verfiication_document = request.files.get("inputVerificationDocument")
        if not p_verfiication_document:
            flash("Please upload a verification document")
            return redirect(url_for("main.sign_up_serviceprovider"))
        else:
            p_verfiication_document.save(f"static/verification/{p_verfiication_document.filename}")
        p_address = request.form.get("inputAddress")
        p_city = request.form.get("inputCity")
        p_pincode = request.form.get("inputZip")
        p_approved = False
        p_blocked = False

        if not p_name or not p_email or not p_password or not p_confirm_password or not p_contact_number or not p_service_id or not p_experience or not p_address or not p_city or not p_pincode or not p_fname or not p_lname:
            flash("All fields are required")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        if " " in p_name:
            flash("Username cannot have spaces")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        if ' ' in p_email:
            flash("Email cannot have spaces")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        if len(p_password) < 8:
            flash("Password should be atleast 8 characters long")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        if p_password != p_confirm_password:    
            flash("Passwords do not match")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        username = User.query.filter_by(u_name = p_name).first()
        if username:
            flash("Username already exists")
            return redirect(url_for("main.sign_up_serviceprovider"))

        useremail = User.query.filter_by(u_email = p_email).first()
        if useremail:
            flash("Email already exists")
            return redirect(url_for("main.sign_up_serviceprovider"))
        
        passhash = generate_password_hash(p_password)

        new_user = User(u_name = p_name, u_email = p_email, u_passhash = passhash, u_role = 2)
        
        db.session.add(new_user)
        db.session.commit()
        new_provider = ServiceProvider(p_name = p_name, p_email = p_email, p_fname = p_fname, p_lname = p_lname, p_contact_number = p_contact_number, p_experience = p_experience, p_city = p_city, p_pincode = p_pincode, p_user_id = new_user.u_id, p_service_id = p_service_id, p_approved = p_approved, p_blocked = p_blocked, p_verification_document = p_verfiication_document.filename, p_address = p_address)
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
from sqlalchemy.orm import aliased

@my_blueprint.route("/dashboard")
@requires_login
def dashboard():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 0:
        services = Service.query.all()
        services_providers = ServiceProvider.query.all()
        customers = Customer.query.all()
        categories = ServiceCategory.query.all()
        service_requests = ServiceRequest.query.all()
        return render_template("admin_dashboard.html" , services = services, services_providers = services_providers, service_requests = service_requests, customers = customers, categories = categories, user_role = user.u_role)
    elif user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = session["user_id"]).first()
        service_requests = ServiceRequest.query.filter_by(sr_customer_id = customer.c_id).all()
        service_ids = {request.sr_service_id for request in service_requests}
        services = Service.query.filter(Service.s_id.in_(service_ids)).all()
        service_categories = ServiceCategory.query.all()
        return render_template("customer_dashboard.html", service_categories = service_categories, service_requests = service_requests, user_role = user.u_role)

    elif user.u_role == 2:
        user = User.query.filter_by(u_id = session["user_id"]).first()
        service_provider = ServiceProvider.query.filter_by(p_user_id = user.u_id).first()
        service_requests = ServiceRequest.query.filter_by(sr_service_provider_id = service_provider.p_id).all()
        service_feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id = service_provider.p_id).all()
        if not service_requests:
            flash("No Service Requests")
            return redirect(url_for("main.profile"))
        if not service_feedbacks:
            flash("No Feedbacks")
            return redirect(url_for("main.profile"))

        return render_template("service_provider_dashboard.html", service_feedbacks = service_feedbacks, service_requests = service_requests, user_role = user.u_role)






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
            return render_template("profile.html", user = user, c_user = c_user, user_role = user.u_role)
        elif user.u_role == 2:
            p_user = ServiceProvider.query.filter_by(p_user_id = user.u_id).first()
            p_service = Service.query.filter_by(s_id = p_user.p_service_id).first()
            return render_template("profile.html", user = user, p_user = p_user, p_service = p_service, user_role = user.u_role)
        return render_template("profile.html", user = user, user_role = user.u_role)
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
            address = request.form.get("inputAddress")
            city = request.form.get("inputCity")
            pincode = request.form.get("inputPincode")

            if not username or not city or not pincode or not address:
                flash("All fields are required")
                return redirect(url_for("main.profile"))
            


            
            if username != user.u_name:
                new_username = User.query.filter_by(u_name = username).first()
                if new_username:
                    flash("Username already exist")
                    return redirect(url_for("main.profile"))

            user.u_name = username

            c_user = Customer.query.filter_by(c_user_id = session["user_id"]).first()
            c_user.c_name = username
            c_user.c_address = address
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
            p_user.p_contact_number = contact_number
            db.session.commit()
            flash("Profile Updated Successfully")
            return redirect(url_for("main.profile"))
        

@my_blueprint.route("/update_password", methods = ["GET", "POST"])
@requires_login
def update_password():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if request.method == "GET":
        return render_template("update_password.html" , user_role = user.u_role)
    elif request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_password or not new_password or not confirm_password:
            flash("All fields are required")
            return redirect(url_for("main.update_password"))
        
        if not check_password_hash(user.u_passhash, current_password):
            flash("Invalid Current Password")
            return redirect(url_for("main.update_password"))
        
        if new_password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("main.update_password"))
        if current_password == new_password:
            flash("Current Password and New Password Cannot be Same")
            return redirect(url_for("main.update_password"))
        
        new_passhash = generate_password_hash(new_password)
        user.u_passhash = new_passhash
        db.session.commit()
        flash("Password Updated Successfully")
        return redirect(url_for("main.profile"))
    
@my_blueprint.route("/category_services/<int:s_category_id>")
@requires_login
def services(s_category_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    services = Service.query.filter_by(s_category_id = s_category_id).all()
    service_category = ServiceCategory.query.filter_by(sc_id = s_category_id).first()
    return render_template("services.html", services = services, service_category = service_category, user_role = user.u_role)

@my_blueprint.route("/category_service/<int:s_category_id>")
def service(s_category_id):
    if "user_id" in session:
        return redirect(url_for("main.services", s_category_id = s_category_id))
    services = Service.query.filter_by(s_category_id = s_category_id).all()
    service_category = ServiceCategory.query.filter_by(sc_id = s_category_id).first()
    return render_template("service.html", services = services, service_category = service_category)

@my_blueprint.route("/search")
@requires_login
def search():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        return render_template("customer_search.html", user_role = user.u_role)

@my_blueprint.route("/searches")
@requires_login
def search_from_header():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        parameter = request.args.get("parameter")
        query = request.args.get("query").strip()
        service_providers = ServiceProvider.query.filter_by(p_approved = True, p_blocked = False).all()

        service_providers_and_ratings = []
        for service_provider in service_providers:
            feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id= service_provider.p_id).all()
            if feedbacks:
                average_rating = sum(feedback.sf_rating for feedback in feedbacks) / len(feedbacks)
            else:
                average_rating = "No Ratings"
            service_providers_and_ratings.append((service_provider, average_rating))
        
        if not query:
            flash("Please enter a search term")
            return redirect(request.referrer)
        if parameter == "parameter":
            flash("Please select a search by option")
            return redirect(request.referrer)

        search_result = []
        if parameter == "p_name":
            search_result = [service_provider for service_provider in service_providers_and_ratings if query.lower() in service_provider[0].p_name.lower()]
        elif parameter == "p_city":
            search_result = [service_provider for service_provider in service_providers_and_ratings if query.lower() in service_provider[0].p_city.lower()]
        elif parameter == "p_pincode":
            search_result = [service_provider for service_provider in service_providers_and_ratings if int(query) == int(service_provider[0].p_pincode)]
        elif parameter == "p_experience":
            search_result = [service_provider for service_provider in service_providers_and_ratings if int(query) <= int(service_provider[0].p_experience)]
        elif parameter == "s_name":
            search_result = [service_provider for service_provider in service_providers_and_ratings if query.lower() in service_provider[0].service.s_name.lower()]
        elif parameter == "rating":
            search_result = [service_provider for service_provider in service_providers_and_ratings if query <= service_provider[1]]
        if not search_result:
            return render_template("No_Results_Found.html", user_role = user.u_role)
        return render_template("customer_search_result.html", search_result = search_result, user_role = user.u_role)
    elif user.u_role == 2:
        parameter = request.args.get("parameter")
        query = request.args.get("query").strip()
        service_provider = ServiceProvider.query.filter_by(p_user_id = user.u_id).first()
        service_requests = ServiceRequest.query.filter_by(sr_service_provider_id = service_provider.p_id).all()
        

        if parameter == "parameter":
            flash("Please select a search by option")
            return redirect(request.referrer)

        if not query:
            flash("Please enter a search term")
            return redirect(request.referrer)

        if query == "-" or query == ":":
            flash("Please enter a valid search term")
            return redirect(request.referrer)

        
        search_result = []
        if parameter == "sr_id":
            search_result = [request for request in service_requests if int(query) == request.sr_id]
        elif parameter == "customer_name":
            search_result = [request for request in service_requests if query.lower() in request.sr_customer_name.lower()]
        elif parameter == "customer_city":
            search_result = [request for request in service_requests if query.lower() in request.sr_city.lower()]
        elif parameter == "customer_pincode":
            search_result = [request for request in service_requests if int(query) == request.sr_pincode]
        elif parameter == "sr_date_time":
            search_result = [request for request in service_requests if query in str(request.sr_date_time)]
        elif parameter == "sr_status":
            search_result = [request for request in service_requests if query.lower() in request.sr_status.lower()]
        if not search_result:
            return render_template("No_Results_Found.html", user_role = user.u_role)
        return render_template("service_provider_result.html", search_result = search_result, user_role = user.u_role)
    
    elif user.u_role == 0:
        parameter = request.args.get("parameter")
        query = request.args.get("query").strip()
        service_requests = ServiceRequest.query.all()
        customers = Customer.query.all()
        services = Service.query.all()
        service_providers_avg = db.session.query(
            ServiceProvider.p_name,
            ServiceProvider.p_id,
            ServiceProvider.p_city,
            ServiceProvider.p_pincode,
            ServiceProvider.p_experience,
            ServiceProvider.p_service_id,
            ServiceProvider.p_verification_document,
            ServiceProvider.p_email,
            ServiceProvider.p_contact_number,
            ServiceProvider.p_approved,
            ServiceProvider.p_blocked,
            Service.s_name.label('s_name'),
            func.avg(ServiceFeedback.sf_rating).label('average_rating')
        ).join(ServiceFeedback, ServiceProvider.p_id == ServiceFeedback.sf_service_provider_id, isouter=True).join(
            Service, ServiceProvider.p_service_id == Service.s_id
        ).group_by(ServiceProvider.p_id).all()

        if not query:
            flash("Please enter a search term")
            return redirect(request.referrer)
        if query == "-" or query == ":":
            flash("Please enter a valid search term")
            return redirect(request.referrer)

        if parameter == "parameter":
            flash("Please select a search by option")
            return redirect(request.referrer)
        
        service_search_result = []
        service_provider_search_result = []
        customer_search_result = []
        service_request_search_result = []

        if parameter == "sc_name" or parameter == "s_name":
            service_search_result = [service for service in services if query.lower() in service.s_name.lower() or query.lower() in service.category.sc_name.lower()]
        elif parameter == "p_name":
            service_provider_search_result = [service_provider for service_provider in service_providers_avg if query in service_provider.p_name]
        elif parameter == "c_name":
            customer_search_result = [customer for customer in customers if query.lower() in customer.c_name.lower()]
        elif parameter == "sr_id":
            service_request_search_result = ServiceRequest.query.filter_by(sr_id = int(query)).all()
        elif parameter == "sr_date_time":
            service_request_search_result = [service_request for service_request in service_requests if query in str(request.sr_date_time)]
        elif parameter == "rating":
            service_provider_search_result = [service_provider for service_provider in service_providers_avg if float(query) <= service_provider.average_rating]
        
        if service_search_result or  service_provider_search_result or  customer_search_result or  service_request_search_result:
            return render_template("admin_search_result.html", service_search_result = service_search_result, service_provider_search_result = service_provider_search_result, customer_search_result = customer_search_result, service_request_search_result = service_request_search_result, user_role = user.u_role)
        return render_template("No_Results_Found.html", user_role = user.u_role)

        

@my_blueprint.route("/summary")
@requires_login
def summary():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 0:
        users = User.query.all()
        total_users = len(users) -1
        customes = Customer.query.all()
        total_customers = len(customes)
        service_providers = ServiceProvider.query.all()
        total_service_providers = len(service_providers)
        service_requests = ServiceRequest.query.all()
        total_service_requests = len(service_requests) 
        total_requested_services = len([request for request in service_requests if request.sr_status == "Requested"])
        total_assigned_services = len([request for request in service_requests if request.sr_status == "Assigned"])
        total_rejected_services = len([request for request in service_requests if request.sr_status == "Rejected"])
        total_closed_services = len([request for request in service_requests if request.sr_status == "Closed"])
        return render_template("admin_summary.html", total_users = total_users, total_customers = total_customers, total_service_providers = total_service_providers, total_service_requests = total_service_requests, total_requested_services = total_requested_services, total_assigned_services = total_assigned_services, total_rejected_services = total_rejected_services, total_closed_services = total_closed_services, user_role = user.u_role)

    elif user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = session["user_id"]).first()
        service_requests = ServiceRequest.query.filter_by(sr_customer_id = customer.c_id).all()
        total_service_requests = len(service_requests)
        total_requested_services = len([request for request in service_requests if request.sr_status == "Requested"])
        total_assigned_services = len([request for request in service_requests if request.sr_status == "Assigned"])
        total_rejected_services = len([request for request in service_requests if request.sr_status == "Rejected"])
        total_closed_services = len([request for request in service_requests if request.sr_status == "Closed"])
        return render_template("customer_summary.html", total_service_requests = total_service_requests, total_requested_services = total_requested_services, total_assigned_services = total_assigned_services, total_rejected_services = total_rejected_services, total_closed_services = total_closed_services, user_role = user.u_role)

    elif user.u_role == 2:
        service_provider = ServiceProvider.query.filter_by(p_user_id = session["user_id"]).first()
        service_requests = ServiceRequest.query.filter_by(sr_service_provider_id = service_provider.p_id).all()
        total_service_requests = len(service_requests)
        total_requested_services = len([request for request in service_requests if request.sr_status == "Requested"])
        total_assigned_services = len([request for request in service_requests if request.sr_status == "Assigned"])
        total_rejected_services = len([request for request in service_requests if request.sr_status == "Rejected"])
        total_closed_services = len([request for request in service_requests if request.sr_status == "Closed"])
        service_feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id = service_provider.p_id).all()
        ratings_count = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0
        }

        for feedback in service_feedbacks:
            if 0 <= feedback.sf_rating == 1:
                ratings_count["1"] += 1
            elif 1 < feedback.sf_rating == 2:
                ratings_count["2"] += 1
            elif 2 < feedback.sf_rating == 3:
                ratings_count["3"] += 1
            elif 3 < feedback.sf_rating == 4:
                ratings_count["4"] += 1
            elif 4 < feedback.sf_rating == 5:
                ratings_count["5"] += 1

        return render_template("service_provider_summary.html", total_service_requests = total_service_requests, total_requested_services = total_requested_services, total_assigned_services = total_assigned_services, total_rejected_services = total_rejected_services, total_closed_services = total_closed_services, ratings_count = ratings_count, user_role = user.u_role)

@my_blueprint.route("/service/<int:service_id>/edit", methods = ["GET", "POST"])
@requires_admin
def edit_service(service_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    service = Service.query.filter_by(s_id = service_id).first()
    service_categories = ServiceCategory.query.all()
    if request.method == "GET":
        return render_template("edit_service.html", service = service, service_categories = service_categories, user_role = user.u_role)
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

@my_blueprint.route("/service_category/<int:sc_id>/edit", methods = ["GET", "POST"])
@requires_admin
def edit_service_category(sc_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    service_category = ServiceCategory.query.filter_by(sc_id = sc_id).first()
    if request.method == "GET":
        return render_template("edit_category.html", user_role = user.u_role, service_category = service_category)
    elif request.method == "POST":
        sc_name = request.form.get("sc_name")
        if not sc_name:
            flash("Please Enter the Service Category Name")
            return redirect(url_for("main.edit_service_category"))

        service_category.sc_name = sc_name
        db.session.commit()
        flash("Service Category edited Successfully")
        return redirect(url_for("main.dashboard"))



@my_blueprint.route("/service/<int:service_id>/delete")
@requires_admin
def delete_service(service_id):
    service = Service.query.filter_by(s_id = service_id).first()
    db.session.delete(service)
    db.session.commit()
    flash("Service Deleted Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_category/<int:sc_id>/delete")
@requires_admin
def delete_service_category(sc_id):
    service_category = ServiceCategory.query.filter_by(sc_id = sc_id).first()
    db.session.delete(service_category)
    db.session.commit()
    flash("Service Deleted Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service/add", methods = ["GET", "POST"])
@requires_admin
def add_service():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if request.method == "GET":
        service_categories = ServiceCategory.query.all()
        return render_template("add_service.html", service_categories = service_categories, user_role = user.u_role)
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

@my_blueprint.route("/service_category/add", methods = ["GET", "POST"])
@requires_admin
def add_category():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if request.method == "GET":
        return render_template("add_category.html", user_role = user.u_role)
    elif request.method == "POST":
        sc_name = request.form.get("sc_name")
        if not sc_name:
            flash("Please Enter the Service Category Name")
            return redirect(url_for("main.add_category"))
        service_catergory = ServiceCategory(sc_name = sc_name)
        db.session.add(service_catergory)
        db.session.commit()
        flash("Service Category Added Successfully")
        return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_request", methods = ["POST"])
@requires_login
def service_request():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        sr_customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        if sr_customer.c_blocked:
            flash("You are blocked by admin. Please contact admin for further details")
            return redirect(url_for("main.dashboard"))
        t_date_time = request.form.get("sr_date_time")
        new_t_date_time = datetime.strptime(t_date_time, '%d %B %Y %I:%M %p')
        new_transaction = Transaction(t_customer_id = sr_customer.c_id, t_date_time = new_t_date_time)
        db.session.add(new_transaction)
        db.session.commit()
        carts = Cart.query.filter_by(cart_customer_id = sr_customer.c_id).all()
        for cart in carts:
            sr_service_provider_fullname = cart.service_provider.p_fname + " " + cart.service_provider.p_lname
            sr_customer_fullname = sr_customer.c_fname + " " + sr_customer.c_lname
            new_service_request = ServiceRequest( sr_transaction_id = new_transaction.t_id, sr_customer_id = sr_customer.c_id, sr_customer_name = sr_customer.c_name, sr_customer_email = sr_customer.c_email, sr_customer_fullname = sr_customer_fullname, sr_address = sr_customer.c_address, sr_city = sr_customer.c_city, sr_pincode = sr_customer.c_pincode, sr_service_id = cart.service.s_id, sr_service_name = cart.service.s_name, sr_date_time = new_t_date_time, sr_status = "Requested", sr_service_provider_id = cart.service_provider.p_id, sr_service_provider_name = cart.service_provider.p_name, sr_service_provider_fullname = sr_service_provider_fullname, sr_service_provider_email = cart.service_provider.p_email, sr_service_provider_contact_number = cart.service_provider.p_contact_number)
            db.session.add(new_service_request)
            db.session.delete(cart)
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

@my_blueprint.route("/customer/<int:c_id>/block")
@requires_admin
def block_customer(c_id):
    customer = Customer.query.filter_by(c_id = c_id).first()
    customer.c_blocked = True
    db.session.commit()
    flash("Customer Blocked Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/customer/<int:c_id>/unblock")
@requires_admin
def unblock_customer(c_id):
    customer = Customer.query.filter_by(c_id = c_id).first()
    customer.c_blocked = False
    db.session.commit()
    flash("Customer Unblocked Successfully")
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

@my_blueprint.route("/customer/<int:c_id>/delete")
@requires_admin
def delete_customer(c_id):
    customer = Customer.query.filter_by(c_id = c_id).first()
    user = User.query.filter_by(u_id = customer.c_user_id).first()
    db.session.delete(user)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer Deleted Successfully")
    return redirect(url_for("main.dashboard"))

@my_blueprint.route("/service_provider/<int:provider_id>/")
@requires_login
def view_service_provider(provider_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    provider = ServiceProvider.query.filter_by(p_id = provider_id).first()
    service = Service.query.filter_by(s_id = provider.p_service_id).first()
    service_requests = ServiceRequest.query.filter_by(sr_service_provider_id = provider_id).all()
    service_feedback = ServiceFeedback.query.filter_by(sf_service_provider_id = provider_id).all()
    return render_template("service_provider_profile.html", provider = provider, service = service, service_requests = service_requests, service_feedback = service_feedback, user_role = user.u_role)

@my_blueprint.route("/service_request/<int:sr_id>/accept")
@requires_login
def accept_request(sr_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 2:
        service_provider = ServiceProvider.query.filter_by(p_user_id = user.u_id).first()
        if service_provider.p_blocked:
            flash("You are blocked by admin. Please contact admin for further details")
            return redirect(url_for("main.dashboard"))
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
            new_completion_date_time = completion_date_time.strftime('%d %b %Y %I:%M %p')
            return render_template("feedback.html", service_request = service_request, service_provider = service_provider, service = service, completion_date_time = new_completion_date_time, user_role = user.u_role)
        elif request.method == "POST":
            service_request = ServiceRequest.query.filter_by(sr_id = sr_id).first()
            sf_service_request_id = sr_id
            sf_rating = request.form.get("service_rating")
            sf_customer_id  = service_request.sr_customer_id
            sf_service_provider_id = service_request.sr_service_provider_id
            sf_feedback = request.form.get("service_feedback")


            if not sf_rating or not sf_feedback:
                flash("All fields are required")
                return redirect(url_for("main.service_completed", sr_id = sr_id))
            
            new_service_feedback = ServiceFeedback(sf_service_request_id = sf_service_request_id, sf_rating = sf_rating, sf_customer_id = sf_customer_id, sf_service_provider_id = sf_service_provider_id, sf_feedback = sf_feedback)
            service_request.sr_status = "Closed"
            completion_date_time_str = request.form.get("completion_date_time")
            service_request.sr_date_time = datetime.strptime(completion_date_time_str, '%d %b %Y %I:%M %p')
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

@my_blueprint.route("/professional_list/<int:s_id>")
@requires_login
def professional_list(s_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        service = Service.query.filter_by(s_id = s_id).first()
        carts = Cart.query.filter_by(cart_customer_id = customer.c_id).all()
        cart_professional_ids = [cart.cart_service_provider_id for cart in carts]
        service_providers = ServiceProvider.query.filter_by(p_service_id = s_id, p_approved = True, p_city = customer.c_city).all()
        service_providers_and_ratings = []
        for service_provider in service_providers:
            feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id= service_provider.p_id).all()
            if feedbacks:
                average_rating = sum(feedback.sf_rating for feedback in feedbacks) / len(feedbacks)
            else:
                average_rating = "No Ratings"
            service_providers_and_ratings.append((service_provider, average_rating))
        
        service_providers_and_ratings = sorted(service_providers_and_ratings, key = lambda x: x[1], reverse = True)
        if service_providers_and_ratings:
            return render_template("professional_list.html", service=service, service_providers_and_ratings=service_providers_and_ratings, user_role = user.u_role, customer = customer, cart_professional_ids = cart_professional_ids, carts = carts)
        else:
            return render_template("No_Professional_Available.html", service=service, user_role = user.u_role)

    elif user.u_role == 2:
        flash("Professional cannot request service")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 0:
        flash("Admin cannot request service")
        return redirect(url_for("main.dashboard"))


@my_blueprint.route("/cart", methods = ["GET", "POST"])
@requires_login
def cart():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        carts = Cart.query.filter_by(cart_customer_id = customer.c_id).all()
        total = sum([(cart.service.s_rate * cart.service.s_time_required) for cart in carts])
        return render_template("cart.html", carts = carts, user_role = user.u_role, total = total)
    elif user.u_role == 2:
        flash("Professionals do not have a cart")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 0:
        flash("Admin does not have a cart")
        return redirect(url_for("main.dashboard"))


@my_blueprint.route("/add_to_cart/<int:p_id>")
@requires_login
def add_to_cart(p_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        service_provider = ServiceProvider.query.filter_by(p_id = p_id).first()
        service = Service.query.filter_by(s_id = service_provider.p_service_id).first()
        new_cart = Cart(cart_customer_id = customer.c_id, cart_service_provider_id = service_provider.p_id, cart_service_id = service.s_id)
        db.session.add(new_cart)
        db.session.commit()
        flash("Service Added to Cart Successfully")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 2:
        flash("Professionals do not have a cart")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 0:
        flash("Admin does not have a cart")
        return redirect(url_for("main.dashboard"))

@my_blueprint.route("/remove_from_cart/<int:cart_id>")
@requires_login
def remove_from_cart(cart_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        cart = Cart.query.filter_by(cart_id = cart_id).first()
        if not cart:
            flash("Service not found in cart")
            return redirect(url_for("main.cart"))
        
        if cart.cart_customer_id != customer.c_id:
            flash("You do not have permission to remove this service from cart")
            return redirect(url_for("main.cart"))
        
        db.session.delete(cart)
        db.session.commit()
        flash("Service Removed from Cart Successfully")
        return redirect(url_for("main.cart"))
    elif user.u_role == 2:
        flash("Professionals do not have a cart")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 0:
        flash("Admin does not have a cart")
        return redirect(url_for("main.dashboard"))

@my_blueprint.route("/checkout")
@requires_login
def checkout():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        carts = Cart.query.filter_by(cart_customer_id = customer.c_id).all()
        if not carts:
            flash("Cart is Empty")
            return redirect(url_for("main.dashboard"))
        total = sum([(cart.service.s_rate * cart.service.s_time_required) for cart in carts])
        current_date_time = datetime.now(tz=None).strftime('%d %B %Y %I:%M %p')
        return render_template("checkout.html", carts = carts, user_role = user.u_role, total = total, current_date_time = current_date_time, customer = customer)
    elif user.u_role == 2:
        flash("Professionals cannot Checkout")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 0:
        flash("Admin cannot Checkout")
        return redirect(url_for("main.dashboard"))
