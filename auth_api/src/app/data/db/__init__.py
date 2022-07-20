from .db_models import AuthHistory, Permission, Role, RolePermission, UserPersonalData, UserRole


class AuthDB:


    @property
    def auth_history(self):
        return AuthHistory()

    @property
    def user_personal_data(self):
        return UserPersonalData()

    @property
    def role(self):
        return Role()

    @property
    def permission(self):
        return Permission()

    @property
    def role_permission(self):
        return RolePermission()

    @property
    def user_role(self):
        return UserRole()

