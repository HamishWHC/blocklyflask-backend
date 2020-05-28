import bcrypt
from marshmallow import fields, validate, post_load

from app import marshmallow
from app.models import User


class UserSchema(marshmallow.ModelSchema):
    class Meta:
        model = User
        fields = ("id", "email", "projects", "username", "password")

    id = fields.Integer(dump_only=True)
    email = fields.String(required=True, validate=validate.Regexp(r"^[^@]+@[^@]+\.[^@]+$"))
    username = fields.String(required=True,
                             validate=[validate.Regexp(r"^[a-zA-Z_\-0-9]{6,20}$"), validate.Length(min=6, max=20)])
    password = fields.String(required=True, validate=[validate.Length(min=8)], load_only=True)
    projects = fields.Nested("ProjectSchema", exclude=("user", "root_directory"), many=True, dump_only=True)

    @post_load(pass_original=True)
    def hash_loaded_password(self, data, original_data, **kwargs):
        data["hashed_password"] = bcrypt.hashpw(original_data["password"].encode(), bcrypt.gensalt()).decode()
        return data
