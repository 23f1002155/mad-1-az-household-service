from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
from application.models import ServiceCategory
from application.database import db
from application.validation import Not_Found

category_fields = {
    'sc_name': fields.String
}

create_service_category_parser = reqparse.RequestParser()
create_service_category_parser.add_argument('sc_name', type=str, required=True)


class ServiceCategoryAPI(Resource):
    @marshal_with(category_fields)
    def get(self, sc_id=None):
        if sc_id:
            category = ServiceCategory.query.get_or_404(sc_id)
            return category
        else:
            categories = ServiceCategory.query.all()
            return categories

    @marshal_with(category_fields)
    def post(self):
        data = request.get_json()
        new_category = ServiceCategory(sc_name=data['sc_name'])
        db.session.add(new_category)
        db.session.commit()
        return new_category, 201

    @marshal_with(category_fields)
    def put(self, sc_id):
        category = ServiceCategory.query.get_or_404(sc_id)
        data = request.get_json()
        category.sc_name = data.get('sc_name', category.sc_name)
        db.session.commit()
        return category, 200

    def delete(self, sc_id):
        category = ServiceCategory.query.get_or_404(sc_id)
        db.session.delete(category)
        db.session.commit()
        return '', 204

