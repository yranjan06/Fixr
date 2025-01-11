from flask import jsonify, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user
from backend.models import User, Role, Service, db

api = Api(prefix='/api')

# Serialization fields
user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'active': fields.Boolean,
}

role_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
}

service_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'base_price': fields.Float,
    'description': fields.String,
    'category': fields.String,
}

# User Resources
class UserAPI(Resource):
    @marshal_with(user_fields)
    @auth_required('token')
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user

    @auth_required('token')
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

# Role Resources
class RoleAPI(Resource):
    @marshal_with(role_fields)
    @auth_required('token')
    def get(self, role_id):
        role = Role.query.get(role_id)
        if not role:
            return {"message": "Role not found"}, 404
        return role

# Service Resources
class ServiceAPI(Resource):
    @marshal_with(service_fields)
    def get(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404
        return service

    def delete(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404

        db.session.delete(service)
        db.session.commit()
        return {"message": "Service deleted"}, 200

    def put(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404

        data = request.get_json()
        service.name = data.get('name', service.name)
        service.base_price = data.get('base_price', service.base_price)
        service.description = data.get('description', service.description)
        service.category = data.get('category', service.category)

        db.session.commit()
        return {"message": "Service updated"}, 200

class ServiceListAPI(Resource):
    @marshal_with(service_fields)
    def get(self):
        services = Service.query.all()
        return services

    def post(self):
        data = request.get_json()
        name = data.get('name')
        base_price = data.get('base_price')
        description = data.get('description')
        category = data.get('category')

        if not all([name, base_price, category]):
            return {"message": "Missing required fields"}, 400

        service = Service(
            name=name,
            base_price=base_price,
            description=description,
            category=category
        )

        db.session.add(service)
        db.session.commit()
        return {"message": "Service created"}, 201

# Register resources
api.add_resource(UserAPI, '/users/<int:user_id>')
api.add_resource(RoleAPI, '/roles/<int:role_id>')
api.add_resource(ServiceAPI, '/services/<int:service_id>')
api.add_resource(ServiceListAPI, '/services')
