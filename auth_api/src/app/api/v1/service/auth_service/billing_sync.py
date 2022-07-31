from flask import Blueprint, request
from flask_restx import Namespace, Resource, fields

from app.data.datastore.roles_datastore import RolesCRUD

from app.data.datastore.user_datastore import UserDataStore

from app.data.db import Role, UserRole
from flask_restx._http import HTTPStatus

sync = Blueprint('billing_sync', __name__)

billing_sync_namespace = Namespace("billing_sync", description='billing_sync')

user_product_fields = billing_sync_namespace.model('user_product_fields', {'user_id': fields.String,
                                                                           'product_name': fields.String,
                                                                           'created_at': fields.String})

sync_model = billing_sync_namespace.model(
    'billing_sync', {
        'total': fields.Integer,
        'items': fields.List(fields.Nested(user_product_fields))
    }
)


class BillingSyncAPI(Resource):

    @staticmethod
    @billing_sync_namespace.expect(sync_model)
    def post():
        body = request.get_json()
        for item in body['items']:
            if UserDataStore.get_user_info(item['user_id']) is not None:
                subscribe_role = Role.query.filter_by(role_type='subscribe').one_or_none()
                if subscribe_role is not None and item['product_name'] in ['1 month', '3 months', '6 months', '1 year']:
                    if UserRole.query.filter_by(user_id=item['user_id'], role_id=subscribe_role.id).one_or_none() \
                            is None:
                        RolesCRUD.add_role_to_user(item['user_id'], subscribe_role.id)
                        return HTTPStatus.OK
                    return {"error": {"message": "User with this role already exist"}}, HTTPStatus.BAD_REQUEST
                return {"error": {"message": "Role not found or wrong product_name field"}}, HTTPStatus.BAD_REQUEST
            return {"error": {"message": "User not found"}}, HTTPStatus.BAD_REQUEST
        return {"error": {"message": "Wrong data in items"}}, HTTPStatus.BAD_REQUEST
