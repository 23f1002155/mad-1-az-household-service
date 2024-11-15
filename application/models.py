from .database import db




class Role(db.Model):
    __tablename__ = "user_role"
    role_id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String, nullable = False, unique = True)

class User(db.Model):
    __tablename__ = 'user_database'
    u_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    u_name = db.Column(db.String, nullable = False, unique = True)
    u_email = db.Column(db.String, nullable = False, unique = True)
    u_passhash = db.Column(db.String(256), nullable=False, unique=True)
    u_role = db.Column(db.Integer, db.ForeignKey('user_role.role_id'))

    roles = db.relationship("Role", backref = "user_database", lazy = True)



class Customer(db.Model):
    __tablename__ = "customer_database"
    c_id = db.Column(db.Integer, primary_key = True)
    c_name = db.Column(db.String, nullable = False)
    c_email = db.Column(db.String, nullable = False)
    c_fname = db.Column(db.String, nullable = False)
    c_lname = db.Column(db.String, nullable = False)
    c_address = db.Column(db.String, nullable = False)
    c_city = db.Column(db.String, nullable = False)
    c_pincode = db.Column(db.Integer, nullable = False)
    c_user_id = db.Column(db.Integer, db.ForeignKey('user_database.u_id'))
    c_blocked = db.Column(db.Boolean, nullable = False)

    user = db.relationship("User", backref = "customer_database", lazy = True)

class ServiceProvider(db.Model):
    __tablename__ = "service_provider_database"
    p_id = db.Column(db.Integer, primary_key = True)
    p_name = db.Column(db.String, nullable = False)
    p_email = db.Column(db.String, nullable = False)
    p_fname = db.Column(db.String, nullable = True)
    p_lname = db.Column(db.String, nullable = True)
    p_contact_number = db.Column(db.Integer, nullable = False)
    p_experience = db.Column(db.Integer, nullable = False)
    p_verification_document = db.Column(db.String, nullable = False)
    p_address = db.Column(db.String, nullable = False)
    p_city = db.Column(db.String, nullable = False)
    p_pincode = db.Column(db.Integer, nullable = False)
    p_user_id = db.Column(db.Integer, db.ForeignKey('user_database.u_id'))
    p_service_id = db.Column(db.Integer, db.ForeignKey('service_database.s_id'))
    p_approved = db.Column(db.Boolean, nullable = False)
    p_blocked = db.Column(db.Boolean, nullable = False)

    user = db.relationship("User", backref = "service_provider_database", lazy = True)
    service = db.relationship("Service", backref = "service_provider_database", lazy = True)


class ServiceCategory(db.Model):
    __tablename__ = "service_category_database"
    sc_id = db.Column(db.Integer, primary_key = True)
    sc_name = db.Column(db.String, nullable = False)
    

class Service(db.Model):
    __tablename__ = "service_database"
    s_id = db.Column(db.Integer, primary_key = True)
    s_name = db.Column(db.String, nullable = False)
    s_rate = db.Column(db.Integer, nullable = False)
    s_description = db.Column(db.String, nullable = False)
    s_time_required = db.Column(db.REAL, nullable = False)
    s_category_id = db.Column(db.Integer, db.ForeignKey('service_category_database.sc_id'))
    s_image = db.Column(db.String, nullable = False)
    category = db.relationship("ServiceCategory", backref = "service_database", lazy = True)


class ServiceRequest(db.Model):
    __tablename__ = "service_request_database"
    sr_id = db.Column(db.Integer, primary_key = True)
    sr_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction_database.t_id'))
    sr_service_id = db.Column(db.Integer, nullable = False)
    sr_service_name = db.Column(db.String, nullable = False)
    sr_total = db.Column(db.REAL, nullable = False)
    sr_service_provider_id = db.Column(db.Integer, nullable = False)
    sr_service_provider_name = db.Column(db.String, nullable = False)
    sr_service_provider_fullname = db.Column(db.String, nullable = False)
    sr_service_provider_email = db.Column(db.String, nullable = False)
    sr_service_provider_contact_number = db.Column(db.Integer, nullable = False)
    sr_customer_id = db.Column(db.Integer, nullable = False)
    sr_customer_name = db.Column(db.String, nullable = False)
    sr_customer_fullname = db.Column(db.String, nullable = False)
    sr_customer_email = db.Column(db.String, nullable = False)
    sr_address = db.Column(db.String, nullable = False)
    sr_city = db.Column(db.String, nullable = False)
    sr_pincode = db.Column(db.Integer, nullable = False)
    sr_date_time = db.Column(db.DateTime, nullable = False)
    sr_status = db.Column(db.String, nullable = False)

    transaction = db.relationship('Transaction', back_populates='service_requests', overlaps="service_request_database,transaction", lazy = True)

class Cart(db.Model):
    __tablename__ = "cart_database"
    cart_id = db.Column(db.Integer, primary_key = True)
    cart_customer_id = db.Column(db.Integer, db.ForeignKey('customer_database.c_id'))
    cart_service_id = db.Column(db.Integer, db.ForeignKey('service_database.s_id'))
    cart_service_provider_id = db.Column(db.Integer, db.ForeignKey('service_provider_database.p_id'))

    customer = db.relationship("Customer", backref = "cart_database", lazy = True)
    service = db.relationship("Service", backref = "cart_database", lazy = True)
    service_provider = db.relationship("ServiceProvider", backref = "cart_database", lazy = True)

class Transaction(db.Model):
    __tablename__ = "transaction_database"
    t_id = db.Column(db.Integer, primary_key = True)
    t_customer_id = db.Column(db.Integer, nullable = False)
    t_date_time = db.Column(db.DateTime, nullable = False)
    t_total_amount = db.Column(db.REAL, nullable = False)

    service_requests = db.relationship('ServiceRequest', back_populates='transaction', overlaps="service_request_database,transaction", lazy = True)

class ServiceFeedback(db.Model):
    __tablename__ = "service_feedback_database"
    sf_id = db.Column(db.Integer, primary_key = True)
    sf_service_request_id = db.Column(db.Integer, db.ForeignKey('service_request_database.sr_id'))
    sf_rating = db.Column(db.REAL, nullable = True)
    sf_feedback = db.Column(db.String, nullable = True)
    sf_customer_id = db.Column(db.Integer, db.ForeignKey('customer_database.c_id'))
    sf_service_provider_id = db.Column(db.Integer, db.ForeignKey("service_provider_database.p_id"))

    service_request = db.relationship("ServiceRequest", backref = "service_feedback_database", lazy = True)
    service_customer = db.relationship("Customer", backref = "service_feedback_database", lazy = True)

