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
        c_password = request.form.get("inputPassword4")
        c_confirm_password = request.form.get("inputConfirmPassword4")
        c_address = request.form.get("inputAddress")
        c_city = request.form.get("inputCity")
        c_pincode = request.form.get("inputZip")
        blocked = False

        if not c_name or not c_email or not c_password or not c_confirm_password or not c_city or not c_pincode or not c_address:
            flash("All fields are required")
            return redirect(url_for("main.sign_up_customer"))
        if c_password != c_confirm_password:    
            flash("Passwords do not match")
            return redirect(url_for("main.sign_up_customer"))
        
        user = User.query.filter_by(u_name = c_name).first()
        user_email = User.query.filter_by(u_email = c_email).first()
        if user or user_email:
            flash("Email already exists")
            return redirect(url_for("main.sign_up_customer"))
        else:
            passhash = generate_password_hash(c_password)
            new_user = User(u_name = c_name, u_email = c_email, u_passhash = passhash, u_role = 1)
            new_customer = Customer(c_name = c_name, c_email = c_email, c_address = c_address, c_city = c_city, c_pincode = c_pincode, c_user_id = new_user.u_id, c_blocked = blocked)
            db.session.add(new_user)
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
        username = request.form.get("inputName")
        email = request.form.get("inputEmail4")
        password = request.form.get("inputPassword4")
        confirm_password = request.form.get("inputConfirmPassword4")
        contact_number = request.form.get("inputPhone")
        service_id= request.form.get("inputService")
        experience = request.form.get("inputExperience")
        verfiication_document = request.files.get("inputVerificationDocument")
        if not verfiication_document:
            flash("Please upload a verification document")
            return redirect(url_for("main.sign_up_serviceprovider"))
        else:
            verfiication_document.save(f"static/verification/{verfiication_document.filename}")
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
        new_provider = ServiceProvider(p_name = username, p_email = email, p_contact_number = contact_number, p_experience = experience, p_city = city, p_pincode = pincode, p_user_id = new_user.u_id, p_service_id = service_id, p_approved = approved, p_blocked = blocked, p_verification_document = verfiication_document.filename, p_address = address)
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
        return render_template("admin_dashboard.html" , services = services, services_providers = services_providers, customers = customers, categories = categories, user_role = user.u_role)
    elif user.u_role == 1:
        customer = Customer.query.filter_by(c_user_id = session["user_id"]).first()
        service_requests = ServiceRequest.query.filter_by(sr_customer_id = customer.c_id).all()
        service_ids = {request.sr_service_id for request in service_requests}
        services = Service.query.filter(Service.s_id.in_(service_ids)).all()
        service_categories = ServiceCategory.query.all()
        ServiceAlias = aliased(Service)
        CustomerAlias = aliased(Customer)

        temp_table = db.session.query(
            ServiceRequest.sr_id,
            ServiceRequest.sr_status,
            ServiceRequest.sr_date_time,
            ServiceAlias.s_name.label('s_name'),
            CustomerAlias.c_name.label('c_name'),
            CustomerAlias.c_address.label('c_address'),
            CustomerAlias.c_city.label('c_city'),
            CustomerAlias.c_pincode.label('c_pincode')
        ).join(
            ServiceAlias, ServiceRequest.sr_service_id == ServiceAlias.s_id
        ).join(
            CustomerAlias, ServiceRequest.sr_customer_id == CustomerAlias.c_id
        ).filter(
            ServiceRequest.sr_customer_id == customer.c_id
        ).all()
        return render_template("customer_dashboard.html", service_categories = service_categories, temp_table = temp_table, user_role = user.u_role)

    elif user.u_role == 2:
        user = User.query.filter_by(u_id = session["user_id"]).first()
        service_provider = ServiceProvider.query.filter_by(p_user_id = user.u_id).first()
        service_requests = ServiceRequest.query.filter_by(sr_service_provider_id = service_provider.p_id).all()
        service_feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id = service_provider.p_id).all()
        CustomerAlias = aliased(Customer)
        ServiceProviderAlias = aliased(ServiceProvider)

        temp_table = db.session.query(
            ServiceRequest.sr_id,
            ServiceRequest.sr_status,
            ServiceRequest.sr_date_time,
            CustomerAlias.c_name.label('c_name'),
            CustomerAlias.c_city.label('c_city'),
            CustomerAlias.c_pincode.label('c_pincode'),
            ServiceProviderAlias.p_verification_document.label('p_verification_document'),
            ServiceProviderAlias.p_blocked.label('p_blocked')
        ).join(
            CustomerAlias, ServiceRequest.sr_customer_id == CustomerAlias.c_id
        ).join(
            ServiceProviderAlias, ServiceRequest.sr_service_provider_id == ServiceProviderAlias.p_id
        ).filter(
            ServiceRequest.sr_service_provider_id == service_provider.p_id
        ).all()
        return render_template("service_provider_dashboard.html", temp_table = temp_table, service_feedbacks = service_feedbacks, user_role = user.u_role)






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

