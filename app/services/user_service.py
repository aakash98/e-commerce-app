from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:

    @classmethod
    def get_by_username(cls, username):
        user = User.objects(username=username).first()
        return user

    @classmethod
    def get_by_id(cls, user_id):
        user = User.objects(id=user_id).first()
        return user

    @classmethod
    def verify_password(cls, username, password):
        user = cls.get_by_username(username)
        return check_password_hash(user.password, password)

    @classmethod
    def create_user(cls, **kwargs):
        kwargs.pop('id', None)
        if 'password' in kwargs:
            kwargs['password'] = generate_password_hash(kwargs['password'],'pbkdf2')
        user = User(**kwargs)
        user.save()
        return user

    @classmethod
    def update_user(cls, user_id, **kwargs):
        user = cls.get_by_id(user_id)
        kwargs.pop('id', None)
        kwargs.pop('username', None)
        if 'password' in kwargs:
            kwargs['password'] = generate_password_hash(kwargs['password'], 'pbkdf2')
        user.update(**kwargs)
        user.save()
        return user

    @classmethod
    def delete_user(cls, user_id):
        user = cls.get_by_id(user_id)
        user.delete()
        return True
