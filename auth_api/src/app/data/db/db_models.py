import uuid
from dataclasses import dataclass

from app.data.db.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression


@dataclass
class Users(db.Model):
    __tablename__ = 'users'

    id: uuid.uuid4()
    username: str
    password: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Users {self.id}>'


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS auth_history_in_smart PARTITION OF auth_history FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS auth_history_in_mobile PARTITION OF auth_history FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS auth_history_in_web PARTITION OF auth_history FOR VALUES IN ('web')"""
    )


@dataclass
class AuthHistory(db.Model):
    __tablename__ = 'auth_history'
    __table_args__ = (
        {
            'postgresql_partition_by': 'LIST (device)',
            'listeners': [('after_create', create_partition)],
        },
    )

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    user_agent: str
    device: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    auth_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    device = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return f'<AuthHistory {self.id}>'


@dataclass
class UserPersonalData(db.Model):
    __tablename__ = 'user_personal_data'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    email: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    email = db.Column(db.String, nullable=True, unique=True)

    def __repr__(self):
        return f'<UserPersonalData {self.id}>'


@dataclass
class Role(db.Model):
    __tablename__ = 'role'

    id: uuid.uuid4()
    role_type: str
    description: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    role_type = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Role {self.id}>'


@dataclass
class Permission(db.Model):
    __tablename__ = 'permission'

    id: uuid.uuid4()
    permission_id: int
    description: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    permission_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Permission {self.id}>'


@dataclass
class RolePermission(db.Model):
    __tablename__ = 'role_permission'

    id: uuid.uuid4()
    role_id: uuid.uuid4()
    permission_id: uuid.uuid4()

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=False, nullable=False)
    permission_id = db.Column(UUID(as_uuid=True), ForeignKey("permission.id"), unique=False, nullable=False)

    def __repr__(self):
        return f'<RolePermission {self.id}>'


@dataclass
class UserRole(db.Model):
    __tablename__ = 'user_role'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    role_id: uuid.uuid4()

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=False, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey("role.id"), unique=False, nullable=False)

    def __repr__(self):
        return f'<UserRole {self.id}>'


@dataclass
class Tokens(db.Model):
    __tablename__ = 'tokens'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    refresh_token: str

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)

    def __iter__(self):
        return iter(self.data)


@dataclass
class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    social_id: str
    social_name: str

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(Users, backref=db.backref('social_accounts', lazy=True))
    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'

@dataclass
class UsersSercrestsTotp(db.Model):

    id: uuid.uuid4()
    user_id: uuid.uuid4()
    secret: str
    verified: bool

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), unique=True, nullable=False)
    secret = db.Column(db.Text, nullable=False)
    verified = db.Column(db.Boolean, server_default=expression.false(), nullable=False)

    def __repr__(self):
        return f'<SocialAccount {self.user_id}>'