import click
from app.data.datastore.roles_datastore import RolesCRUD
from app.data.datastore.user_datastore import UserDataStore
from app.data.db.db_models import Users
from flask import Blueprint

adm_cmd = Blueprint('adm-cmd', __name__)


@adm_cmd.cli.command('create-superuser')
@click.argument('name')
@click.argument('password')
def create_superuser(name, password):
    check_user = Users.query.filter_by(username=name).one_or_none()
    if check_user is not None:
        return print('This name already taken')
    else:
        user = UserDataStore.register_user(name, password)
    check_role = Role.query.filter_by(role_type='superuser').one_or_none()
    if check_role is None:
        super_role = RolesCRUD.create_role('superuser', 'Супер пользователь, может все')
        RolesCRUD.add_role_to_user(user, super_role.id)
    else:
        RolesCRUD.add_role_to_user(user, check_role.id)
    print('Superuser created')