@my_blueprint.route("/search", methods = ["GET", "POST"])
@requires_login
def search():
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if request.method == "GET":
        return render_template("search.html", user_role = user.u_role)
    elif request.method == "POST":
        value = request.form.get("search_by")
        search = request.form.get("search")
        ServiceAliased = aliased(Service)        
        temp_tables = db.session.query(
        ServiceProvider.p_id,
        ServiceProvider.p_name,
        ServiceProvider.p_city,
        ServiceProvider.p_pincode,
        ServiceProvider.p_experience,
        ServiceAliased.s_id,
        ServiceAliased.s_name.label('s_name')
        ).join(
            ServiceAliased, ServiceProvider.p_service_id == ServiceAliased.s_id
        ).all()

        service_providers_and_ratings = []
        for service_provider in temp_tables:
            feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id= service_provider.p_id).all()
            if feedbacks:
                average_rating = sum(feedback.sf_rating for feedback in feedbacks) / len(feedbacks)
            else:
                average_rating = "No Ratings"
            service_providers_and_ratings.append((service_provider, average_rating))
        
        if not search:
            flash("Please enter a search term")
            return redirect(url_for("main.search"))
        if value == "search_by":
            flash("Please select a search by option")
            return redirect(url_for("main.search"))


        search_result = []
        if value == "p_name":
            search_result = [temp_table for temp_table in service_providers_and_ratings if search.lower() in temp_table[0].p_name.lower()]
            if search_result:
                return render_template("customer_search_result.html", search_result = search_result, user_role = user.u_role)
            else:
                return render_template("No_Results_Found.html", user_role = user.u_role)
        elif value == "p_city":
            search_result = [temp_table for temp_table in service_providers_and_ratings if search.lower() in temp_table[0].p_city.lower()]
            if search_result:
                return render_template("customer_search_result.html", search_result = search_result, user_role = user.u_role)
            else:
                return render_template("No_Results_Found.html", user_role = user.u_role)
        elif value == "p_pincode":
            search_result = [temp_table for temp_table in service_providers_and_ratings if int(search) == temp_table[0].p_pincode]
            if search_result:
                return render_template("customer_search_result.html", search_result = search_result, user_role = user.u_role)
            else:
                return render_template("No_Results_Found.html", user_role = user.u_role)
        elif value == "p_experience":
            search_result = [temp_table for temp_table in service_providers_and_ratings if int(search) <= temp_table[0].p_experience]
            if search_result:
                return render_template("customer_search_result.html", search_result = search_result, user_role = user.u_role)
            else:
                return render_template("No_Results_Found.html", user_role = user.u_role)
        elif value == "s_name":
            search_result = [temp_table for temp_table in service_providers_and_ratings if search.lower() in temp_table[0].s_name.lower()]
            if search_result:
                return render_template("customer_search_result.html", search_result = search_result, user_role = user.u_role)
            else:
                return render_template("No_Results_Found.html", user_role = user.u_role)
        elif value == "rating":
            search_result = [temp_table for temp_table in service_providers_and_ratings if temp_table[1] != "No Ratings" and int(search) <= temp_table[1]]
            if search_result:
                return render_template("customer_search_result.html", search_result = search_result, user_role = user.u_role)
            else:
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

@my_blueprint.route("/service_request/<int:s_id>")
@requires_login
def service_request(s_id):
    user = User.query.filter_by(u_id = session["user_id"]).first()
    if user.u_role == 1:
        sr_customer = Customer.query.filter_by(c_user_id = user.u_id).first()
        if sr_customer.c_blocked:
            flash("You are blocked by admin. Please contact admin for further details")
            return redirect(url_for("main.dashboard"))
        sr_service_provider = ServiceProvider.query.filter_by(p_service_id = s_id).first()
        sr_status = "Requested"
        sr_date_time = str(datetime.now(tz=None))
        new_sr_date_time = datetime.strptime(sr_date_time.split('.')[0], '%Y-%m-%d %H:%M:%S')
        new_service_request = ServiceRequest(sr_customer_id = sr_customer.c_id, sr_service_provider_id = sr_service_provider.p_id, sr_service_id = s_id, sr_status = sr_status, sr_date_time = new_sr_date_time)
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
            completion_date_time = str(datetime.now(tz=None))
            new_completion_date_time = datetime.strptime(completion_date_time.split('.')[0], '%Y-%m-%d %H:%M:%S')
            return render_template("feedback.html", service_request = service_request, service_provider = service_provider, service = service, completion_date_time = new_completion_date_time, user_role = user.u_role)
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
            completion_date_time_str = request.form.get("completion_date_time")
            service_request.sr_date_time = datetime.strptime(completion_date_time_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
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
        service_providers = ServiceProvider.query.filter_by(p_service_id = s_id).all()
        service_providers_and_ratings = []
        for service_provider in service_providers:
            feedbacks = ServiceFeedback.query.filter_by(sf_service_provider_id= service_provider.p_id).all()
            if feedbacks:
                average_rating = sum(feedback.sf_rating for feedback in feedbacks) / len(feedbacks)
            else:
                average_rating = "No Ratings"
            service_providers_and_ratings.append((service_provider, average_rating))
        
        if service_providers_and_ratings:
            return render_template("professional_list.html", service=service, service_providers_and_ratings=service_providers_and_ratings, user_role = user.u_role, customer = customer)
        else:
            return render_template("No_Professional_Available.html", service=service, user_role = user.u_role)

    elif user.u_role == 2:
        flash("Professional cannot request service")
        return redirect(url_for("main.dashboard"))
    elif user.u_role == 0:
        flash("Admin cannot request service")
        return redirect(url_for("main.dashboard"))
