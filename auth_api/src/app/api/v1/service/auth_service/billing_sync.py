from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields, reqparse

auth = Blueprint('billing_sync', __name__)

auth_namespace = Namespace("billing_sync", description='billing_sync')

registration_model = auth_namespace.model('billing_sync', {
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
})


class BillingSyncAPI(Resource):

    @staticmethod
    def post():
        body = request.get_json()
        print(body)