from flask import jsonify, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user
from backend.models import db, ServicePackage

api = Api(prefix="/api")

package_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "price": fields.Float,
    "description": fields.String,
    "professional_id": fields.Integer,
    "service_id": fields.Integer,
}


class ServicePackageAPI(Resource):
    @marshal_with(package_fields)
    @auth_required("token")
    def get(self, package_id):
        package = ServicePackage.query.get(package_id)
        if not package:
            return {"message": "not found"}, 404
        return package


api.add_resource(ServicePackageAPI, "/packages/<int:package_id>")
