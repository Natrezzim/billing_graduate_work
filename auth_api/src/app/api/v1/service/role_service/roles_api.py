import os
import uuid

from app.data.datastore.roles_datastore import RolesCRUD
from app.data.decorators import admin_required
from app.utils.pagination import get_paginated_list
from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse

roles = Blueprint('roles', __name__)

ROLE_START_PAGE = os.getenv('ROLE_START_PAGE')
ROLE_PAGE_LIMIT = os.getenv('ROLE_PAGE_LIMIT')

role_namespace = Namespace("roles", description='roles')

roles_model = role_namespace.model('Roles', {
    'id': fields.String,
    'role': fields.String,
    'description': fields.String,
})


@role_namespace.doc(params={'access_token': 'access_token'})
class RolesAPI(Resource):
    """
    Логика работы метода api/v1/roles
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=uuid.uuid4(), required=False, help="id")
    parser.add_argument('role', type=str, required=False, help="role")
    parser.add_argument('description', type=str, required=False, help="description")

    @staticmethod
    @admin_required()
    def get():
        return jsonify(get_paginated_list(RolesCRUD.get_all_roles(), '/api/v1/roles',
                                          start=request.args.get('start', ROLE_START_PAGE),
                                          limit=request.args.get('limit', ROLE_PAGE_LIMIT)))

    @staticmethod
    @role_namespace.expect(roles_model)
    @admin_required()
    def post():
        body = request.get_json()
        try:
            return jsonify({'message': 'Role Created'},
                           RolesCRUD.create_role(body.get("role"), body.get("description")))
        except Exception as e:
            return str(e)

    @staticmethod
    @role_namespace.expect(roles_model)
    @admin_required()
    def put():
        body = request.get_json()
        try:
            RolesCRUD.update_role(body.get("id"), body.get("role"), body.get("description"))
            return {'message': 'Role Updated'}
        except Exception as e:
            return str(e)

    @staticmethod
    @role_namespace.expect(roles_model)
    @admin_required()
    def delete():
        body = request.get_json()
        try:
            RolesCRUD.delete_role(body.get("id"))
            return {'message': 'Role Deleted'}
        except Exception as e:
            return str(e)


user_roles_model = role_namespace.model('UserRoles', {
    'user_id': fields.String,
    'role_id': fields.String
})


@role_namespace.doc(params={'access_token': 'access_token'})
class UserRolesAPI(Resource):
    """
    Логика работы метода api/v1/user-roles
    """

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=uuid.uuid4(), required=False, help="user_id")
    parser.add_argument('role_id', type=uuid.uuid4(), required=False, help="role_id")

    @staticmethod
    @role_namespace.doc(params={'user_id': 'user_id'})
    @admin_required()
    def get():
        body = request.args
        return jsonify(RolesCRUD.check_user_role(body["user_id"]))

    @staticmethod
    @role_namespace.expect(user_roles_model)
    @admin_required()
    def post():
        body = request.get_json()
        try:
            jsonify(RolesCRUD.add_role_to_user(body.get("user_id"), body.get("role_id")))
            return {'message': 'Role added to User'}
        except Exception as e:
            return str(e)

    @staticmethod
    @role_namespace.expect(user_roles_model)
    @admin_required()
    def delete():
        body = request.get_json()
        try:
            jsonify(RolesCRUD.delete_user_role(body.get("user_id"), body.get("role_id")))
            return {'message': 'User role deleted'}
        except Exception as e:
            return str(e)
